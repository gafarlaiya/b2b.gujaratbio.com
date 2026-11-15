/* GBO team dashboard: Orders.
   One record per order, from won lead to money received. Every step goes through a database function
   that checks the rules (invoice before dispatch, farmer pays before dispatch, proof photo, unique UTR)
   and stamps the name and time. Loaded by team/index.html, which provides window.GBO helpers. */
(function(){
var G=window.GBO, $=G.$, esc=G.esc, api=G.api, toast=G.toast, IC=G.IC;
var O={list:[],items:[],pays:[],events:{},st:'open',q:'',who:'',limit:60,urls:{}};
G.O=O;
var PRODUCTS=['Immunity Sugarcane Special','Immunity Granules','Immunity Gold','Immunity Mango Special','Immunity Apple Special','Immunity Potato Special','Immunity Banana Special','Immunity NPK Liquid','Humic acid granules','Seaweed extract','Amino acid'];
var PACKS=['250 ml','500 ml','1 L','5 L','500 g','1 kg','2 kg','4 kg','8 kg','25 kg','50 kg'];
var MODES=['UPI','Bank transfer','Cheque','Cash','Other'];
var SEND=['Courier','Transport','Own vehicle','Customer pickup'];
var PROOF=['Customer confirmed on WhatsApp','Customer confirmed on call','Signed receipt / photo'];
var STATUS=['Awaiting invoice','Awaiting payment','Ready to dispatch','In transit','Payment due','Closed','Cancelled'];
var OPEN=['Awaiting invoice','Awaiting payment','Ready to dispatch','In transit','Payment due'];

function rs(n){n=+n||0;return 'Rs '+Math.round(n).toLocaleString('en-IN')}
function today(){return G.dkey(new Date())}
function isTeam(){return !G.S.partner}
function isAdmin(){var em=(G.ls('gbo_em')||'').toLowerCase();var t=G.S.team.find(function(x){return (x.email||'').toLowerCase()===em});return !!(t&&t.role==='admin')}
function rpc(fn,body){return api('rpc/'+fn,{method:'POST',body:body})}
function stCls(s){return s==='Closed'?'':s==='Cancelled'?'grey':s==='Payment due'||s==='Awaiting payment'?'amber':'blue'}

/* ---- data ---- */
O.load=async function(){
  var r=await Promise.all([api('orders_v?select=*&order=created_at.desc&limit=1000'),api('order_items?select=*&limit=5000'),api('order_payments?select=*&order=received_on.desc&limit=5000')]);
  O.list=r[0]||[];O.items=r[1]||[];O.pays=r[2]||[];
};
O.stuckCount=function(){return O.list.filter(function(o){return o.stuck}).length};
function itemsOf(id){return O.items.filter(function(i){return i.order_id===id})}
function paysOf(id){return O.pays.filter(function(p){return p.order_id===id})}
function byLead(lid){return O.list.filter(function(o){return o.lead_id===lid&&o.status!=='Cancelled'})}
O.byLead=byLead;

/* ---- photos: shrink on the phone, upload to the private bucket, view with a short-lived link ---- */
function shrink(file){
  return new Promise(function(res){
    if(!/^image\//.test(file.type)||/heic/i.test(file.type)){res(file);return}
    var img=new Image(),u=URL.createObjectURL(file);
    img.onload=function(){var m=1600,w=img.width,h=img.height,k=Math.min(1,m/Math.max(w,h));var c=document.createElement('canvas');c.width=Math.round(w*k);c.height=Math.round(h*k);c.getContext('2d').drawImage(img,0,0,c.width,c.height);URL.revokeObjectURL(u);c.toBlob(function(b){res(b||file)},'image/jpeg',.78)};
    img.onerror=function(){URL.revokeObjectURL(u);res(file)};img.src=u;
  });
}
async function upload(orderId,kind,inputId){
  var inp=$(inputId);if(!inp||!inp.files||!inp.files[0])return null;
  var f=inp.files[0],b=await shrink(f),ext=b.type==='application/pdf'?'pdf':/png/.test(b.type)?'png':'jpg';
  var path=orderId+'/'+kind+'-'+Date.now()+'.'+ext;
  async function go(){return fetch(G.SB+'/storage/v1/object/order-proofs/'+path,{method:'POST',headers:{apikey:G.KEY,Authorization:'Bearer '+G.tok(),'Content-Type':b.type||'image/jpeg','x-upsert':'false'},body:b})}
  var r=await go();if(r.status===401||r.status===400&&/jwt/i.test(await r.clone().text())){await G.refresh();r=await go()}
  if(!r.ok){var t=await r.text();throw new Error('Photo not uploaded: '+(t.slice(0,120)||r.status))}
  return path;
}
async function signed(path){
  if(!path)return null;if(O.urls[path]&&O.urls[path].t>Date.now())return O.urls[path].u;
  var r=await fetch(G.SB+'/storage/v1/object/sign/order-proofs/'+path,{method:'POST',headers:{apikey:G.KEY,Authorization:'Bearer '+G.tok(),'Content-Type':'application/json'},body:JSON.stringify({expiresIn:3600})});
  var j=await r.json().catch(function(){return {}});if(!r.ok||!j.signedURL)return null;
  var u=G.SB+'/storage/v1'+j.signedURL;O.urls[path]={u:u,t:Date.now()+50*60e3};return u;
}
function photoLink(path,label){return path?'<a href="#" class="tag blue" data-photo="'+esc(path)+'">'+esc(label||'View photo')+'</a>':''}
function bindPhotos(root){root.querySelectorAll('[data-photo]').forEach(function(a){a.onclick=async function(e){e.preventDefault();var w=window.open('','_blank');var u=await signed(a.dataset.photo);if(u){if(w)w.location=u;else location.href=u}else{if(w)w.close();toast('Could not open the photo')}}})}
function fileField(id,label,req){return '<div class="full"><label for="'+id+'">'+label+(req?' (required)':' (optional)')+'</label><input id="'+id+'" type="file" accept="image/*,application/pdf" capture="environment"></div>'}

/* ---- list (owner view) ---- */
function rows(){
  var q=O.q.toLowerCase();
  return O.list.filter(function(o){
    if(O.st==='open'){if(OPEN.indexOf(o.status)<0)return false}else if(O.st==='stuck'){if(!o.stuck)return false}else if(O.st&&o.status!==O.st)return false;
    if(O.who&&o.created_by!==O.who)return false;
    if(q){var h=[o.order_no,o.customer_name,o.phone,o.invoice_no,o.tracking_no,o.district,o.created_by,itemsOf(o.id).map(function(i){return i.product}).join(' ')].join(' ').toLowerCase();if(h.indexOf(q)<0)return false}
    return true});
}
function dots(o){
  var paidOk=+o.paid>=+o.due_amount-0.5;
  var s=[['Order',1],['Invoice',!!o.invoice_no],['Paid',paidOk],['Sent',!!o.dispatched_at],['Delivered',!!o.delivered_at]];
  return '<div class="odots">'+s.map(function(x){return '<span class="'+(x[1]?'on':'')+'">'+x[0]+'</span>'}).join('')+'</div>';
}
function ocard(o){
  var it=itemsOf(o.id).map(function(i){return i.product+(i.pack?' '+i.pack:'')+' x'+(+i.qty)}).join(', ');
  var tags='<span class="tag '+stCls(o.status)+'">'+esc(o.status)+'</span>'+(o.customer_type==='B2B'?'<span class="tag" style="background:#fff3d6;color:#8a5a00">B2B '+esc(o.terms)+'</span>':'');
  if(o.stuck)tags+='<span class="tag red">'+esc(o.stuck)+'</span>';
  tags+='<span class="tag grey">'+esc(o.created_by)+'</span>';
  return '<article class="lc'+(o.stuck?' Hot':'')+'" data-o="'+o.id+'"'+(G.S.sel===o.id?' aria-current="true"':'')+' tabindex="0"><span class="bar"></span><div class="main"><div class="t"><b>'+esc(o.customer_name)+'</b><span class="when">'+esc(rs(o.due_amount))+'</span></div>'
   +'<div class="s">'+esc(o.order_no+(o.invoice_no?' | Inv '+o.invoice_no:'')+' | '+it)+'</div>'
   +(o.next_step?'<div class="s" style="color:var(--ink)">Next: '+esc(o.next_step)+'</div>':'')
   +dots(o)+'<div class="m">'+tags+'</div></div></article>';
}
G.vOrders=function(){
  var L=O.list,open=L.filter(function(o){return OPEN.indexOf(o.status)>=0});
  function sum(a,f){return a.reduce(function(t,o){return t+(+f(o)||0)},0)}
  var stuck=L.filter(function(o){return o.stuck});
  var awaitPay=L.filter(function(o){return o.status==='Awaiting payment'});
  var due=L.filter(function(o){return o.status==='Payment due'||o.status==='In transit'&&+o.balance>0});
  var over=L.filter(function(o){return o.status==='Payment due'&&o.stuck});
  var m0=new Date();m0.setDate(1);m0.setHours(0,0,0,0);
  var month=L.filter(function(o){return o.status!=='Cancelled'&&new Date(o.created_at)>=m0});
  var cash=O.pays.filter(function(p){return !p.voided&&new Date(p.received_on)>=m0});
  var k=[['Stuck, needs action',stuck.length,stuck.length?'alert':'','stuck'],['Open orders',open.length,'','open'],
    ['Waiting for Tally invoice',L.filter(function(o){return o.status==='Awaiting invoice'}).length,'','Awaiting invoice'],
    ['Farmer payment awaited',rs(sum(awaitPay,function(o){return o.balance})),'','Awaiting payment'],
    ['Ready to dispatch',L.filter(function(o){return o.status==='Ready to dispatch'}).length,'','Ready to dispatch'],
    ['In transit',L.filter(function(o){return o.status==='In transit'}).length,'','In transit'],
    ['To collect (credit)',rs(sum(due,function(o){return o.balance})),'','Payment due'],
    ['Overdue payments',rs(sum(over,function(o){return o.balance})),over.length?'alert':'','Payment due'],
    ['Orders this month',month.length+' | '+rs(sum(month,function(o){return o.due_amount})),'',''],
    ['Money received this month',rs(sum(cash,function(p){return p.amount})),'','']];
  var people=Object.keys(L.reduce(function(m,o){m[o.created_by]=1;return m},{})).sort();
  var cnt={};L.forEach(function(o){cnt[o.status]=(cnt[o.status]||0)+1});
  var chips=[['open','Open',open.length],['stuck','Stuck',stuck.length]].concat(STATUS.filter(function(s){return cnt[s]}).map(function(s){return [s,s,cnt[s]]})).concat([['','All',L.length]]);
  $('pane').innerHTML=(isTeam()?'<div class="kpis okpis">'+k.map(function(x){return '<button class="kpi '+(x[2]||'')+'" data-k="'+esc(x[3])+'"><b>'+x[1]+'</b><small>'+x[0]+'</small></button>'}).join('')+'</div>':'')
   +'<div class="tool" style="margin-top:.6rem"><div style="display:flex;gap:.5rem"><label class="search" style="flex:1"><span class="sr">Search orders</span>'+IC.search+'<input type="search" id="oq" placeholder="Search customer, order, invoice, LR" value="'+esc(O.q)+'" autocomplete="off"></label><button class="btn pri" id="onew">+ New order</button></div>'
   +'<div class="chips" role="group" aria-label="Status">'+chips.map(function(c){return '<button class="chip" data-s="'+esc(c[0])+'" aria-pressed="'+(O.st===c[0])+'">'+esc(c[1])+'<b>'+c[2]+'</b></button>'}).join('')+'</div>'
   +(people.length>1?'<div class="selrow"><select id="owho" aria-label="Taken by"><option value="">Taken by anyone</option>'+people.map(function(p){return '<option'+(O.who===p?' selected':'')+'>'+esc(p)+'</option>'}).join('')+'</select></div>':'')
   +'</div><div id="ol"></div>';
  $('oq').oninput=function(){O.q=this.value;O.limit=60;drawList()};
  $('onew').onclick=function(){newOrder(null)};
  var w=$('owho');if(w)w.onchange=function(){O.who=this.value;drawList()};
  $('pane').querySelectorAll('.chip').forEach(function(c){c.onclick=function(){O.st=c.dataset.s;O.limit=60;$('pane').querySelectorAll('.chip').forEach(function(x){x.setAttribute('aria-pressed',String(x===c))});drawList()}});
  $('pane').querySelectorAll('.okpis .kpi').forEach(function(b){b.onclick=function(){if(!b.dataset.k)return;O.st=b.dataset.k;G.render()}});
  drawList();
};
function drawList(){
  var r=rows(),box=$('ol');if(!box)return;
  if(!r.length){box.innerHTML='<div class="empty">'+(O.list.length?'<b>No orders here</b>Try another filter.':'<b>No orders yet</b>Tap "+ New order", or open a lead and tap "Create order".')+'</div>';return}
  box.innerHTML='<div class="sec"><span class="n">'+r.length+' order'+(r.length>1?'s':'')+', newest first</span></div><div class="list">'+r.slice(0,O.limit).map(ocard).join('')+'</div>'+(r.length>O.limit?'<button class="btn more" id="omore">Show more</button>':'');
  box.querySelectorAll('[data-o]').forEach(function(c){c.onclick=function(){openOrder(c.dataset.o)};c.onkeydown=function(e){if(e.key==='Enter')openOrder(c.dataset.o)}});
  var m=$('omore');if(m)m.onclick=function(){O.limit+=60;drawList()};
}

/* ---- new order ---- */
function itemRow(i,v){v=v||{};return '<div class="oitem" data-i="'+i+'"><input class="it_p" list="dl_prod" placeholder="Product" value="'+esc(v.product||'')+'"><input class="it_k" list="dl_pack" placeholder="Pack" value="'+esc(v.pack||'')+'"><input class="it_q" type="number" min="0" step="any" inputmode="decimal" placeholder="Qty" value="'+esc(v.qty||'')+'"><input class="it_r" type="number" min="0" step="any" inputmode="decimal" placeholder="Rate Rs" value="'+esc(v.rate||'')+'"><button class="iconbtn it_x" aria-label="Remove">'+IC.x+'</button></div>'}
function newOrder(lead){
  G.S.sel=null;G.setCur({type:'neworder',id:lead?lead.id:null});
  var l=lead||{},b2b=lead?G.isB2B(lead):false;
  var addr=[l.village,l.taluka,l.district,l.state].filter(Boolean).join(', ');
  G.sheetOpen(G.head('New order',lead?esc('For lead '+(l.lead_no||'')):'Customer not in leads')
   +'<div class="sh-body"><div class="box"><h3>Customer</h3><div class="seg" id="n_type"><button data-v="Farmer" aria-pressed="'+(!b2b)+'">Farmer</button><button data-v="B2B" aria-pressed="'+b2b+'">B2B (dealer, distributor, company)</button></div>'
   +'<div class="f" style="margin-top:.7rem"><div><label for="n_name">Name</label><input id="n_name" value="'+esc(l.name||l.company||'')+'"></div><div><label for="n_ph">Phone</label><input id="n_ph" inputmode="tel" value="'+esc(G.digits(l.phone).replace(/^91(?=\d{10}$)/,''))+'"></div>'
   +'<div class="full"><label for="n_addr">Delivery address</label><textarea id="n_addr" rows="2">'+esc(addr)+'</textarea></div>'
   +'<div><label for="n_dis">District</label><input id="n_dis" value="'+esc(l.district||'')+'"></div><div><label for="n_st">State</label><input id="n_st" value="'+esc(l.state||'Gujarat')+'"></div>'
   +'<div class="b2bonly full"><label for="n_gst">GST number</label><input id="n_gst" value=""></div>'
   +'<div class="b2bonly"><label for="n_terms">Payment</label><select id="n_terms"><option>Credit</option><option>Advance</option></select></div><div class="b2bonly"><label for="n_days">Credit days</label><input id="n_days" type="number" min="0" max="180" value="30"></div>'
   +'<div class="full farmonly" style="font-size:.85rem;color:var(--mut)">Farmer orders are paid in advance. Dispatch is blocked until the full amount is received.</div></div></div>'
   +'<div class="box"><h3>Products</h3><div id="n_items">'+itemRow(0)+'</div><button class="btn" id="n_add" style="margin-top:.5rem">+ Add product</button>'
   +'<datalist id="dl_prod">'+PRODUCTS.map(function(p){return '<option value="'+esc(p)+'">'}).join('')+'</datalist><datalist id="dl_pack">'+PACKS.map(function(p){return '<option value="'+esc(p)+'">'}).join('')+'</datalist>'
   +'<div class="ototal">Order value: <b id="n_total">Rs 0</b></div></div>'
   +'<div class="box"><h3>Note for the office (optional)</h3><textarea class="note" id="n_note" placeholder="e.g. deliver before Monday, farmer pays by UPI tomorrow"></textarea></div>'
   +'<div class="err" id="n_err" role="alert"></div><div class="acts2"><button class="btn pri" id="n_ok" style="flex:1;min-height:48px">Create order</button></div></div>');
  function type(){var b=document.querySelector('#n_type button[aria-pressed="true"]');return b?b.dataset.v:'Farmer'}
  function sync(){var t=type();document.querySelectorAll('.b2bonly').forEach(function(e){e.classList.toggle('hide',t!=='B2B')});document.querySelectorAll('.farmonly').forEach(function(e){e.classList.toggle('hide',t==='B2B')})}
  function items(){return Array.prototype.map.call(document.querySelectorAll('#n_items .oitem'),function(r){return {product:r.querySelector('.it_p').value.trim(),pack:r.querySelector('.it_k').value.trim(),qty:r.querySelector('.it_q').value,rate:r.querySelector('.it_r').value}}).filter(function(x){return x.product||x.qty})}
  function total(){var t=items().reduce(function(s,x){return s+(+x.qty||0)*(+x.rate||0)},0);$('n_total').textContent=rs(t)}
  function bindItems(){document.querySelectorAll('#n_items input').forEach(function(i){i.oninput=total});document.querySelectorAll('#n_items .it_x').forEach(function(b){b.onclick=function(){var r=b.closest('.oitem');if(document.querySelectorAll('#n_items .oitem').length>1)r.remove();else r.querySelectorAll('input').forEach(function(i){i.value=''});total()}})}
  document.querySelectorAll('#n_type button').forEach(function(b){b.onclick=function(){document.querySelectorAll('#n_type button').forEach(function(x){x.setAttribute('aria-pressed',String(x===b))});sync()}});
  $('n_add').onclick=function(){$('n_items').insertAdjacentHTML('beforeend',itemRow(Date.now()));bindItems()};
  bindItems();sync();
  $('n_ok').onclick=async function(){
    var it=items();$('n_err').textContent='';
    if(!it.length){$('n_err').textContent='Add at least one product.';return}
    if(it.some(function(x){return !x.product||!(+x.qty>0)})){$('n_err').textContent='Each product needs a name and a quantity.';return}
    if(it.some(function(x){return !(+x.rate>0)})&&!confirm('Some products have no rate. Create the order anyway? The office will use the Tally invoice amount.'))return;
    this.disabled=true;
    try{
      var t=type(),p={customer_type:t,customer_name:$('n_name').value.trim(),phone:$('n_ph').value.trim(),address:$('n_addr').value.trim(),district:$('n_dis').value.trim(),state:$('n_st').value.trim(),notes:$('n_note').value.trim(),items:it};
      if(lead)p.lead_id=lead.id;
      if(t==='B2B'){p.gst_no=$('n_gst').value.trim();p.terms=$('n_terms').value;p.credit_days=$('n_days').value}
      var id=await rpc('order_create',{p:p});
      await O.load();if(lead){lead.stage='Won';lead.next_followup=null}
      toast('Order created');G.S.tab='orders';O.st='open';G.render();openOrder(id);
      G.load('bg').catch(function(){});
    }catch(e){this.disabled=false;$('n_err').textContent=e.message}
  };
}
G.newOrder=newOrder;

/* ---- one order: steps, the next action, proof, history ---- */
function step(name,done,line,sub){return '<li class="'+(done?'done':'')+'"><b>'+name+'</b>'+(line?'<span>'+line+'</span>':'')+(sub?'<small>'+sub+'</small>':'')+'</li>'}
async function openOrder(id,keep){
  var o=O.list.find(function(x){return x.id===id});if(!o)return;
  G.S.sel=id;G.setCur({type:'order',id:id});
  document.querySelectorAll('.lc').forEach(function(c){if(c.dataset.o===id)c.setAttribute('aria-current','true');else c.removeAttribute('aria-current')});
  var it=itemsOf(id),py=paysOf(id),team=isTeam(),adm=isAdmin();
  var paidOk=+o.paid>=+o.due_amount-0.5,ph=G.digits(o.phone);
  var steps='<ol class="osteps">'
   +step('Order taken',1,esc(G.fdt(o.created_at)+' by '+o.created_by),esc(o.customer_type+', '+o.terms+(o.credit_days!=null?' '+o.credit_days+' days':'')))
   +step('Tally invoice',!!o.invoice_no,o.invoice_no?esc(o.invoice_no+', '+rs(o.invoice_amount)+', '+G.fd(o.invoice_date)):'',o.invoiced_by?esc('entered by '+o.invoiced_by+' '+G.fdt(o.invoiced_at)):'')
   +step('Payment',paidOk,esc(rs(o.paid)+' received of '+rs(o.due_amount)),o.terms==='Credit'&&o.payment_due?esc('due by '+G.fd(o.payment_due)):(o.terms==='Advance'&&!paidOk?'must be paid before dispatch':''))
   +step('Dispatched',!!o.dispatched_at,o.dispatched_at?esc(o.dispatch_mode+(o.transporter?' via '+o.transporter:'')+', '+o.tracking_no):'',o.dispatched_by?esc('by '+o.dispatched_by+' '+G.fdt(o.dispatched_at)+(o.batch_nos?', batch '+o.batch_nos:'')):'')
   +step('Delivered',!!o.delivered_at,o.delivered_at?esc(o.delivery_proof):'',o.delivered_by?esc('by '+o.delivered_by+' '+G.fdt(o.delivered_at)+(o.delivery_note?': '+o.delivery_note:'')):'')
   +'</ol>';
  var photos=[photoLink(o.invoice_file,'Invoice'),photoLink(o.dispatch_photo,'Dispatch slip'),photoLink(o.delivery_photo,'Delivery proof')].concat(py.map(function(p){return photoLink(p.photo,'Payment '+p.reference)})).filter(Boolean).join(' ');
  var act='';
  if(o.status!=='Cancelled'&&o.status!=='Closed'){
    if(!o.invoice_no){
      act+=team?'<div class="box obox"><h3>Next: enter the Tally invoice</h3><div class="f"><div><label for="a_inv">Tally invoice no.</label><input id="a_inv"></div><div><label for="a_dt">Invoice date</label><input id="a_dt" type="date" value="'+today()+'" max="'+today()+'"></div>'
        +'<div class="full"><label for="a_amt">Invoice amount (Rs, with GST)</label><input id="a_amt" type="number" min="1" step="any" inputmode="decimal" value="'+(+o.order_value||'')+'"></div>'+fileField('a_f','Photo or PDF of the invoice',false)+'</div>'
        +'<div class="err" id="a_err"></div><button class="btn pri" id="a_ok">Save invoice</button></div>':'<div class="box obox"><h3>Waiting for the office</h3>The office will enter the Tally invoice.</div>';
    }
    if(o.invoice_no&&+o.balance>0.5&&team){
      act+='<div class="box obox"><h3>'+(o.terms==='Advance'&&!o.dispatched_at?'Next: confirm the advance payment':'Record a payment received')+'</h3><div style="font-size:.88rem;margin-bottom:.5rem">Still to receive: <b>'+rs(o.balance)+'</b>. Check the bank or UPI app before saving.</div><div class="f">'
        +'<div><label for="p_amt">Amount received (Rs)</label><input id="p_amt" type="number" min="1" step="any" inputmode="decimal" value="'+Math.round(o.balance)+'"></div><div><label for="p_mode">Paid by</label><select id="p_mode">'+MODES.map(function(m){return '<option>'+m+'</option>'}).join('')+'</select></div>'
        +'<div><label for="p_ref">UTR / cheque / receipt no.</label><input id="p_ref" autocomplete="off"></div><div><label for="p_dt">Date received</label><input id="p_dt" type="date" value="'+today()+'" max="'+today()+'"></div>'+fileField('p_f','Payment screenshot',false)+'</div>'
        +'<div class="err" id="p_err"></div><button class="btn pri" id="p_ok">Save payment</button></div>';
    }
    if(o.status==='Ready to dispatch'){
      act+=team?'<div class="box obox"><h3>Next: dispatch</h3><div class="f"><div><label for="d_mode">Sent by</label><select id="d_mode">'+SEND.map(function(m){return '<option>'+m+'</option>'}).join('')+'</select></div><div><label for="d_tr">Courier / transport name</label><input id="d_tr"></div>'
        +'<div><label for="d_no">LR / AWB / vehicle no.</label><input id="d_no" autocomplete="off"></div><div><label for="d_b">Batch no(s)</label><input id="d_b" placeholder="from the pack label"></div>'+fileField('d_f','Photo of the LR / courier slip or loaded goods',true)+'</div>'
        +'<div class="err" id="d_err"></div><button class="btn pri" id="d_ok">Mark dispatched</button></div>':'<div class="box obox"><h3>Waiting for dispatch</h3>The office will send it and add the tracking number.</div>';
    }else if(o.status==='Awaiting payment'&&!team){act+='<div class="box obox"><h3>Waiting for payment</h3>Dispatch starts once the office confirms '+rs(o.balance)+' is received.</div>'}
    if(o.dispatched_at&&!o.delivered_at){
      act+='<div class="box obox"><h3>Next: confirm delivery</h3><div class="f"><div class="full"><label for="v_pr">How was it confirmed?</label><select id="v_pr">'+PROOF.map(function(m){return '<option>'+m+'</option>'}).join('')+'</select></div>'
        +'<div class="full"><label for="v_n">What did the customer say?</label><input id="v_n" placeholder="e.g. received 2 bottles in good condition"></div>'+fileField('v_f','Photo or WhatsApp screenshot',false)+'</div>'
        +'<div class="err" id="v_err"></div><button class="btn pri" id="v_ok">Confirm delivery</button></div>';
    }
  }
  var msgs='';
  if(ph&&o.dispatched_at){
    var guj=o.customer_type==='Farmer'&&/gujarat/i.test(o.state||'Gujarat');
    var t1=guj?'નમસ્તે '+o.customer_name+', આપનો ઓર્ડર '+o.order_no+' મોકલી દીધો છે. '+o.dispatch_mode+(o.transporter?' ('+o.transporter+')':'')+', નંબર: '+o.tracking_no+'. માલ મળે એટલે અમને જરૂર જણાવજો. ગુજરાત બાયો ઓર્ગેનિક્સ, 99787 91167'
      :'Hello '+o.customer_name+', your order '+o.order_no+(o.invoice_no?' (invoice '+o.invoice_no+')':'')+' has been dispatched by '+o.dispatch_mode+(o.transporter?' - '+o.transporter:'')+'. Tracking / LR no: '+o.tracking_no+'. Please let us know when it reaches you. Gujarat Bio Organics, +91 99787 91167';
    msgs+='<a class="btn wa" target="_blank" rel="noopener" href="https://wa.me/'+G.waNum(o.phone)+'?text='+encodeURIComponent(t1)+'">'+IC.wa+'Send tracking</a>';
  }
  if(ph&&+o.balance>0.5&&o.invoice_no){
    var t2='Hello '+o.customer_name+', payment of '+rs(o.balance)+' for order '+o.order_no+' (invoice '+o.invoice_no+')'+(o.payment_due?' is due by '+G.fd(o.payment_due):' is pending')+'. Please share the UTR after payment. Gujarat Bio Organics, +91 99787 91167';
    msgs+='<a class="btn" target="_blank" rel="noopener" href="https://wa.me/'+G.waNum(o.phone)+'?text='+encodeURIComponent(t2)+'">Payment reminder</a>';
  }
  var h=G.head(o.customer_name,esc([o.order_no,o.status].join(', ')))
   +'<div class="sh-body">'
   +(ph?'<div class="callbar"><a class="btn pri" href="tel:+'+G.waNum(o.phone)+'">'+IC.phone+'Call</a><a class="btn wa" target="_blank" rel="noopener" href="https://wa.me/'+G.waNum(o.phone)+'">'+IC.wa+'WhatsApp</a></div>':'')
   +(o.stuck?'<div class="box" style="border-color:#f0c4bd;background:var(--hots)"><b class="missed">Stuck: '+esc(o.stuck)+'</b></div>':'')
   +(o.cancelled_at?'<div class="box" style="background:#eef1ef"><b>Cancelled</b> by '+esc(o.cancelled_by)+', '+esc(G.fdt(o.cancelled_at))+': '+esc(o.cancel_reason)+'</div>':'')
   +'<div class="box"><h3>Progress</h3>'+steps+(photos?'<div class="m" style="display:flex;flex-wrap:wrap;gap:.35rem;margin-top:.6rem">'+photos+'</div>':'')+(msgs?'<div class="acts2" style="margin-top:.7rem">'+msgs+'</div>':'')+'</div>'
   +act
   +'<div class="box"><h3>Products<span class="r">'+esc(rs(o.order_value))+'</span></h3><table class="otab"><tbody>'+it.map(function(i){return '<tr><td>'+esc(i.product)+(i.pack?' <small>'+esc(i.pack)+'</small>':'')+'</td><td>'+(+i.qty)+'</td><td>'+(+i.rate?esc(rs(i.amount)):'-')+'</td></tr>'}).join('')+'</tbody></table>'
     +G.facts([['Address',o.address],['District',[o.district,o.state].filter(Boolean).join(', ')],['GST',o.gst_no],['Note',o.notes]])
     +(o.lead_id&&G.S.leads.some(function(l){return l.id===o.lead_id})?'<div class="acts2" style="margin-top:.5rem"><button class="btn" id="o_lead">Open lead</button></div>':'')+'</div>'
   +(py.length?'<div class="box"><h3>Payments</h3><ul class="calls">'+py.map(function(p){return '<li'+(p.voided?' style="text-decoration:line-through;color:var(--faint)"':'')+'><b>'+esc(rs(p.amount))+'</b> '+esc(p.mode)+', ref '+esc(p.reference)+', '+esc(G.fd(p.received_on))+'<br><small style="color:var(--mut)">recorded by '+esc(p.recorded_by)+(p.voided?', voided: '+esc(p.void_reason):'')+'</small>'+(adm&&!p.voided?' <button class="btn ghost" data-void="'+p.id+'" style="min-height:30px;padding:.1rem .4rem;color:var(--hot)">Void</button>':'')+'</li>'}).join('')+'</ul></div>':'')
   +'<div class="box"><h3>History</h3><div id="o_hist" class="notes" style="margin-top:0">Loading...</div><div class="inline"><input id="o_note" placeholder="Add a note (what happened, what is next)"><button class="btn" id="o_addn">Add</button></div></div>'
   +((adm||(!o.invoice_no&&o.status!=='Cancelled'))&&o.status!=='Cancelled'?'<details class="box"><summary>'+(adm?'Correct or cancel (admin)':'Cancel this order')+'</summary>'
     +(adm?'<div class="f"><div><label for="c_f">What to correct</label><select id="c_f"><option value="invoice_no">Invoice no.</option><option value="invoice_amount">Invoice amount</option><option value="invoice_date">Invoice date (YYYY-MM-DD)</option><option value="payment_due">Payment due date (YYYY-MM-DD)</option><option value="tracking_no">LR / AWB no.</option><option value="terms">Terms (Advance or Credit)</option><option value="undo_dispatch">Undo dispatch</option><option value="undo_delivery">Undo delivery</option></select></div><div><label for="c_v">New value</label><input id="c_v"></div><div class="full"><label for="c_r">Reason (kept in history)</label><input id="c_r"></div></div><div class="acts2" style="margin-top:.5rem"><button class="btn" id="c_ok">Save correction</button></div><hr style="border:0;border-top:1px solid var(--line);margin:.8rem 0">':'')
     +'<div class="inline"><input id="x_r" placeholder="Reason for cancelling"><button class="btn" id="x_ok" style="color:var(--hot)">Cancel order</button></div></details>':'')
   +'</div>';
  G.sheetOpen(h);if(!keep)$('sheet').scrollTop=0;
  bindPhotos($('sheet'));
  loadHist(id);
  var ol=$('o_lead');if(ol)ol.onclick=function(){G.S.tab='leads';G.render();G.openLead(o.lead_id)};
  function wire(btn,errId,fn){var b=$(btn);if(!b)return;b.onclick=async function(){$(errId).textContent='';b.disabled=true;try{await fn();await refreshOrder(id)}catch(e){$(errId).textContent=e.message;b.disabled=false}}}
  wire('a_ok','a_err',async function(){var amt=+$('a_amt').value;if(!$('a_inv').value.trim())throw new Error('Enter the Tally invoice number');if(!(amt>0))throw new Error('Enter the invoice amount');
    if(+o.order_value>0&&Math.abs(amt-o.order_value)>1&&!confirm('Invoice amount '+rs(amt)+' is different from the order value '+rs(o.order_value)+'. Save anyway?'))throw new Error('Not saved');
    var f=await upload(id,'invoice','a_f');await rpc('order_invoice',{p_order:id,p_invoice_no:$('a_inv').value.trim(),p_invoice_date:$('a_dt').value,p_amount:amt,p_file:f});toast('Invoice saved')});
  wire('p_ok','p_err',async function(){var amt=+$('p_amt').value;if(!(amt>0))throw new Error('Enter the amount');if($('p_ref').value.trim().length<4)throw new Error('Enter the UTR, cheque or receipt number');
    if(amt>+o.balance+1&&!confirm(rs(amt)+' is more than the '+rs(o.balance)+' still due. Save anyway?'))throw new Error('Not saved');
    var f=await upload(id,'payment','p_f');await rpc('order_add_payment',{p_order:id,p_amount:amt,p_mode:$('p_mode').value,p_reference:$('p_ref').value.trim(),p_received_on:$('p_dt').value,p_photo:f});toast('Payment saved')});
  wire('d_ok','d_err',async function(){if(!$('d_no').value.trim())throw new Error('Enter the LR, AWB or vehicle number');if(!$('d_f').files.length)throw new Error('Add the photo of the slip or loaded goods');
    var f=await upload(id,'dispatch','d_f');await rpc('order_dispatch',{p_order:id,p_mode:$('d_mode').value,p_transporter:$('d_tr').value.trim(),p_tracking_no:$('d_no').value.trim(),p_batch_nos:$('d_b').value.trim(),p_photo:f});toast('Dispatched. Now send the tracking on WhatsApp.')});
  wire('v_ok','v_err',async function(){var pr=$('v_pr').value;if(pr==='Signed receipt / photo'&&!$('v_f').files.length)throw new Error('Add the photo');if(pr!=='Signed receipt / photo'&&!$('v_n').value.trim()&&!$('v_f').files.length)throw new Error('Write what the customer said, or add a screenshot');
    var f=await upload(id,'delivery','v_f');await rpc('order_deliver',{p_order:id,p_proof:pr,p_photo:f,p_note:$('v_n').value.trim()});toast('Delivery confirmed')});
  var an=$('o_addn');if(an)an.onclick=async function(){var t=$('o_note').value.trim();if(!t)return;an.disabled=true;try{await rpc('order_note',{p_order:id,p_text:t});$('o_note').value='';delete O.events[id];loadHist(id);toast('Note added')}catch(e){toast(e.message)}finally{an.disabled=false}};
  var co=$('c_ok');if(co)co.onclick=async function(){try{await rpc('order_correct',{p_order:id,p_field:$('c_f').value,p_value:$('c_v').value.trim()||null,p_reason:$('c_r').value.trim()});toast('Corrected');await refreshOrder(id)}catch(e){toast(e.message)}};
  var xo=$('x_ok');if(xo)xo.onclick=async function(){if(!confirm('Cancel order '+o.order_no+'?'))return;try{await rpc('order_cancel',{p_order:id,p_reason:$('x_r').value.trim()});toast('Order cancelled');await refreshOrder(id)}catch(e){toast(e.message)}};
  $('sheet').querySelectorAll('[data-void]').forEach(function(b){b.onclick=async function(){var r=prompt('Why void this payment? (kept in history)');if(!r)return;try{await rpc('order_correct',{p_order:id,p_field:'void_payment',p_value:b.dataset.void,p_reason:r});toast('Payment voided');await refreshOrder(id)}catch(e){toast(e.message)}}});
}
G.openOrder=openOrder;
async function refreshOrder(id){delete O.events[id];await O.load();G.render(true);openOrder(id,true)}
async function loadHist(id){
  try{
    var ev=O.events[id]||(O.events[id]=await api('order_events?select=at,by_name,action,detail&order_id=eq.'+id+'&order=at.desc'));
    var box=$('o_hist');if(!box||!G.isCur('order',id))return;
    box.textContent=ev.map(function(e){return G.fdt(e.at)+', '+(e.by_name||'')+': '+e.action+(e.detail?' - '+e.detail:'')}).join('\n')||'No history yet';
  }catch(e){var b=$('o_hist');if(b)b.textContent='Could not load history'}
}

/* ---- on a lead: its orders, or a button to create one ---- */
G.leadOrdersBox=function(l){
  var os=byLead(l.id);
  return '<div class="box"><h3>Orders'+(os.length?'<span class="r">'+os.length+'</span>':'')+'</h3>'
   +(os.length?'<div class="list">'+os.map(function(o){return '<button class="btn" data-oo="'+o.id+'" style="justify-content:space-between;width:100%"><span>'+esc(o.order_no)+' | '+esc(rs(o.due_amount))+'</span><span class="tag '+stCls(o.status)+'">'+esc(o.status)+'</span></button>'}).join('')+'</div>':'<div style="font-size:.88rem;color:var(--mut);margin-bottom:.5rem">Customer agreed to buy? Create the order here, so invoice, payment and dispatch are tracked. The lead moves to Won.</div>')
   +'<div class="acts2" style="margin-top:.5rem"><button class="btn pri" id="d_order">'+(os.length?'Create another order':'Create order')+'</button></div></div>';
};
G.bindLeadOrders=function(l){
  var b=$('d_order');if(b)b.onclick=function(){newOrder(l)};
  document.querySelectorAll('[data-oo]').forEach(function(x){x.onclick=function(){G.S.tab='orders';G.render();openOrder(x.dataset.oo)}});
};
})();
