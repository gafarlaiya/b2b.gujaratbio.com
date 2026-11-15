-- GBO order control: one record per order, from won lead to money received.
-- Every step is written only through the order_* functions below. They check who is acting,
-- refuse a step that skips the rules, and log the step with name and time in order_events.
-- Rules:
--   * Farmer orders are Advance: they cannot be dispatched until the full invoice amount is paid.
--   * B2B orders may be Credit: they get a payment due date (invoice date + credit days).
--   * Dispatch needs a Tally invoice number, an LR/AWB/vehicle number and a photo of the slip or loaded goods.
--   * Payment needs a reference (UTR, cheque no. or cash receipt no.); the same reference cannot be used twice.
--   * Delivery needs a confirmation method; a photo when it is a signed receipt.
--   * Recorded steps cannot be changed afterwards except by an admin, with a reason (order_correct).

create sequence if not exists public.order_seq;

create table if not exists public.orders (
  id uuid primary key default gen_random_uuid(),
  order_no text unique not null,
  created_at timestamptz not null default now(),
  created_by text not null,
  created_by_email text,
  lead_id uuid references public.leads(id) on delete set null,
  customer_type text not null check (customer_type in ('Farmer','B2B')),
  customer_name text not null,
  phone text,
  gst_no text,
  address text,
  district text,
  state text,
  terms text not null check (terms in ('Advance','Credit')),
  credit_days int check (credit_days is null or credit_days between 0 and 180),
  order_value numeric not null default 0,
  notes text,
  invoice_no text unique,
  invoice_date date,
  invoice_amount numeric check (invoice_amount is null or invoice_amount > 0),
  invoice_file text,
  invoiced_by text,
  invoiced_at timestamptz,
  payment_due date,
  dispatched_at timestamptz,
  dispatch_mode text,
  transporter text,
  tracking_no text,
  batch_nos text,
  dispatch_photo text,
  dispatched_by text,
  delivered_at timestamptz,
  delivery_proof text,
  delivery_photo text,
  delivery_note text,
  delivered_by text,
  cancelled_at timestamptz,
  cancelled_by text,
  cancel_reason text,
  last_alerts jsonb not null default '{}'::jsonb
);
create index if not exists orders_lead_idx on public.orders(lead_id);
create index if not exists orders_created_idx on public.orders(created_at desc);

create table if not exists public.order_items (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.orders(id) on delete cascade,
  product text not null,
  pack text,
  qty numeric not null check (qty > 0),
  rate numeric not null default 0 check (rate >= 0),
  amount numeric generated always as (qty * rate) stored
);
create index if not exists order_items_order_idx on public.order_items(order_id);

create table if not exists public.order_payments (
  id uuid primary key default gen_random_uuid(),
  order_id uuid not null references public.orders(id) on delete cascade,
  created_at timestamptz not null default now(),
  amount numeric not null check (amount > 0),
  mode text not null check (mode in ('UPI','Bank transfer','Cheque','Cash','Other')),
  reference text not null,
  received_on date not null,
  photo text,
  recorded_by text not null,
  voided boolean not null default false,
  void_reason text
);
create index if not exists order_payments_order_idx on public.order_payments(order_id);

create table if not exists public.order_events (
  id bigserial primary key,
  order_id uuid not null references public.orders(id) on delete cascade,
  at timestamptz not null default now(),
  by_name text,
  by_email text,
  action text not null,
  detail text
);
create index if not exists order_events_order_idx on public.order_events(order_id, at);

alter table public.orders enable row level security;
alter table public.order_items enable row level security;
alter table public.order_payments enable row level security;
alter table public.order_events enable row level security;

-- who is acting
create or replace function public.order_me_email() returns text language sql stable as $$
  select lower(coalesce(auth.jwt() ->> 'email',''))
$$;
create or replace function public.order_is_admin() returns boolean language sql stable security definer set search_path = public as $$
  select exists (select 1 from public.team t where lower(t.email) = public.order_me_email() and t.role = 'admin')
$$;
create or replace function public.order_me_name() returns text language sql stable security definer set search_path = public as $$
  select coalesce(
    (select nullif(t.name,'') from public.team t where lower(t.email) = public.order_me_email() limit 1),
    (select r.person from public.lead_routes r where r.active and lower(r.email) = public.order_me_email() limit 1),
    nullif(split_part(public.order_me_email(),'@',1),''))
$$;
-- can this person see this order?
create or replace function public.order_visible(o public.orders) returns boolean language sql stable security definer set search_path = public as $$
  select public.is_team()
    or (public.my_route_key() is not null and (
         lower(coalesce(o.created_by_email,'')) = public.order_me_email()
         or exists (select 1 from public.leads l where l.id = o.lead_id and l.routed_to = public.my_route_key())))
$$;

drop policy if exists "orders readable" on public.orders;
create policy "orders readable" on public.orders for select using (public.order_visible(orders));
drop policy if exists "order items readable" on public.order_items;
create policy "order items readable" on public.order_items for select using (exists (select 1 from public.orders o where o.id = order_id and public.order_visible(o)));
drop policy if exists "order payments readable" on public.order_payments;
create policy "order payments readable" on public.order_payments for select using (exists (select 1 from public.orders o where o.id = order_id and public.order_visible(o)));
drop policy if exists "order events readable" on public.order_events;
create policy "order events readable" on public.order_events for select using (exists (select 1 from public.orders o where o.id = order_id and public.order_visible(o)));

create or replace function public.order_log(p_order uuid, p_action text, p_detail text) returns void language sql security definer set search_path = public as $$
  insert into public.order_events(order_id, by_name, by_email, action, detail) values (p_order, public.order_me_name(), public.order_me_email(), p_action, p_detail)
$$;

create or replace function public.order_paid(p_order uuid) returns numeric language sql stable security definer set search_path = public as $$
  select coalesce(sum(amount),0) from public.order_payments where order_id = p_order and not voided
$$;

-- the one place that decides the status, the next step and whether it is stuck
create or replace view public.orders_v with (security_invoker = true) as
select o.*, s.paid, s.due_amount, s.balance, s.status, s.next_step, s.step_since,
  case
    when s.status = 'Awaiting invoice' and s.step_since < now() - interval '24 hours' then 'No Tally invoice for over 24 hours'
    when s.status = 'Awaiting payment' and s.step_since < now() - interval '48 hours' then 'Invoiced, farmer has not paid for over 48 hours'
    when s.status = 'Ready to dispatch' and s.step_since < now() - interval '24 hours' then 'Ready but not dispatched for over 24 hours'
    when s.status = 'In transit' and s.step_since < now() - interval '7 days' then 'Dispatched over 7 days ago, delivery not confirmed'
    when s.status = 'Payment due' and o.payment_due < (now() at time zone 'Asia/Kolkata')::date then 'Payment overdue since ' || to_char(o.payment_due,'DD Mon')
  end as stuck
from public.orders o
cross join lateral (
  select p.paid, d.due_amount, d.due_amount - p.paid as balance,
    case
      when o.cancelled_at is not null then 'Cancelled'
      when o.invoice_no is null then 'Awaiting invoice'
      when o.dispatched_at is null and o.terms = 'Advance' and p.paid < d.due_amount then 'Awaiting payment'
      when o.dispatched_at is null then 'Ready to dispatch'
      when o.delivered_at is null then 'In transit'
      when p.paid < d.due_amount then 'Payment due'
      else 'Closed'
    end as status,
    case
      when o.cancelled_at is not null then null
      when o.invoice_no is null then 'Accounts: enter the Tally invoice'
      when o.dispatched_at is null and o.terms = 'Advance' and p.paid < d.due_amount then 'Accounts: confirm the advance payment'
      when o.dispatched_at is null then 'Dispatch: send it and add the LR/AWB with a photo'
      when o.delivered_at is null then 'Confirm delivery with the customer'
      when p.paid < d.due_amount then 'Accounts: collect the payment by ' || coalesce(to_char(o.payment_due,'DD Mon'),'due date')
    end as next_step,
    case
      when o.invoice_no is null then o.created_at
      when o.dispatched_at is null and o.terms = 'Advance' and p.paid < d.due_amount then o.invoiced_at
      when o.dispatched_at is null then greatest(o.invoiced_at, p.last_paid)
      when o.delivered_at is null then o.dispatched_at
      else o.delivered_at
    end as step_since
  from (select public.order_paid(o.id) as paid,
               (select max(created_at) from public.order_payments x where x.order_id = o.id and not x.voided) as last_paid) p
  cross join (select coalesce(o.invoice_amount, o.order_value) as due_amount) d
) s;

-- 1. create an order (field officer or office). Farmers always pay in advance.
create or replace function public.order_create(p jsonb) returns uuid language plpgsql security definer set search_path = public as $$
declare
  v_id uuid; v_no text; v_type text; v_terms text; v_days int; v_total numeric := 0; it jsonb; v_lead public.leads; v_partner text := public.my_route_key();
begin
  if not public.is_team() and v_partner is null then raise exception 'Only team members can create orders'; end if;
  v_type := p->>'customer_type';
  if v_type is null or v_type not in ('Farmer','B2B') then raise exception 'Choose Farmer or B2B'; end if;
  if coalesce(trim(p->>'customer_name'),'') = '' then raise exception 'Enter the customer name'; end if;
  if length(regexp_replace(coalesce(p->>'phone',''),'\D','','g')) < 10 then raise exception 'Enter the customer phone number'; end if;
  if coalesce(jsonb_typeof(p->'items'),'') <> 'array' or jsonb_array_length(p->'items') = 0 then raise exception 'Add at least one product'; end if;
  v_terms := case when v_type = 'Farmer' then 'Advance' else coalesce(nullif(p->>'terms',''),'Credit') end;
  if v_terms not in ('Advance','Credit') then raise exception 'Payment terms must be Advance or Credit'; end if;
  v_days := case when v_terms = 'Credit' then coalesce(nullif(p->>'credit_days','')::int, 30) else null end;
  if (p->>'lead_id') is not null then
    select * into v_lead from public.leads where id = (p->>'lead_id')::uuid;
    if v_lead.id is null then raise exception 'Lead not found'; end if;
    if v_partner is not null and coalesce(v_lead.routed_to,'') <> v_partner then raise exception 'This lead is not assigned to you'; end if;
  end if;
  v_no := 'ORD-' || to_char(now() at time zone 'Asia/Kolkata','YYMM') || '-' || lpad(nextval('public.order_seq')::text,4,'0');
  insert into public.orders(order_no, created_by, created_by_email, lead_id, customer_type, customer_name, phone, gst_no, address, district, state, terms, credit_days, notes)
  values (v_no, public.order_me_name(), public.order_me_email(), v_lead.id, v_type, left(trim(p->>'customer_name'),160), left(p->>'phone',40),
          nullif(left(trim(p->>'gst_no'),20),''), nullif(left(p->>'address',600),''), nullif(left(p->>'district',80),''), nullif(left(p->>'state',80),''),
          v_terms, v_days, nullif(left(p->>'notes',2000),''))
  returning id into v_id;
  for it in select * from jsonb_array_elements(p->'items') loop
    if coalesce(trim(it->>'product'),'') = '' or coalesce(nullif(it->>'qty','')::numeric,0) <= 0 then raise exception 'Each product needs a name and a quantity'; end if;
    insert into public.order_items(order_id, product, pack, qty, rate)
    values (v_id, left(trim(it->>'product'),160), nullif(left(it->>'pack',60),''), (it->>'qty')::numeric, coalesce(nullif(it->>'rate','')::numeric,0));
  end loop;
  select coalesce(sum(amount),0) into v_total from public.order_items where order_id = v_id;
  update public.orders set order_value = v_total where id = v_id;
  perform public.order_log(v_id, 'Order created', v_type || ', ' || v_terms || case when v_days is not null then ' ' || v_days || ' days' else '' end || ', value Rs ' || to_char(v_total,'FM99,99,99,990'));
  -- the lead becomes Won with the order value (this also sends the Won signal to Meta)
  if v_lead.id is not null and v_lead.stage <> 'Won' then
    insert into public.quotes(lead_id, company, country, value, currency, status, notes)
    values (v_lead.id, coalesce(v_lead.company, v_lead.name), v_lead.country, nullif(v_total,0), 'INR', 'Won', 'From order ' || v_no);
    update public.leads set stage = 'Won', next_followup = null,
      notes = to_char(now() at time zone 'Asia/Kolkata','DD Mon') || ', ' || public.order_me_name() || ': order ' || v_no || ' created' || coalesce(E'\n' || notes,'')
    where id = v_lead.id;
  end if;
  return v_id;
end $$;

-- 2. Tally invoice (office)
create or replace function public.order_invoice(p_order uuid, p_invoice_no text, p_invoice_date date, p_amount numeric, p_file text default null) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders;
begin
  if not public.is_team() then raise exception 'Only the office team can enter invoices'; end if;
  select * into o from public.orders where id = p_order for update;
  if o.id is null then raise exception 'Order not found'; end if;
  if o.cancelled_at is not null then raise exception 'This order is cancelled'; end if;
  if o.invoice_no is not null then raise exception 'Invoice already entered (%). An admin can correct it.', o.invoice_no; end if;
  if coalesce(trim(p_invoice_no),'') = '' then raise exception 'Enter the Tally invoice number'; end if;
  if p_invoice_date is null or p_invoice_date > (now() at time zone 'Asia/Kolkata')::date then raise exception 'Enter a valid invoice date'; end if;
  if coalesce(p_amount,0) <= 0 then raise exception 'Enter the invoice amount'; end if;
  if exists (select 1 from public.orders where invoice_no = trim(p_invoice_no)) then raise exception 'Invoice % is already on another order', trim(p_invoice_no); end if;
  update public.orders set invoice_no = trim(p_invoice_no), invoice_date = p_invoice_date, invoice_amount = p_amount, invoice_file = p_file,
    invoiced_by = public.order_me_name(), invoiced_at = now(),
    payment_due = case when terms = 'Credit' then p_invoice_date + coalesce(credit_days,30) else null end
  where id = p_order;
  perform public.order_log(p_order, 'Tally invoice entered', trim(p_invoice_no) || ', Rs ' || to_char(p_amount,'FM99,99,99,990') ||
    case when abs(p_amount - o.order_value) > 1 and o.order_value > 0 then ' (order value was Rs ' || to_char(o.order_value,'FM99,99,99,990') || ')' else '' end);
end $$;

-- 3. payment received (office)
create or replace function public.order_add_payment(p_order uuid, p_amount numeric, p_mode text, p_reference text, p_received_on date, p_photo text default null) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders; v_ref text := upper(trim(coalesce(p_reference,'')));
begin
  if not public.is_team() then raise exception 'Only the office team can confirm payments'; end if;
  select * into o from public.orders where id = p_order for update;
  if o.id is null then raise exception 'Order not found'; end if;
  if o.cancelled_at is not null then raise exception 'This order is cancelled'; end if;
  if coalesce(p_amount,0) <= 0 then raise exception 'Enter the amount received'; end if;
  if p_mode is null or p_mode not in ('UPI','Bank transfer','Cheque','Cash','Other') then raise exception 'Choose how it was paid'; end if;
  if length(v_ref) < 4 then raise exception 'Enter the UTR, cheque number or cash receipt number'; end if;
  if p_received_on is null or p_received_on > (now() at time zone 'Asia/Kolkata')::date then raise exception 'Enter a valid date received'; end if;
  if exists (select 1 from public.order_payments where upper(reference) = v_ref and not voided) then raise exception 'Reference % is already recorded on another payment', v_ref; end if;
  insert into public.order_payments(order_id, amount, mode, reference, received_on, photo, recorded_by)
  values (p_order, p_amount, p_mode, v_ref, p_received_on, p_photo, public.order_me_name());
  perform public.order_log(p_order, 'Payment received', 'Rs ' || to_char(p_amount,'FM99,99,99,990') || ' by ' || p_mode || ', ref ' || v_ref || ', received ' || to_char(p_received_on,'DD Mon'));
end $$;

-- 4. dispatch (dispatch desk). Needs invoice, and full payment for Advance orders.
create or replace function public.order_dispatch(p_order uuid, p_mode text, p_transporter text, p_tracking_no text, p_batch_nos text, p_photo text) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders; v_paid numeric;
begin
  if not public.is_team() then raise exception 'Only the office team can dispatch'; end if;
  select * into o from public.orders where id = p_order for update;
  if o.id is null then raise exception 'Order not found'; end if;
  if o.cancelled_at is not null then raise exception 'This order is cancelled'; end if;
  if o.dispatched_at is not null then raise exception 'Already dispatched'; end if;
  if o.invoice_no is null then raise exception 'Enter the Tally invoice before dispatch'; end if;
  v_paid := public.order_paid(p_order);
  if o.terms = 'Advance' and v_paid < o.invoice_amount then
    raise exception 'Advance order: Rs % still to be received before dispatch', to_char(o.invoice_amount - v_paid,'FM99,99,99,990'); end if;
  if coalesce(trim(p_mode),'') = '' then raise exception 'Choose how it is being sent'; end if;
  if coalesce(trim(p_tracking_no),'') = '' then raise exception 'Enter the LR, AWB or vehicle number'; end if;
  if coalesce(p_photo,'') = '' then raise exception 'Add a photo of the LR/courier slip or the loaded goods'; end if;
  update public.orders set dispatched_at = now(), dispatch_mode = left(p_mode,40), transporter = nullif(left(trim(p_transporter),120),''),
    tracking_no = left(trim(p_tracking_no),80), batch_nos = nullif(left(trim(p_batch_nos),200),''), dispatch_photo = p_photo, dispatched_by = public.order_me_name()
  where id = p_order;
  perform public.order_log(p_order, 'Dispatched', p_mode || coalesce(' via ' || nullif(trim(p_transporter),''),'') || ', ' || trim(p_tracking_no) ||
    coalesce(', batch ' || nullif(trim(p_batch_nos),''),''));
end $$;

-- 5. delivery confirmed (office or the field officer of that customer)
create or replace function public.order_deliver(p_order uuid, p_proof text, p_photo text default null, p_note text default null) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders;
begin
  select * into o from public.orders where id = p_order for update;
  if o.id is null or not public.order_visible(o) then raise exception 'Order not found'; end if;
  if o.cancelled_at is not null then raise exception 'This order is cancelled'; end if;
  if o.dispatched_at is null then raise exception 'Not dispatched yet'; end if;
  if o.delivered_at is not null then raise exception 'Delivery already confirmed'; end if;
  if p_proof is null or p_proof not in ('Customer confirmed on WhatsApp','Customer confirmed on call','Signed receipt / photo') then raise exception 'Choose how delivery was confirmed'; end if;
  if p_proof = 'Signed receipt / photo' and coalesce(p_photo,'') = '' then raise exception 'Add the photo'; end if;
  if p_proof <> 'Signed receipt / photo' and coalesce(trim(p_note),'') = '' and coalesce(p_photo,'') = '' then raise exception 'Write what the customer said, or add a screenshot'; end if;
  update public.orders set delivered_at = now(), delivery_proof = p_proof, delivery_photo = p_photo, delivery_note = nullif(left(trim(p_note),500),''), delivered_by = public.order_me_name()
  where id = p_order;
  perform public.order_log(p_order, 'Delivery confirmed', p_proof || coalesce(': ' || nullif(trim(p_note),''),''));
end $$;

-- notes (anyone who can see the order)
create or replace function public.order_note(p_order uuid, p_text text) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders;
begin
  select * into o from public.orders where id = p_order;
  if o.id is null or not public.order_visible(o) then raise exception 'Order not found'; end if;
  if coalesce(trim(p_text),'') = '' then raise exception 'Write the note'; end if;
  perform public.order_log(p_order, 'Note', left(trim(p_text),1000));
end $$;

-- cancel: admin anytime; the creator only before the invoice
create or replace function public.order_cancel(p_order uuid, p_reason text) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders;
begin
  select * into o from public.orders where id = p_order for update;
  if o.id is null or not public.order_visible(o) then raise exception 'Order not found'; end if;
  if o.cancelled_at is not null then raise exception 'Already cancelled'; end if;
  if not public.order_is_admin() and not (o.invoice_no is null and lower(coalesce(o.created_by_email,'')) = public.order_me_email()) then
    raise exception 'Only an admin can cancel an invoiced order'; end if;
  if coalesce(trim(p_reason),'') = '' then raise exception 'Write the reason'; end if;
  update public.orders set cancelled_at = now(), cancelled_by = public.order_me_name(), cancel_reason = left(trim(p_reason),500) where id = p_order;
  perform public.order_log(p_order, 'Cancelled', trim(p_reason));
end $$;

-- admin corrections of recorded steps, always with a reason
create or replace function public.order_correct(p_order uuid, p_field text, p_value text, p_reason text) returns void language plpgsql security definer set search_path = public as $$
declare o public.orders; v_old text;
begin
  if not public.order_is_admin() then raise exception 'Only an admin can correct a recorded step'; end if;
  if coalesce(trim(p_reason),'') = '' then raise exception 'Write the reason for the correction'; end if;
  select * into o from public.orders where id = p_order for update;
  if o.id is null then raise exception 'Order not found'; end if;
  if p_field = 'invoice_no' then v_old := o.invoice_no;
    if exists (select 1 from public.orders where invoice_no = trim(p_value) and id <> p_order) then raise exception 'Invoice % is already on another order', trim(p_value); end if;
    update public.orders set invoice_no = nullif(trim(p_value),'') where id = p_order;
  elsif p_field = 'invoice_amount' then v_old := o.invoice_amount::text; update public.orders set invoice_amount = p_value::numeric where id = p_order;
  elsif p_field = 'invoice_date' then v_old := o.invoice_date::text; update public.orders set invoice_date = p_value::date,
      payment_due = case when terms = 'Credit' then p_value::date + coalesce(credit_days,30) else payment_due end where id = p_order;
  elsif p_field = 'payment_due' then v_old := o.payment_due::text; update public.orders set payment_due = p_value::date where id = p_order;
  elsif p_field = 'tracking_no' then v_old := o.tracking_no; update public.orders set tracking_no = p_value where id = p_order;
  elsif p_field = 'terms' then v_old := o.terms; if p_value not in ('Advance','Credit') then raise exception 'Advance or Credit'; end if;
    update public.orders set terms = p_value, credit_days = case when p_value = 'Credit' then coalesce(credit_days,30) end,
      payment_due = case when p_value = 'Credit' and invoice_date is not null then invoice_date + coalesce(credit_days,30) end where id = p_order;
  elsif p_field = 'undo_dispatch' then v_old := o.tracking_no;
    if o.delivered_at is not null then raise exception 'Undo the delivery first'; end if;
    update public.orders set dispatched_at = null, dispatch_mode = null, transporter = null, tracking_no = null, batch_nos = null, dispatch_photo = null, dispatched_by = null where id = p_order;
  elsif p_field = 'undo_delivery' then v_old := o.delivery_proof;
    update public.orders set delivered_at = null, delivery_proof = null, delivery_photo = null, delivery_note = null, delivered_by = null where id = p_order;
  elsif p_field = 'void_payment' then
    update public.order_payments set voided = true, void_reason = trim(p_reason) where id = p_value::uuid and order_id = p_order and not voided returning reference into v_old;
    if v_old is null then raise exception 'Payment not found'; end if;
  else raise exception 'This field cannot be corrected here'; end if;
  perform public.order_log(p_order, 'Admin correction', p_field || ': ' || coalesce(v_old,'(empty)') || ' -> ' || coalesce(p_value,'(empty)') || '. Reason: ' || trim(p_reason));
end $$;

revoke all on function public.order_create(jsonb), public.order_invoice(uuid,text,date,numeric,text), public.order_add_payment(uuid,numeric,text,text,date,text),
  public.order_dispatch(uuid,text,text,text,text,text), public.order_deliver(uuid,text,text,text), public.order_note(uuid,text),
  public.order_cancel(uuid,text), public.order_correct(uuid,text,text,text), public.order_log(uuid,text,text) from public, anon;
grant execute on function public.order_create(jsonb), public.order_invoice(uuid,text,date,numeric,text), public.order_add_payment(uuid,numeric,text,text,date,text),
  public.order_dispatch(uuid,text,text,text,text,text), public.order_deliver(uuid,text,text,text), public.order_note(uuid,text),
  public.order_cancel(uuid,text), public.order_correct(uuid,text,text,text) to authenticated;
revoke all on function public.order_log(uuid,text,text) from authenticated;
grant select on public.orders_v to authenticated;

-- proof photos: private bucket, team and field officers can upload and view
insert into storage.buckets (id, name, public, file_size_limit, allowed_mime_types)
values ('order-proofs','order-proofs', false, 8388608, array['image/jpeg','image/png','image/webp','image/heic','application/pdf'])
on conflict (id) do nothing;
drop policy if exists "order proofs upload" on storage.objects;
create policy "order proofs upload" on storage.objects for insert to authenticated
  with check (bucket_id = 'order-proofs' and (public.is_team() or public.my_route_key() is not null));
drop policy if exists "order proofs read" on storage.objects;
create policy "order proofs read" on storage.objects for select to authenticated
  using (bucket_id = 'order-proofs' and (public.is_team() or public.my_route_key() is not null));

-- hardening: helpers are not callable without signing in
alter function public.order_me_email() set search_path = public;
revoke execute on function public.order_is_admin(), public.order_me_name(), public.order_paid(uuid), public.order_visible(public.orders), public.order_me_email() from public, anon;
grant execute on function public.order_is_admin(), public.order_me_name(), public.order_paid(uuid), public.order_visible(public.orders), public.order_me_email() to authenticated;

-- hourly stuck-order alerts (edge function source: lead-system/functions/order-alerts.ts)
-- select cron.schedule('gbo-order-alerts', '20 3-14 * * *', $$ select net.http_post(url := 'https://filbmvtclfcrrvxckema.supabase.co/functions/v1/order-alerts', body := '{"mode":"run"}'::jsonb, headers := '{"Content-Type": "application/json"}'::jsonb, timeout_milliseconds := 20000) $$);
