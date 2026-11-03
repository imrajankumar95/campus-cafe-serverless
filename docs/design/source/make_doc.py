import sys, re, pathlib, html

icons_dir = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

ICONS = {
    "func": "10029-icon-service-Function-Apps.svg",
    "storage": "10086-icon-service-Storage-Accounts.svg",
    "queue": "10840-icon-service-Storage-Queue.svg",
    "table": "10841-icon-service-Table.svg",
    "blob": "10780-icon-service-Blob-Block.svg",
    "acs": "00968-icon-service-Azure-Communication-Services.svg",
    "insights": "00012-icon-service-Application-Insights.svg",
    "identity": "10227-icon-service-Managed-Identities.svg",
    "budget": "10793-icon-service-Cost-Budgets.svg",
    "rg": "10007-icon-service-Resource-Groups.svg",
    "users": "10230-icon-service-Users.svg",
}

BLUE, ORANGE, DARK, GRAY = "#0F6CBD", "#C75B12", "#323130", "#6B6B6B"


def esc(s):
    return html.escape(s, quote=False)


def load_symbol(key, fname):
    raw = (icons_dir / fname).read_text(encoding="utf-8")
    m = re.search(r"<svg\b[^>]*>(.*)</svg>\s*$", raw, re.S)
    inner = re.sub(r"<title>.*?</title>", "", m.group(1), flags=re.S)
    return '<symbol id="ic-%s" viewBox="0 0 18 18">%s</symbol>' % (key, inner)


def marker(mid, color):
    return ('<marker id="%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" '
            'markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (mid, color))


def icon(key, x, y, size):
    return '<use href="#ic-%s" x="%s" y="%s" width="%s" height="%s"/>' % (key, x, y, size, size)


def text(x, y, s, cls, anchor=None):
    a = ' text-anchor="%s"' % anchor if anchor else ""
    return '<text x="%s" y="%s" class="%s"%s>%s</text>' % (x, y, cls, a, esc(s))


def rect(x, y, w, h, fill="#FFFFFF", stroke="#C8C6C4", sw=1.2, rx=8, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (
        x, y, w, h, rx, fill, stroke, sw, d)


def path(d, color, mk, dash=None, sw=1.8):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s marker-end="url(#%s)"/>' % (d, color, sw, ds, mk)


def badge(cx, cy, n, color):
    return ('<circle cx="%s" cy="%s" r="10" fill="%s" stroke="#FFFFFF" stroke-width="1.5"/>' % (cx, cy, color)
            + '<text x="%s" y="%s" class="num">%s</text>' % (cx, cy + 4.2, n))


def fn_card(x, y, title, l2, l3):
    return (rect(x, y, 220, 100, stroke="#8FB6E3")
            + icon("func", x + 12, y + 12, 32)
            + text(x + 54, y + 34, title, "t14")
            + text(x + 12, y + 66, l2, "s11")
            + text(x + 12, y + 84, l3, "s11"))


def st_card(x, y, key, title, l1, l2):
    cx = x + 70
    return (rect(x, y, 140, 96, stroke="#79BBA6")
            + icon(key, cx - 15, y + 10, 30)
            + text(cx, y + 58, title, "t13", "middle")
            + text(cx, y + 74, l1, "s11", "middle")
            + text(cx, y + 89, l2, "s11", "middle"))


def plat_card(x, y, key, title, sub):
    return (rect(x, y, 240, 56, fill="#F8F8F8", stroke="#BDBDBD")
            + icon(key, x + 10, y + 14, 28)
            + text(x + 46, y + 24, title, "t13")
            + text(x + 46, y + 42, sub, "s11"))


CSS_SVG = (
    '.t14{font:600 14px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.t13{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.t125{font:600 12.5px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.s11{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#4B4B4B}'
    '.g11{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B}'
    '.cap{font:600 10px "Segoe UI",Arial,sans-serif;fill:#6B6B6B;letter-spacing:.09em}'
    '.num{font:700 12px "Segoe UI",Arial,sans-serif;fill:#fff;text-anchor:middle}'
    '.lbl{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130}'
    '.lblr{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130;text-anchor:end}'
    '.hdrr{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E;text-anchor:end}'
    '.g11r{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B;text-anchor:end}'
)

W, H = 1000, 644
s = []
add = s.append

add('<defs><style>%s</style>' % CSS_SVG)
add(marker("ah-blue", BLUE) + marker("ah-orange", ORANGE) + marker("ah-dark", DARK) + marker("ah-gray", GRAY))
add("".join(load_symbol(k, f) for k, f in ICONS.items()))
add("</defs>")
add('<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))

# actors
add(rect(30, 14, 200, 68, stroke="#C8C6C4"))
add(icon("users", 42, 28, 40) + text(92, 46, "Customer", "t14") + text(92, 65, "Browser or Postman", "s11"))
add(rect(325, 14, 200, 68, stroke="#C8C6C4"))
add(icon("users", 337, 28, 40) + text(387, 46, "Café staff", "t14") + text(387, 65, "Postman · staff key", "s11"))

# resource group boundary
add(rect(8, 94, 824, 502, fill="none", stroke="#6B6B6B", sw=1.2, rx=10, dash="6 4"))
add(text(796, 114, "Resource group · rg-campus-cafe", "hdrr") + icon("rg", 804, 98, 22))

# function app boundary
add(rect(40, 126, 770, 162, fill="#EAF3FC", stroke=BLUE, sw=1.3, rx=10))
add(text(772, 149, "Function App · Flex Consumption", "hdrr") + icon("func", 778, 130, 26))
add(text(772, 166, "Linux · scales to zero · max 5 instances", "g11r"))
add(fn_card(60, 172, "SubmitOrder", "HTTP trigger · POST /api/orders", "Validate · save · enqueue"))
add(fn_card(315, 172, "UpdateOrderStatus", "HTTP trigger · function key", "Check status · save · enqueue"))
add(fn_card(570, 172, "SendNotification", "Queue trigger (notify)", "Template · send · mark notified"))

# storage boundary
add(rect(40, 336, 500, 160, fill="#ECF7F3", stroke="#2A9D78", sw=1.3, rx=10))
add(icon("storage", 48, 342, 24) + text(80, 359, "Storage account · Standard LRS", "hdr_l" if False else "t13"))
add(st_card(60, 392, "table", "Table: orders", "status + customer email", "PK date · RK orderId"))
add(st_card(220, 392, "blob", "Blob: runtime", "Functions host state", "deployment package"))
add(st_card(380, 392, "queue", "Queue: notify", "order status messages", "+ notify-poison (auto)"))

# ACS
add(rect(565, 392, 230, 96, stroke="#B8A9D9"))
add(icon("acs", 577, 400, 32) + text(577, 450, "Azure Communication Services", "t125"))
add(text(577, 467, "Email · Azure-managed domain", "s11") + text(577, 482, "Cap: 5/min · 10/hour", "s11"))

# inbox (generic envelope, not an Azure icon)
add(rect(852, 392, 140, 96, stroke="#C8C6C4"))
add('<rect x="904" y="406" width="36" height="25" rx="3" fill="#FFFFFF" stroke="#6B6B6B" stroke-width="1.6"/>'
    '<path d="M905 408 L922 421 L939 408" fill="none" stroke="#6B6B6B" stroke-width="1.6" stroke-linejoin="round"/>')
add(text(922, 454, "Customer inbox", "t13", "middle") + text(922, 472, "3 status emails", "s11", "middle"))

# platform
add(text(40, 514, "PLATFORM SERVICES · SECURITY · MONITORING · COST", "cap"))
add(plat_card(40, 520, "insights", "Application Insights", "Logs · failures · poison alert"))
add(plat_card(305, 520, "identity", "Managed identity", "Function App → Storage (RBAC)"))
add(plat_card(570, 520, "budget", "Cost Management budget", "Email alert at $5 spend"))

# arrows: customer path (blue)
add(path("M130 82 L130 170", BLUE, "ah-blue"))
add(path("M130 272 L130 334", BLUE, "ah-blue"))
# staff path (orange)
add(path("M425 82 L425 170", ORANGE, "ah-orange"))
add(path("M425 272 L425 334", ORANGE, "ah-orange"))
# shared notification path (dark)
add(path("M450 392 L450 312 L620 312 L620 274", DARK, "ah-dark"))
add(path("M680 272 L680 390", DARK, "ah-dark"))
add(path("M795 440 L850 440", DARK, "ah-dark"))
# dashed: telemetry and identity
add(path("M40 250 L24 250 L24 548 L38 548", GRAY, "ah-gray", dash="5 4", sw=1.5))
add(path("M425 520 L425 498", GRAY, "ah-gray", dash="5 4", sw=1.5))
add(text(437, 512, "RBAC roles, no keys", "g11"))

# badges and arrow labels
add(badge(146, 110, 1, BLUE) + text(162, 114, "POST /api/orders", "lbl"))
add(badge(146, 312, 2, BLUE) + text(162, 316, "save + enqueue", "lbl"))
add(badge(441, 110, 3, ORANGE) + text(457, 114, "PUT /status + key", "lbl"))
add(badge(408, 312, 4, ORANGE) + text(396, 316, "save + enqueue", "lblr"))
add(badge(480, 312, 5, DARK) + text(496, 300, "queue trigger", "lbl"))
add(badge(698, 332, 6, DARK) + text(714, 336, "send email", "lbl"))
add(badge(812, 440, 7, DARK))

# legend
ly = 624
add(badge(20, ly, 1, BLUE) + badge(44, ly, 2, BLUE) + text(60, ly + 4, "Customer order", "lbl"))
add(badge(176, ly, 3, ORANGE) + badge(200, ly, 4, ORANGE) + text(216, ly + 4, "Staff status update", "lbl"))
add(badge(356, ly, 5, DARK) + badge(380, ly, 6, DARK) + badge(404, ly, 7, DARK) + text(420, ly + 4, "Notify customer (shared)", "lbl"))
add('<path d="M600 %d L636 %d" fill="none" stroke="%s" stroke-width="1.5" stroke-dasharray="5 4"/>' % (ly, ly, GRAY))
add(text(644, ly + 4, "Identity / telemetry", "lbl"))

body = "".join(s)
svg_inline = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
              'aria-label="Campus Café Azure serverless architecture v1">%s</svg>' % (W, H, body))
svg_file = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>\n' % (W, H, W, H, body))
(out_dir / "campus-cafe-architecture-v1.svg").write_text(svg_file, encoding="utf-8")

CSS_DOC = """
:root{--blue:#0F6CBD;--orange:#C75B12;--dark:#323130;--line:#E1DFDD;--bg:#F3F2F1}
*{box-sizing:border-box}
@page{size:11in 8.5in;margin:0}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI",Arial,sans-serif;color:#201F1E;font-size:9.5pt;line-height:1.38;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:11in;height:8.5in;padding:.38in .45in .5in;position:relative;overflow:hidden;
 break-after:page;page-break-after:always;background:#fff}
.page:last-child{break-after:auto;page-break-after:auto}
.hdr{border-bottom:2px solid var(--blue);padding-bottom:.07in;margin-bottom:.1in}
h1{font-size:19pt;margin:0;font-weight:600;letter-spacing:-.2px}
.sub{color:#605E5C;font-size:9.5pt;margin-top:1px}
.chips{display:flex;gap:6px;margin-top:.06in}
.chip{background:#EFF6FC;border:1px solid #C7E0F4;color:#0B4F8A;border-radius:12px;padding:1px 9px;font-size:8.5pt;white-space:nowrap}
figure{margin:0}
figure svg{width:100%;height:auto;max-height:6.3in;display:block}
figcaption{font-size:8pt;color:#605E5C;margin-top:.05in}
h2{font-size:11pt;margin:0 0 .07in;padding-left:.09in;border-left:4px solid var(--blue);font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:.34in}
.blk{margin-bottom:.2in}
p{margin:0 0 .06in}
ul{margin:0;padding-left:1.1em}
li{margin-bottom:.045in}
code{font-family:Consolas,"Courier New",monospace;font-size:.92em;background:var(--bg);padding:0 3px;border-radius:3px}
table{border-collapse:collapse;width:100%;font-size:8.8pt}
th{background:var(--bg);text-align:left;padding:4px 6px;border-bottom:1px solid #C8C6C4;font-weight:600}
td{padding:4px 6px;border-bottom:1px solid var(--line);vertical-align:top}
ol.steps{list-style:none;margin:0;padding:0;counter-reset:s}
ol.steps li{position:relative;padding-left:.32in;margin-bottom:.07in;counter-increment:s}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:1px;width:.21in;height:.21in;border-radius:50%;
 background:var(--dark);color:#fff;font-weight:700;font-size:8.5pt;text-align:center;line-height:.21in}
ol.steps li.c::before{background:var(--blue)}
ol.steps li.s::before{background:var(--orange)}
.callout{border:1px solid #F1C8A4;background:#FFF7F0;border-radius:6px;padding:.08in .12in}
.box{background:#FAF9F8;border:1px solid var(--line);border-radius:6px;padding:.08in .12in}
.good{border-left:4px solid #107C10}
.bad{border-left:4px solid #C50F1F}
.note{font-size:8pt;color:#605E5C;margin-top:.05in}
.refs{font-size:8.3pt}
.refs li{margin-bottom:.035in}
.foot{position:absolute;left:.45in;right:.45in;bottom:.24in;display:flex;justify-content:space-between;font-size:7.5pt;color:#8A8886}
a{color:#0F6CBD;text-decoration:none}
"""

PAGE1 = """
<section class="page">
 <div class="hdr">
  <h1>Campus Café — Azure serverless order tracking</h1>
  <div class="sub">Simplified architecture v1 · George Brown College · Work Integrated Project · October 2026</div>
  <div class="chips"><span class="chip">3 functions</span><span class="chip">1 storage account</span>
   <span class="chip">1 email service</span><span class="chip">4 statuses · 3 emails</span><span class="chip">est. under $1 / month</span></div>
 </div>
 <figure>
  __DIAGRAM__
  <figcaption>Figure 1. Customer order = steps 1–2 (blue). Staff status update = steps 3–4 (orange). Notification = steps 5–7 (shared by both paths).
  Dashed lines = identity and telemetry. Azure icons: Microsoft Azure Public Service Icons V24, see References on page 3.</figcaption>
 </figure>
 <div class="foot"><span>Campus Café · Azure architecture v1</span><span>Page 1 of 3</span></div>
</section>
"""

PAGE2 = """
<section class="page">
 <div class="hdr"><h1>How it works</h1>
  <div class="sub">What each piece does, why the design is this small, and what it costs</div></div>
 <div class="cols">
  <div>
   <div class="blk">
    <h2>What it does</h2>
    <p>A customer places a coffee order and gets an email as it moves through four statuses:
    <b>Accepted → Preparing → Ready for pickup → Collected</b>. Staff move the status forward.
    The customer receives three emails. <b>Collected</b> closes the order with no email.</p>
   </div>
   <div class="blk">
    <h2>Steps (numbers match Figure 1)</h2>
    <ol class="steps">
     <li class="c">Customer sends <code>POST /api/orders</code> over HTTPS. The endpoint is public, so it validates input and limits size.</li>
     <li class="c"><code>SubmitOrder</code> saves the order as <code>Accepted</code> in Table <code>orders</code>, puts <code>{orderId, status}</code> on Queue <code>notify</code>, returns the <code>orderId</code>.</li>
     <li class="s">Staff send <code>PUT /api/orders/{id}/status</code> with a function key.</li>
     <li class="s"><code>UpdateOrderStatus</code> allows only the next valid status, saves it, and enqueues a message. <code>Collected</code> is saved with no message.</li>
     <li>The queue message triggers <code>SendNotification</code>. A failed message retries; after 5 failures it moves to <code>notify-poison</code>.</li>
     <li><code>SendNotification</code> picks the email text for the status, sends it through Azure Communication Services Email, then marks that status as notified so duplicates are skipped.</li>
     <li>Customer receives Accepted, Preparing and Ready emails.</li>
    </ol>
   </div>
   <div class="blk">
    <h2>Why this shape</h2>
    <ul>
     <li><b>Serverless:</b> pay per execution, scales to zero, no servers to patch.</li>
     <li><b>Event-driven:</b> a queue message triggers the email function, so HTTP calls return fast and email trouble never blocks an order.</li>
     <li><b>Queue as shock absorber:</b> the email service has hard send limits. Messages wait and retry instead of failing the request.</li>
     <li><b>Minimal on purpose:</b> the earlier V24 design (<code>ProcessOrder</code> + Event Grid) is deferred until a second consumer exists.</li>
    </ul>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>Services and cost (estimate)</h2>
    <table>
     <tr><th>Service</th><th>Role</th><th>Cost</th></tr>
     <tr><td>Azure Functions, Flex Consumption</td><td>3 functions, scale to zero</td><td>Free grant: 250,000 executions + 100,000 GB-s per month</td></tr>
     <tr><td>Storage account, Standard LRS</td><td>Table, Queue, Blob runtime</td><td>Cents per month</td></tr>
     <tr><td>Azure Communication Services Email</td><td>Customer emails</td><td>$0.00025 per email</td></tr>
     <tr><td>Application Insights</td><td>Logs, failures, poison-queue alert</td><td>First 5 GB per month free</td></tr>
     <tr><td>Managed identity</td><td>Function App to storage via RBAC</td><td>Free</td></tr>
     <tr><td>Cost Management budget</td><td>Alert before overspend</td><td>Free</td></tr>
    </table>
    <div class="note">Total estimate: under $1 per month, covered by Azure for Students ($100 credit, no card). Figures from Microsoft pricing pages, Oct 2026. Confirm in the Azure Pricing Calculator.</div>
   </div>
   <div class="blk">
    <h2>Well-Architected check</h2>
    <table>
     <tr><th>Pillar</th><th>In v1</th><th>Add later</th></tr>
     <tr><td>Reliability</td><td>Queue retry, poison queue, idempotent email, stateless functions</td><td>ZRS/GRS, Event Grid dead-letter</td></tr>
     <tr><td>Security</td><td>HTTPS only, function key for staff, managed identity to storage, no personal data in logs</td><td>Entra ID sign-in, Key Vault, VNet + private endpoints</td></tr>
     <tr><td>Cost optimization</td><td>Scale to zero, free grants, LRS, instance cap, budget alert</td><td>—</td></tr>
     <tr><td>Operational excellence</td><td>Application Insights, poison-queue alert, Git repo + README runbook</td><td>Bicep or Terraform, GitHub Actions deploy</td></tr>
     <tr><td>Performance efficiency</td><td>Email off the request path, per-function scaling</td><td>Always-ready instance, caching</td></tr>
    </table>
   </div>
  </div>
 </div>
 <div class="foot"><span>Campus Café · Azure architecture v1</span><span>Page 2 of 3</span></div>
</section>
"""

PAGE3 = """
<section class="page">
 <div class="hdr"><h1>Trade-offs, watch-outs and next steps</h1>
  <div class="sub">Honest limits of the simple design, verified against Microsoft documentation on 14 Oct 2026</div></div>
 <div class="cols">
  <div>
   <div class="blk">
    <h2>Good</h2>
    <div class="box good"><ul>
     <li>Few parts: 3 functions, 1 storage account, 1 email service. Easy to explain and demo.</li>
     <li>Still event-driven and decoupled: queue trigger, retries, poison queue.</li>
     <li>Near-zero cost, scales to zero.</li>
     <li>Same features as V24: 4 statuses, 3 emails.</li>
     <li>Clear upgrade path: each later step is one add-on.</li>
    </ul></div>
   </div>
   <div class="blk">
    <h2>Bad</h2>
    <div class="box bad"><ul>
     <li><code>SubmitOrder</code> is public (spam risk). A function key is a shared secret, not a user identity.</li>
     <li>Email is capped, may land in spam, and the service is retiring.</li>
     <li>Table Storage has no auto-number and weak queries. Staff cannot list open orders yet.</li>
     <li>Email only. The customer has no order-status page.</li>
     <li>Save and enqueue are not atomic. The notified flag makes retries safe.</li>
     <li>Cold start of a few seconds after idle. Single region, LRS only.</li>
    </ul></div>
   </div>
   <div class="blk">
    <h2>Later phases</h2>
    <p>Event Grid when a second consumer exists · <code>GET /orders</code> staff board · Entra ID sign-in · Key Vault · VNet + private endpoints · Bicep + GitHub Actions · simple web page on Static Web Apps (Free).</p>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>Watch-outs</h2>
    <div class="callout"><ul>
     <li><b>ACS Email retires 30 Sep 2028</b> (announced Sep 2026). Microsoft limits onboarding to retiring ACS services from 23 Oct 2026 and advises migrating rather than building new. Keep email behind <code>SendNotification</code> and an <code>EMAIL_MODE</code> setting so a swap touches one function. Alternatives: Marketplace partners (Infobip, Telesign). M365 High Volume Email is internal-send only.</li>
     <li><b>Azure-managed domain cap: 5 emails per minute, 10 per hour per subscription, no increase.</b> Three emails per order is about 3 orders per hour. A verified custom domain allows 30 per minute, 100 per hour.</li>
     <li><b>Flex Consumption is Linux only.</b> Student subscriptions get a 15-core default regional quota, plenty for 3 functions.</li>
    </ul></div>
   </div>
   <div class="blk">
    <h2>Build order (each step demo-able)</h2>
    <ol class="steps">
     <li>Resource group, storage account, Function App (Flex), Application Insights. Hello-world HTTP function.</li>
     <li><code>SubmitOrder</code> writes to Table. Test in Postman.</li>
     <li>Queue + <code>SendNotification</code> with <code>EMAIL_MODE=log</code>.</li>
     <li><code>UpdateOrderStatus</code> with status rules.</li>
     <li>Switch to <code>EMAIL_MODE=acs</code>.</li>
     <li>Harden: managed identity, function key, HTTPS only, $5 budget, log daily cap.</li>
    </ol>
    <div class="note">Develop locally first with Azurite (free storage emulator) and log mode. Cost stays $0 until deploy.</div>
   </div>
  </div>
 </div>
 <div class="blk" style="margin-top:.05in">
  <h2>References and credits</h2>
  <ul class="refs">
   <li><b>Icons:</b> Microsoft Azure Public Service Icons V24, file <code>Azure_Public_Service_Icons_V24.zip</code> (Azure architecture icons, © Microsoft).
   Used unmodified (no crop, flip, rotate or distortion) with the product name beside each icon, for architecture documentation, as the pack's Terms of Use permit.
   Icons used: Users, Resource Groups, Function Apps, Storage Accounts, Table, Blob Block, Storage Queue, Azure Communication Services, Application Insights, Managed Identities, Cost Budgets.</li>
   <li><b>Microsoft documentation:</b>
    <a href="https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-plan">Flex Consumption plan</a> ·
    <a href="https://azure.microsoft.com/en-us/pricing/details/functions/">Functions pricing</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/communication-services/concepts/service-limits">ACS service limits</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/communication-services/concepts/email-pricing">ACS Email pricing</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/communication-services/acs-retirement-and-breaking-changes-guide">ACS retirement guide</a> ·
    <a href="https://azure.microsoft.com/en-us/free/students">Azure for Students</a></li>
  </ul>
 </div>
 <div class="foot"><span>Campus Café · Azure architecture v1</span><span>Page 3 of 3</span></div>
</section>
"""

doc = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
       '<title>Campus Café — Azure serverless order tracking (v1)</title>'
       '<style>%s</style></head><body>%s%s%s</body></html>'
       % (CSS_DOC, PAGE1.replace("__DIAGRAM__", svg_inline), PAGE2, PAGE3))
(out_dir / "campus-cafe-architecture-v1.html").write_text(doc, encoding="utf-8")
print("ok", len(doc), "bytes html;", len(svg_file), "bytes svg")
