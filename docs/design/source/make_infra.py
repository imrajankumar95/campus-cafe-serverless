import sys, re, pathlib, html

icons_dir = pathlib.Path(sys.argv[1])
out_dir = pathlib.Path(sys.argv[2])
out_dir.mkdir(parents=True, exist_ok=True)

ICONS = {
    "users": "10230-icon-service-Users.svg",
    "sub": "10002-icon-service-Subscriptions.svg",
    "rg": "10007-icon-service-Resource-Groups.svg",
    "plan": "00046-icon-service-App-Service-Plans.svg",
    "func": "10029-icon-service-Function-Apps.svg",
    "storage": "10086-icon-service-Storage-Accounts.svg",
    "table": "10841-icon-service-Table.svg",
    "blob": "10780-icon-service-Blob-Block.svg",
    "queue": "10840-icon-service-Storage-Queue.svg",
    "acs": "00968-icon-service-Azure-Communication-Services.svg",
    "insights": "00012-icon-service-Application-Insights.svg",
    "law": "00009-icon-service-Log-Analytics-Workspaces.svg",
    "diag": "00008-icon-service-Diagnostics-Settings.svg",
    "identity": "10227-icon-service-Managed-Identities.svg",
    "alerts": "00002-icon-service-Alerts.svg",
    "budget": "10793-icon-service-Cost-Budgets.svg",
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


def text(x, y, s, cls):
    return '<text x="%s" y="%s" class="%s">%s</text>' % (x, y, cls, esc(s))


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


def chip(x, y, w, h, key, title, sub, stroke="#C8C6C4", fill="#FFFFFF", isz=22):
    ty = y + h // 2 - 2
    sy = ty + 15
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.1, rx=7)
            + icon(key, x + 8, y + (h - isz) / 2, isz)
            + text(x + 8 + isz + 7, ty, title, "t12")
            + text(x + 8 + isz + 7, sy, sub, "s11"))


def svc_chip(x, y, w, h, key, title, l1, l2, stroke):
    return (rect(x, y, w, h, stroke=stroke, sw=1.1, rx=7)
            + icon(key, x + 8, y + 8, 24)
            + text(x + 38, y + 26, title, "t12")
            + text(x + 10, y + 51, l1, "s11")
            + text(x + 10, y + 68, l2, "s11"))


def fn_card(x, y, title, l2, l3):
    return (rect(x, y, 232, 70, stroke="#8FB6E3", sw=1.1, rx=7)
            + icon("func", x + 10, y + 8, 24)
            + text(x + 40, y + 26, title, "t13")
            + text(x + 10, y + 46, l2, "s11")
            + text(x + 10, y + 62, l3, "s11"))


CSS_SVG = (
    '.t14{font:600 14px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.t13{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.t12{font:600 12px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.s11{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#4B4B4B}'
    '.g11{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B}'
    '.num{font:700 12px "Segoe UI",Arial,sans-serif;fill:#fff;text-anchor:middle}'
    '.lbl{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130}'
    '.lblr{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130;text-anchor:end}'
    '.hdrr{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E;text-anchor:end}'
    '.g11r{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B;text-anchor:end}'
)

W, H = 1000, 698
s = []
add = s.append

add('<defs><style>%s</style>' % CSS_SVG)
add(marker("ah-blue", BLUE) + marker("ah-orange", ORANGE) + marker("ah-dark", DARK) + marker("ah-gray", GRAY))
add("".join(load_symbol(k, f) for k, f in ICONS.items()))
add("</defs>")
add('<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))

# actors (same as v1)
add(rect(92, 8, 200, 52, stroke="#C8C6C4"))
add(icon("users", 102, 18, 32) + text(144, 31, "Customer", "t14") + text(144, 48, "Browser or Postman", "s11"))
add(rect(334, 8, 200, 52, stroke="#C8C6C4"))
add(icon("users", 344, 18, 32) + text(386, 31, "Café staff", "t14") + text(386, 48, "Postman · staff key", "s11"))

# subscription and resource group boundaries
add(rect(4, 70, 992, 620, fill="none", stroke="#6B6B6B", sw=1, rx=14, dash="7 4"))
add(text(962, 88, "Subscription · Azure for Students", "hdrr") + icon("sub", 968, 74, 22))
add(rect(14, 98, 822, 582, fill="none", stroke="#6B6B6B", sw=1.2, rx=12, dash="5 3"))
add(text(804, 113, "Resource group · rg-campus-cafe", "hdrr") + icon("rg", 810, 98, 22))
add(text(804, 128, "Canada Central (target)", "g11r"))

# compute panel
add(rect(44, 140, 780, 204, fill="#FAFAFA", stroke="#C8C6C4", sw=1, rx=10))
add(text(56, 157, "Compute", "t13"))
add(rect(54, 164, 760, 172, fill="#F4F9FE", stroke=BLUE, sw=1.1, rx=10, dash="5 3"))
add(text(776, 183, "asp-campus-cafe", "hdrr") + icon("plan", 782, 166, 24))
add(text(776, 199, "App Service plan · Flex Consumption (FC1) · Linux", "g11r"))
add(rect(66, 208, 736, 122, fill="#EAF3FC", stroke=BLUE, sw=1.3, rx=10))
add(text(766, 226, "func-campus-cafe", "hdrr") + icon("func", 772, 210, 24))
add(text(766, 242, "Function App · max 5 instances · identity id-campus-cafe-func", "g11r"))
add(fn_card(76, 252, "SubmitOrder", "HTTP trigger · anonymous", "validate · save · enqueue"))
add(fn_card(318, 252, "UpdateOrderStatus", "HTTP trigger · function key", "check status · save · enqueue"))
add(fn_card(560, 252, "SendNotification", "Queue trigger · notify", "template · send · mark notified"))

# data panel
add(rect(44, 374, 516, 170, fill="#FAFAFA", stroke="#C8C6C4", sw=1, rx=10))
add(text(56, 391, "Data", "t13"))
add(rect(52, 400, 500, 136, fill="#ECF7F3", stroke="#2A9D78", sw=1.3, rx=10))
add(icon("storage", 62, 405, 24) + text(94, 421, "stcampuscafe", "t13"))
add(text(94, 436, "Storage account · Standard LRS · TLS 1.2 · keyless", "g11"))
add(svc_chip(62, 446, 156, 82, "table", "Table service", "orders", "PK date · RK orderId", "#2A9D78"))
add(svc_chip(224, 446, 156, 82, "blob", "Blob service", "host state", "deployment package", "#2A9D78"))
add(svc_chip(386, 446, 156, 82, "queue", "Queue service", "notify", "notify-poison (auto)", "#2A9D78"))

# email panel
add(rect(584, 374, 240, 170, fill="#F7F4FC", stroke="#B8A9D9", sw=1, rx=10))
add(text(596, 391, "Email", "t13"))
add(chip(594, 400, 220, 42, "acs", "acs-campus-cafe", "Communication Services", stroke="#B8A9D9"))
add(chip(594, 448, 220, 42, "acs", "ecs-campus-cafe", "Email Communication Service", stroke="#B8A9D9"))
add(chip(594, 496, 220, 42, "acs", "Azure-managed domain", "cap 5/min · 10/hour", stroke="#B8A9D9"))

# inbox (generic envelope)
add(rect(858, 384, 130, 96, stroke="#C8C6C4"))
add('<rect x="905" y="398" width="36" height="25" rx="3" fill="#FFFFFF" stroke="#6B6B6B" stroke-width="1.6"/>'
    '<path d="M906 400 L923 413 L940 400" fill="none" stroke="#6B6B6B" stroke-width="1.6" stroke-linejoin="round"/>')
add(text(923, 448, "Customer inbox", "t13").replace('class="t13"', 'class="t13" text-anchor="middle"'))
add(text(923, 465, "3 status emails", "s11").replace('class="s11"', 'class="s11" text-anchor="middle"'))

# platform panel
add(rect(44, 552, 780, 120, fill="#F8F8F8", stroke="#BDBDBD", sw=1, rx=10))
add(text(56, 568, "Platform services", "t13"))
add(chip(54, 574, 184, 40, "insights", "Application Insights", "appi-campus-cafe", stroke="#BDBDBD"))
add(chip(246, 574, 184, 40, "diag", "Diagnostic setting", "queue service → log", stroke="#BDBDBD"))
add(chip(438, 574, 184, 40, "identity", "Managed identity", "id-campus-cafe-func", stroke="#BDBDBD"))
add(chip(630, 574, 184, 40, "law", "Log Analytics", "log-campus-cafe · 30 d", stroke="#BDBDBD"))
add(chip(54, 620, 184, 40, "alerts", "Alert rule · metric", "failed requests ≥ 1", stroke="#BDBDBD"))
add(chip(246, 620, 184, 40, "alerts", "Alert rule · log", "poison message (opt.)", stroke="#BDBDBD"))
add(chip(438, 620, 184, 40, "alerts", "Action group", "ag-campus-cafe · email", stroke="#BDBDBD"))
add(chip(630, 620, 184, 40, "budget", "Cost budget", "budget-campus-cafe · $5", stroke="#BDBDBD"))

# arrows: customer path (blue), staff path (orange), shared (dark)
add(path("M192 60 L192 250", BLUE, "ah-blue"))
add(path("M192 322 L192 398", BLUE, "ah-blue"))
add(path("M434 60 L434 250", ORANGE, "ah-orange"))
add(path("M434 322 L434 398", ORANGE, "ah-orange"))
add(path("M464 446 L464 362 L640 362 L640 324", DARK, "ah-dark"))
add(path("M720 324 L720 398", DARK, "ah-dark"))
add(path("M824 432 L856 432", DARK, "ah-dark"))
# dashed: telemetry rail, RBAC, diagnostic logs
add(path("M66 290 L29 290 L29 594 L52 594", GRAY, "ah-gray", dash="5 4", sw=1.5))
add(path("M500 574 L500 538", GRAY, "ah-gray", dash="5 4", sw=1.5))
add(path("M338 538 L338 572", GRAY, "ah-gray", dash="5 4", sw=1.5))
add(text(348, 566, "diagnostic logs", "g11"))
add(text(510, 566, "RBAC roles, no keys", "g11"))

# badges and labels
add(badge(208, 120, 1, BLUE) + text(224, 124, "POST /api/orders", "lbl"))
add(badge(208, 359, 2, BLUE) + text(224, 363, "save + enqueue", "lbl"))
add(badge(450, 120, 3, ORANGE) + text(466, 124, "PUT /status + key", "lbl"))
add(badge(418, 359, 4, ORANGE) + text(406, 363, "save + enqueue", "lblr"))
add(badge(500, 362, 5, DARK) + text(516, 356, "queue trigger", "lbl"))
add(badge(738, 360, 6, DARK) + text(754, 364, "send email", "lbl"))
add(badge(841, 417, 7, DARK))

body = "".join(s)
svg_inline = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" '
              'aria-label="Campus Café infrastructure architecture, detail of v1">%s</svg>' % (W, H, body))
svg_file = ('<?xml version="1.0" encoding="UTF-8"?>\n'
            '<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>\n' % (W, H, W, H, body))
(out_dir / "campus-cafe-infrastructure-v1.svg").write_text(svg_file, encoding="utf-8")

CSS_DOC = """
:root{--blue:#0F6CBD;--orange:#C75B12;--dark:#323130;--line:#E1DFDD;--bg:#F3F2F1}
*{box-sizing:border-box}
@page{size:11in 8.5in;margin:0}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI",Arial,sans-serif;color:#201F1E;font-size:9.5pt;line-height:1.36;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:11in;height:8.5in;padding:.36in .45in .5in;position:relative;overflow:hidden;
 break-after:page;page-break-after:always;background:#fff}
.page:last-child{break-after:auto;page-break-after:auto}
.hdr{border-bottom:2px solid var(--blue);padding-bottom:.06in;margin-bottom:.09in}
h1{font-size:18pt;margin:0;font-weight:600;letter-spacing:-.2px}
.sub{color:#605E5C;font-size:9.3pt;margin-top:1px}
figure{margin:0}
figure svg{width:100%;height:auto;max-height:6.72in;display:block;margin:0 auto}
figcaption{font-size:7.8pt;color:#605E5C;margin-top:.04in}
h2{font-size:10.5pt;margin:0 0 .06in;padding-left:.09in;border-left:4px solid var(--blue);font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:.34in}
.blk{margin-bottom:.16in}
p{margin:0 0 .05in}
ul{margin:0;padding-left:1.1em}
li{margin-bottom:.035in}
code{font-family:Consolas,"Courier New",monospace;font-size:.9em;background:var(--bg);padding:0 3px;border-radius:3px;white-space:nowrap}
table{border-collapse:collapse;width:100%;font-size:8.1pt;line-height:1.25}
th{background:var(--bg);text-align:left;padding:3px 5px;border-bottom:1px solid #C8C6C4;font-weight:600}
td{padding:2.5px 5px;border-bottom:1px solid var(--line);vertical-align:top}
td.y{color:#107C10;font-weight:600;white-space:nowrap}
td.i{color:#8A6D00;font-weight:600;white-space:nowrap}
ol.steps{list-style:none;margin:0;padding:0;counter-reset:s}
ol.steps li{position:relative;padding-left:.3in;margin-bottom:.05in;counter-increment:s}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:1px;width:.2in;height:.2in;border-radius:50%;
 background:var(--dark);color:#fff;font-weight:700;font-size:8pt;text-align:center;line-height:.2in}
.callout{border:1px solid #F1C8A4;background:#FFF7F0;border-radius:6px;padding:.07in .12in}
.box{background:#FAF9F8;border:1px solid var(--line);border-radius:6px;padding:.07in .12in}
.note{font-size:7.8pt;color:#605E5C;margin-top:.04in}
.refs{font-size:8.2pt}
.refs li{margin-bottom:.03in}
.foot{position:absolute;left:.45in;right:.45in;bottom:.22in;display:flex;justify-content:space-between;font-size:7.5pt;color:#8A8886}
a{color:#0F6CBD;text-decoration:none}
"""

PAGE1 = """
<section class="page">
 <div class="hdr">
  <h1>Campus Café — Infrastructure architecture</h1>
  <div class="sub">Detail of the v1 data-flow design · same 3 functions, same flow · George Brown College · Work Integrated Project · October 2026</div>
 </div>
 <figure>
  __DIAGRAM__
  <figcaption>Figure 1. Subscription, resource group and every resource behind the v1 diagram. Numbers 1–7 match v1: customer order = 1–2 (blue), staff status update = 3–4 (orange), notification = 5–7 (shared).
  Dashed lines = identity (RBAC), diagnostic logs and telemetry. Azure icons: Microsoft Azure Public Service Icons V24, see References on page 3.</figcaption>
 </figure>
 <div class="foot"><span>Campus Café · Infrastructure v1</span><span>Page 1 of 3</span></div>
</section>
"""

PAGE2 = """
<section class="page">
 <div class="hdr"><h1>Resource inventory and access</h1>
  <div class="sub">18 parts behind the v1 diagram. "Implied" = required for a v1 box to work, not drawn in v1 itself.</div></div>
 <div class="blk">
  <table>
   <tr><th>#</th><th>Name</th><th>Azure resource type</th><th>Group</th><th>Key settings</th><th>In v1 diagram</th></tr>
   <tr><td>1</td><td><code>budget-campus-cafe</code></td><td>Cost Management budget</td><td>Subscription</td><td>Email alert at $5 spend (support on Azure for Students unverified)</td><td class="y">Yes</td></tr>
   <tr><td>2</td><td><code>rg-campus-cafe</code></td><td>Resource group</td><td>—</td><td>Canada Central (target); tags app, env, course</td><td class="y">Yes</td></tr>
   <tr><td>3</td><td><code>asp-campus-cafe</code></td><td>App Service plan, Flex Consumption (FC1)</td><td>Compute</td><td>Linux; one app per plan</td><td class="i">Implied</td></tr>
   <tr><td>4</td><td><code>func-campus-cafe</code></td><td>Function App</td><td>Compute</td><td>3 functions; max 5 instances; always-ready 0; HTTPS only; CORS origins only if a browser page calls the API</td><td class="y">Yes</td></tr>
   <tr><td>5</td><td><code>id-campus-cafe-func</code></td><td>User-assigned managed identity</td><td>Platform</td><td>Attached to the Function App; RBAC on storage; created by the Flex portal wizard</td><td class="y">Yes</td></tr>
   <tr><td>6</td><td><code>stcampuscafe</code></td><td>Storage account</td><td>Data</td><td>Standard LRS; TLS 1.2; shared-key access off</td><td class="y">Yes</td></tr>
   <tr><td>7</td><td>table <code>orders</code></td><td>Table service</td><td>Data</td><td>PK date, RK orderId; status, customer email, notified flags</td><td class="y">Yes</td></tr>
   <tr><td>8</td><td>queue <code>notify</code> + <code>notify-poison</code></td><td>Queue service</td><td>Data</td><td>Poison after 5 tries (automatic); set <code>visibilityTimeout</code> 30–60 s (default 0 = instant retry)</td><td class="y">Yes</td></tr>
   <tr><td>9</td><td>blob containers</td><td>Blob service</td><td>Data</td><td>Functions host state + deployment package (Flex)</td><td class="y">Yes</td></tr>
   <tr><td>10</td><td><code>acs-campus-cafe</code></td><td>Communication Services</td><td>Email</td><td>Azure-managed domain linked</td><td class="y">Yes</td></tr>
   <tr><td>11</td><td><code>ecs-campus-cafe</code></td><td>Email Communication Service</td><td>Email</td><td>Holds the domain (no Cloud Adoption Framework prefix, team convention)</td><td class="i">Implied</td></tr>
   <tr><td>12</td><td>Azure-managed domain</td><td>Email domain (child resource)</td><td>Email</td><td>5 emails/min, 10/hour per subscription, no quota increase</td><td class="y">Yes</td></tr>
   <tr><td>13</td><td><code>log-campus-cafe</code></td><td>Log Analytics workspace</td><td>Platform</td><td>30 d retention; daily cap</td><td class="i">Implied</td></tr>
   <tr><td>14</td><td><code>appi-campus-cafe</code></td><td>Application Insights</td><td>Platform</td><td>Workspace-based; logs and failures from the Function App</td><td class="y">Yes</td></tr>
   <tr><td>15</td><td>diagnostic setting</td><td>On the storage queue service</td><td>Platform</td><td>StorageRead / Write / Delete → <code>log-campus-cafe</code></td><td class="i">Implied</td></tr>
   <tr><td>16</td><td>alert rule · metric</td><td>Azure Monitor metric alert</td><td>Platform</td><td>Application Insights failed requests ≥ 1 in 5 min</td><td class="y">Yes</td></tr>
   <tr><td>17</td><td>alert rule · log (optional)</td><td>Azure Monitor log search alert</td><td>Platform</td><td>PutMessage to <code>notify-poison</code> in <code>StorageQueueLogs</code>; no free tier</td><td class="y">Yes</td></tr>
   <tr><td>18</td><td><code>ag-campus-cafe</code></td><td>Action group</td><td>Platform</td><td>Email to the team</td><td class="i">Implied</td></tr>
  </table>
  <div class="note">Globally unique names (<code>func-</code>, <code>st…</code>) get a short suffix. Prefixes follow the Microsoft Cloud Adoption Framework abbreviations.</div>
 </div>
 <div class="blk">
  <h2>Access (RBAC, keyless)</h2>
  <table>
   <tr><th>Principal</th><th>Role</th><th>Scope</th><th>Why</th></tr>
   <tr><td><code>id-campus-cafe-func</code></td><td>Storage Blob Data Owner</td><td><code>stcampuscafe</code></td><td>Functions host (documented minimum for the host storage connection) and deployment container</td></tr>
   <tr><td><code>id-campus-cafe-func</code></td><td>Storage Table Data Contributor</td><td><code>stcampuscafe</code></td><td>Host diagnostic events and the <code>orders</code> table</td></tr>
   <tr><td><code>id-campus-cafe-func</code></td><td>Storage Queue Data Contributor</td><td><code>stcampuscafe</code></td><td>Send and process <code>notify</code>; write <code>notify-poison</code></td></tr>
   <tr><td>Team group</td><td>Contributor</td><td><code>rg-campus-cafe</code></td><td>Deploy and manage</td></tr>
   <tr><td>Team group</td><td>Queue / Table Data Contributor + Blob Data Reader</td><td><code>stcampuscafe</code></td><td>Inspect messages and rows (Contributor alone gives no data access)</td></tr>
  </table>
  <div class="note">The ACS connection string sits in a Function App setting (encrypted at rest). v1 has no Key Vault.</div>
 </div>
 <div class="foot"><span>Campus Café · Infrastructure v1</span><span>Page 2 of 3</span></div>
</section>
"""

PAGE3 = """
<section class="page">
 <div class="hdr"><h1>Telemetry, settings and build order</h1>
  <div class="sub">How the parts talk to each other, what to configure, and the order to build</div></div>
 <div class="cols">
  <div>
   <div class="blk">
    <h2>Telemetry and alerts</h2>
    <table>
     <tr><th>Source</th><th>Sends</th><th>To</th></tr>
     <tr><td>Function App</td><td>requests, traces, exceptions</td><td>Application Insights → <code>log-campus-cafe</code></td></tr>
     <tr><td>Storage queue service</td><td>StorageRead / Write / Delete (<code>StorageQueueLogs</code>)</td><td><code>log-campus-cafe</code></td></tr>
     <tr><td>Metric alert</td><td>failed requests ≥ 1 in 5 min</td><td>Action group → email</td></tr>
     <tr><td>Log alert (optional)</td><td>PutMessage to <code>notify-poison</code></td><td>Action group → email</td></tr>
    </table>
    <div class="note">Queue Message Count is account-wide with hourly grain, so it is not used for alerts.</div>
   </div>
   <div class="blk">
    <h2>Key settings</h2>
    <ul>
     <li>Host storage by identity: <code>AzureWebJobsStorage__accountName</code>, <code>__credential=managedidentity</code>, <code>__clientId</code>.</li>
     <li>Queue and table connections by identity: <code>__queueServiceUri</code>, <code>__tableServiceUri</code> (same <code>__credential</code> and <code>__clientId</code>).</li>
     <li>Queue trigger: 5 tries then <code>notify-poison</code>; <code>visibilityTimeout</code> 30–60 s.</li>
     <li>Function App: HTTPS only, max 5 instances, always-ready 0.</li>
     <li>Flex portal wizard: pick <b>Managed identity</b> on the Authentication page. It creates the user-assigned identity.</li>
    </ul>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>Build order</h2>
    <ol class="steps">
     <li>Resource group, Log Analytics, Application Insights, storage account.</li>
     <li>Function App on Flex (wizard, Managed identity) + role assignments.</li>
     <li>Table <code>orders</code>, queue <code>notify</code>.</li>
     <li><code>SubmitOrder</code> saves to the table. Test in Postman.</li>
     <li><code>SendNotification</code> with <code>EMAIL_MODE=log</code>.</li>
     <li><code>UpdateOrderStatus</code> with status rules.</li>
     <li>ACS: Communication Services, Email service, managed domain. <code>EMAIL_MODE=acs</code>.</li>
     <li>Diagnostic setting, alert rules, action group.</li>
     <li>Budget, then harden (shared-key off, RBAC review).</li>
    </ol>
   </div>
   <div class="blk">
    <h2>Scope and limits</h2>
    <div class="callout"><ul>
     <li>Detail of the v1 data-flow diagram only. No change to design, flow or features.</li>
     <li>Azure-managed email domain: 5 emails/min, 10/hour. ACS Email retires 30 Sep 2028 and Microsoft limits new ACS onboarding from 23 Oct 2026.</li>
     <li>Flex Consumption is Linux only. Pick a region the portal offers.</li>
    </ul></div>
   </div>
  </div>
 </div>
 <div class="blk" style="margin-top:.02in">
  <h2>References and credits</h2>
  <ul class="refs">
   <li><b>Icons:</b> Microsoft Azure Public Service Icons V24, file <code>Azure_Public_Service_Icons_V24.zip</code> (Azure architecture icons, © Microsoft).
   Used unmodified (no crop, flip, rotate or distortion) with the product name beside each icon, for architecture documentation, as the pack's Terms of Use permit.
   Icons used: Users, Subscriptions, Resource Groups, App Service Plans, Function Apps, Storage Accounts, Table, Blob Block, Storage Queue, Azure Communication Services, Application Insights, Log Analytics Workspaces, Diagnostics Settings, Managed Identities, Alerts, Cost Budgets.</li>
   <li><b>Microsoft documentation:</b>
    <a href="https://learn.microsoft.com/en-us/azure/cloud-adoption-framework/ready/azure-best-practices/resource-abbreviations">Resource abbreviations</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/azure-functions/flex-consumption-how-to">Flex Consumption how-to</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections">Functions connections and roles</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/azure-functions/functions-bindings-storage-queue-trigger">Queue trigger</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/storage/queues/monitor-queue-storage-reference">Queue monitoring reference</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/communication-services/concepts/service-limits">ACS service limits</a> ·
    <a href="https://learn.microsoft.com/en-us/azure/communication-services/acs-retirement-and-breaking-changes-guide">ACS retirement guide</a></li>
  </ul>
 </div>
 <div class="foot"><span>Campus Café · Infrastructure v1</span><span>Page 3 of 3</span></div>
</section>
"""

doc = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
       '<title>Campus Café — Infrastructure architecture (detail of v1)</title>'
       '<style>%s</style></head><body>%s%s%s</body></html>'
       % (CSS_DOC, PAGE1.replace("__DIAGRAM__", svg_inline), PAGE2, PAGE3))
(out_dir / "campus-cafe-infrastructure-v1.html").write_text(doc, encoding="utf-8")
print("ok", len(doc), "bytes html;", len(svg_file), "bytes svg")
