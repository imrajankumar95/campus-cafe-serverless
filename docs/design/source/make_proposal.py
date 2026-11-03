import sys, re, pathlib

svg_path = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

svg = svg_path.read_text(encoding="utf-8")
svg = re.sub(r'^<\?xml[^>]*\?>\s*', '', svg)
svg, n = re.subn(
    r'<svg xmlns="http://www.w3.org/2000/svg" width="\d+" height="\d+" viewBox="([^"]+)">',
    r'<svg xmlns="http://www.w3.org/2000/svg" viewBox="\1" role="img" aria-label="Campus Café infrastructure architecture">',
    svg, count=1)
assert n == 1, "svg root not matched"

CSS = """
:root{--blue:#0F6CBD;--orange:#C75B12;--dark:#323130;--line:#E1DFDD;--bg:#F3F2F1}
*{box-sizing:border-box}
@page{size:11in 8.5in;margin:0}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI",Arial,sans-serif;color:#201F1E;font-size:8.8pt;line-height:1.33;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:11in;height:8.5in;padding:.36in .45in .5in;position:relative;overflow:hidden;
 break-after:page;page-break-after:always;background:#fff}
.page:last-child{break-after:auto;page-break-after:auto}
.hdr{border-bottom:2px solid var(--blue);padding-bottom:.06in;margin-bottom:.1in}
h1{font-size:18pt;margin:0;font-weight:600;letter-spacing:-.2px}
.sub{color:#605E5C;font-size:9.2pt;margin-top:1px}
.chips{display:flex;gap:6px;margin-top:.05in}
.chip{background:#EFF6FC;border:1px solid #C7E0F4;color:#0B4F8A;border-radius:12px;padding:1px 9px;font-size:8.2pt;white-space:nowrap}
h2{font-size:10.2pt;margin:0 0 .045in;padding-left:.09in;border-left:4px solid var(--blue);font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:.34in}
.blk{margin-bottom:.12in}
p{margin:0 0 .04in}
ul{margin:0;padding-left:1.1em}
li{margin-bottom:.025in}
code{font-family:Consolas,"Courier New",monospace;font-size:.9em;background:var(--bg);padding:0 3px;border-radius:3px;white-space:nowrap}
table{border-collapse:collapse;width:100%;font-size:7.9pt;line-height:1.25}
th{background:var(--bg);text-align:left;padding:2.5px 5px;border-bottom:1px solid #C8C6C4;font-weight:600}
td{padding:2.2px 5px;border-bottom:1px solid var(--line);vertical-align:top}
ol.steps{list-style:none;margin:0;padding:0;counter-reset:s}
ol.steps li{position:relative;padding-left:.29in;margin-bottom:.04in;counter-increment:s}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:1px;width:.19in;height:.19in;border-radius:50%;
 background:var(--dark);color:#fff;font-weight:700;font-size:7.8pt;text-align:center;line-height:.19in}
ol.steps li.c::before{background:var(--blue)}
ol.steps li.s::before{background:var(--orange)}
.callout{border:1px solid #F1C8A4;background:#FFF7F0;border-radius:6px;padding:.05in .11in}
.note{font-size:7.5pt;color:#605E5C;margin-top:.03in}
figure{margin:0}
figure svg{width:100%;height:auto;max-height:6.05in;display:block;margin:0 auto}
figcaption{font-size:7.8pt;color:#605E5C;margin-top:.03in}
.refs{font-size:7.8pt;margin-top:.06in}
.refs li{margin-bottom:.02in}
.foot{position:absolute;left:.45in;right:.45in;bottom:.22in;display:flex;justify-content:space-between;font-size:7.5pt;color:#8A8886}
a{color:#0F6CBD;text-decoration:none}
"""

PAGE1 = """
<section class="page">
 <div class="hdr">
  <h1>Campus Café — Serverless Order Tracking on Azure</h1>
  <div class="sub">Project proposal · George Brown College · Work Integrated Project · October 2026</div>
  <div class="chips"><span class="chip">Serverless</span><span class="chip">Event-driven (queue trigger)</span>
   <span class="chip">3 functions · 18 resources</span><span class="chip">est. under $1 / month</span></div>
 </div>
 <div class="cols">
  <div>
   <div class="blk">
    <h2>Overview</h2>
    <p>A campus café needs to take customer orders and keep customers informed. This project builds a small order-tracking system on Azure using serverless services.
    A customer places an order. Café staff move it through four statuses: <b>Accepted → Preparing → Ready for pickup → Collected</b>.
    The customer receives an email at each of the first three.</p>
   </div>
   <div class="blk">
    <h2>Goals and scope</h2>
    <ul>
     <li>A working, deployed system on Azure: order API, staff status API, email notifications.</li>
     <li>A serverless, event-driven design (a queue message triggers the email function) that shows reliability, security and monitoring in practice: retries, poison queue, managed identity, alerts.</li>
     <li>Near-zero cost on an Azure for Students subscription, following Azure Well-Architected principles.</li>
     <li><b>Out of scope:</b> payments, customer accounts, mobile app, order-status web page.</li>
    </ul>
   </div>
   <div class="blk">
    <h2>How it works (numbers match the diagram on page 2)</h2>
    <ol class="steps">
     <li class="c">The customer sends an order: <code>POST /api/orders</code> over HTTPS.</li>
     <li class="c"><code>SubmitOrder</code> validates it, saves it as <code>Accepted</code> in the Table, puts a message on Queue <code>notify</code>, and returns the order id.</li>
     <li class="s">Staff send a status update: <code>PUT /status</code> with a function key.</li>
     <li class="s"><code>UpdateOrderStatus</code> allows only the next valid status, saves it, and queues a message (none for <code>Collected</code>).</li>
     <li>The queue message triggers <code>SendNotification</code>. A failed message retries, then moves to the poison queue and raises an alert.</li>
     <li><code>SendNotification</code> builds the email and sends it through Azure Communication Services, then marks that status as notified.</li>
     <li>The customer receives the email (three per order).</li>
    </ol>
   </div>
   <div class="blk">
    <h2>Plan</h2>
    <table>
     <tr><th>Phase</th><th>Work</th><th>Output</th></tr>
     <tr><td>1 Foundation</td><td>Resource group, storage, monitoring, identity</td><td>Wired environment</td></tr>
     <tr><td>2 Core flow</td><td>Order + status functions, queue, table</td><td>Statuses advance</td></tr>
     <tr><td>3 Email</td><td>Notification function, Communication Services</td><td>3 customer emails</td></tr>
     <tr><td>4 Monitoring</td><td>Diagnostic setting, alerts, budget</td><td>Failure + poison alerts</td></tr>
     <tr><td>5 Test and demo</td><td>Demo script, README</td><td>Live demo and report</td></tr>
    </table>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>Architecture at a glance</h2>
    <p>One Azure subscription holds one resource group, <code>rg-campus-cafe</code>, with 18 resources in four groups:</p>
    <ul>
     <li><b>Compute:</b> Flex Consumption plan + one Function App (3 functions).</li>
     <li><b>Data:</b> one storage account: Table <code>orders</code>, Queue <code>notify</code> (+ poison queue), Blob containers.</li>
     <li><b>Email:</b> Azure Communication Services, Email service, Azure-managed domain.</li>
     <li><b>Platform:</b> managed identity, Application Insights, Log Analytics, diagnostic setting, 2 alert rules, action group, budget.</li>
    </ul>
   </div>
   <div class="blk">
    <h2>Design principles</h2>
    <ul>
     <li><b>Serverless, event-driven:</b> pay per execution; the queue decouples HTTP from email.</li>
     <li><b>Reliable:</b> retries, poison queue, alert; no duplicate emails on retry.</li>
     <li><b>Secure:</b> HTTPS, function key for staff, managed identity + RBAC, no storage keys.</li>
     <li><b>Observable:</b> Application Insights + Log Analytics; alerts email the team.</li>
     <li><b>Cost-aware:</b> free grants, LRS, max 5 instances, $5 budget alert.</li>
    </ul>
   </div>
   <div class="blk">
    <h2>Estimated cost per month</h2>
    <table>
     <tr><th>Item</th><th>Estimate</th></tr>
     <tr><td>Azure Functions (Flex Consumption)</td><td>Within free grant (250,000 executions, 100,000 GB-s)</td></tr>
     <tr><td>Storage account (LRS)</td><td>Cents</td></tr>
     <tr><td>Communication Services Email</td><td>$0.00025 per email</td></tr>
     <tr><td>Application Insights + Log Analytics</td><td>Within 5 GB free</td></tr>
     <tr><td>Alerts, identity, budget</td><td>Free tier; optional log alert about $0.50+</td></tr>
     <tr><td><b>Total</b></td><td><b>Under $1, covered by Azure for Students ($100 credit)</b></td></tr>
    </table>
    <div class="note">Estimates; confirm in the Azure Pricing Calculator.</div>
   </div>
   <div class="blk">
    <h2>Risks and limits</h2>
    <div class="callout"><ul>
     <li><b>Email cap:</b> managed domain allows 5 emails/min, 10/hour (demo under ~3 orders/hour). ACS Email retires 30 Sep 2028 and new onboarding is limited from 23 Oct 2026, so email sits behind one function and can be swapped.</li>
     <li><b>Public endpoints:</b> the order API is anonymous (inputs validated); a function key is a shared secret.</li>
     <li><b>Cold start:</b> the first request after idle can take a few seconds.</li>
     <li><b>To confirm:</b> Flex region availability; budgets on the student subscription.</li>
    </ul></div>
    <div class="note">Possible later phases: Event Grid fan-out (SMS, dashboard), Key Vault, Entra ID sign-in for staff, VNet and private endpoints, Bicep and GitHub Actions.</div>
   </div>
  </div>
 </div>
 <div class="foot"><span>Campus Café · Project proposal</span><span>Page 1 of 2</span></div>
</section>
"""

PAGE2 = """
<section class="page">
 <div class="hdr">
  <h1>Architecture</h1>
  <div class="sub">Infrastructure behind the order-tracking flow: subscription, resource group and all 18 resources</div>
 </div>
 <figure>
  __DIAGRAM__
  <figcaption>Figure 1. Numbers 1–7 follow the flow on page 1: customer order = 1–2 (blue), staff status update = 3–4 (orange), notification = 5–7 (shared).
  Dashed lines = identity (RBAC), diagnostic logs and telemetry.</figcaption>
 </figure>
 <ul class="refs">
  <li><b>Icons:</b> Microsoft Azure Public Service Icons V24, file <code>Azure_Public_Service_Icons_V24.zip</code> (Azure architecture icons, © Microsoft). Used unmodified, with the product name beside each icon, for architecture documentation, as the pack's Terms of Use permit.</li>
  <li><b>Microsoft documentation:</b>
   <a href="https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-how-to">Flex Consumption</a> ·
   <a href="https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections">Functions connections and roles</a> ·
   <a href="https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-queue-trigger">Queue trigger</a> ·
   <a href="https://learn.microsoft.com/en-us/azure/communication-services/concepts/service-limits">ACS service limits</a> ·
   <a href="https://learn.microsoft.com/en-us/azure/communication-services/acs-retirement-and-breaking-changes-guide">ACS retirement guide</a> ·
   <a href="https://azure.microsoft.com/en-us/free/students">Azure for Students</a></li>
 </ul>
 <div class="foot"><span>Campus Café · Project proposal</span><span>Page 2 of 2</span></div>
</section>
"""

doc = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
       '<title>Campus Café — Project proposal</title>'
       '<style>%s</style></head><body>%s%s</body></html>'
       % (CSS, PAGE1, PAGE2.replace("__DIAGRAM__", svg)))
(out_dir / "campus-cafe-proposal.html").write_text(doc, encoding="utf-8")
print("ok", len(doc), "bytes")
