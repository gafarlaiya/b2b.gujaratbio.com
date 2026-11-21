// Gujarat Bio Organics: stuck-order alerts (Supabase Edge Function "order-alerts", deployed; source kept here for reference).
// POST {mode:'run'} (pg_cron job gbo-order-alerts, hourly 8:50 am - 7:50 pm IST): finds orders the view orders_v marks as stuck
// (no invoice 24 h, farmer unpaid 48 h after invoice, ready but not dispatched 24 h, in transit 7 days, credit payment overdue)
// and sends ONE phone push listing them. Each order is repeated at most once a day for the same problem.
import { createClient } from "jsr:@supabase/supabase-js@2";

const db = createClient(Deno.env.get("SUPABASE_URL")!, Deno.env.get("SUPABASE_SERVICE_ROLE_KEY")!);
const TOPIC = Deno.env.get("ORDER_TOPIC") ?? Deno.env.get("NTFY_TOPIC") ?? "gbo-leads-8ce1a43568f8a8c4";
const DASH = "https://gbo.bagban.in/";
const DAY = 24 * 3600e3;
const rs = (n: number) => "Rs " + Math.round(+n || 0).toLocaleString("en-IN");
const json = (o: unknown) => new Response(JSON.stringify(o), { headers: { "Content-Type": "application/json" } });

async function run(force = false) {
  const { data, error } = await db.from("orders_v").select("id,order_no,customer_name,status,stuck,balance,due_amount,created_by,last_alerts").not("stuck", "is", null).limit(200);
  if (error) return json({ error: error.message });
  const now = Date.now();
  const fresh = (data ?? []).filter((o: any) => {
    const last = o.last_alerts?.[o.status];
    return force || !last || now - Date.parse(last) > DAY - 15 * 60e3;
  });
  if (!fresh.length) return json({ stuck: data?.length ?? 0, alerted: 0 });
  const all = data ?? [];
  const money = all.filter((o: any) => /Payment|payment/.test(o.status)).reduce((t: number, o: any) => t + (+o.balance || 0), 0);
  const lines = fresh.slice(0, 12).map((o: any) => `- ${o.order_no} ${o.customer_name} (${rs(o.due_amount)}): ${o.stuck}. Taken by ${o.created_by}`);
  if (fresh.length > 12) lines.push(`...and ${fresh.length - 12} more`);
  const body = lines.join("\n") + `\n\nAll stuck orders: ${all.length}` + (money ? `, money waiting ${rs(money)}` : "") + `\nOpen the dashboard, Orders, Stuck.`;
  const r = await fetch(`https://ntfy.sh/`, {
    method: "POST", headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ topic: TOPIC, title: `[Orders] ${fresh.length} order${fresh.length > 1 ? "s" : ""} stuck`, message: body, tags: ["package", "warning"], priority: 4, click: DASH }),
  }).catch((e) => { console.error("ntfy", e); return null; });
  if (!r || !r.ok) return json({ error: "push failed", status: r?.status });
  const stamp = new Date().toISOString();
  for (const o of fresh as any[]) {
    await db.from("orders").update({ last_alerts: { ...(o.last_alerts ?? {}), [o.status]: stamp } }).eq("id", o.id);
  }
  return json({ stuck: all.length, alerted: fresh.length });
}

Deno.serve(async (req) => {
  if (req.method !== "POST") return new Response("method", { status: 405 });
  let b: any = {};
  try { b = await req.json(); } catch { return new Response("bad json", { status: 400 }); }
  if (b.mode === "run") return await run(false);
  return new Response("bad request", { status: 400 });
});
