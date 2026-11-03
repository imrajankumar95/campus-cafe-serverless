import sys, re, json, pathlib, html

icons_dir = pathlib.Path(sys.argv[1])
md_path = pathlib.Path(sys.argv[2])
out_html = pathlib.Path(sys.argv[3])
svg_dir = pathlib.Path(sys.argv[4])
svg_dir.mkdir(parents=True, exist_ok=True)

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
    "identity": "10227-icon-service-Managed-Identities.svg",
    "alerts": "00002-icon-service-Alerts.svg",
    "budget": "10793-icon-service-Cost-Budgets.svg",
    "kv": "10245-icon-service-Key-Vaults.svg",
    "defender": "10241-icon-service-Microsoft-Defender-for-Cloud.svg",
    "policy": "10316-icon-service-Policy.svg",
    "templates": "10009-icon-service-Templates.svg",
    "vnet": "10061-icon-service-Virtual-Networks.svg",
    "subnet": "02742-icon-service-Subnet.svg",
    "pe": "02579-icon-service-Private-Endpoints.svg",
    "dns": "10064-icon-service-DNS-Zones.svg",
    "nsg": "10067-icon-service-Network-Security-Groups.svg",
    "swa": "01007-icon-service-Static-Apps.svg",
    "groups": "10223-icon-service-Groups.svg",
    "appreg": "10232-icon-service-App-Registrations.svg",
    "activity": "00007-icon-service-Activity-Log.svg",
    "workbook": "10851-icon-service-Workbooks.svg",
    "monitor": "00001-icon-service-Monitor.svg",
}

BLUE, GREEN, ORANGE, PURPLE, DARK, GRAY = "#0F6CBD", "#2A9D78", "#C75B12", "#8764B8", "#323130", "#6B6B6B"
P = "x-"


def esc(s):
    return html.escape(s, quote=False)


def load_symbol(key):
    raw = (icons_dir / ICONS[key]).read_text(encoding="utf-8")
    m = re.search(r"<svg\b[^>]*>(.*)</svg>\s*$", raw, re.S)
    inner = re.sub(r"<title>.*?</title>", "", m.group(1), flags=re.S)
    inner = re.sub(r'id="([^"]+)"', lambda mm: 'id="%s%s"' % (P, mm.group(1)), inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda mm: 'url(#%s%s)' % (P, mm.group(1)), inner)
    return '<symbol id="%sic-%s" viewBox="0 0 18 18">%s</symbol>' % (P, key, inner)


def marker(name, color):
    return ('<marker id="%s%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="9" markerHeight="9" '
            'markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (P, name, color))


CSS_SVG = (
    '.t14{font:600 14px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.t12{font:600 12px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.s11{font:400 11px "Segoe UI",Arial,sans-serif;fill:#4B4B4B}'
    '.g11{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B}'
    '.g11r{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B;text-anchor:end}'
    '.hdr{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E}'
    '.hdrr{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E;text-anchor:end}'
    '.lbl{font:400 11px "Segoe UI",Arial,sans-serif;fill:#323130}'
    '.lblm{font:400 11px "Segoe UI",Arial,sans-serif;fill:#323130;text-anchor:middle}'
)


def icon(key, x, y, size):
    return '<use href="#%sic-%s" x="%s" y="%s" width="%s" height="%s"/>' % (P, key, x, y, size, size)


def text(x, y, s, cls):
    return '<text x="%s" y="%s" class="%s">%s</text>' % (x, y, cls, esc(s))


def rect(x, y, w, h, fill="#FFFFFF", stroke="#C8C6C4", sw=1.2, rx=8, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (
        x, y, w, h, rx, fill, stroke, sw, d)


def path(d, color, mk, dash=None, sw=1.7):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s marker-end="url(#%s%s)"/>' % (d, color, sw, ds, P, mk)


def label_bg(x, y, s, anchor="start"):
    w = len(s) * 5.9 + 8
    x0 = x - 4 if anchor == "start" else x - w / 2
    cls = "lbl" if anchor == "start" else "lblm"
    return rect(x0, y - 11, w, 15, fill="#FFFFFF", stroke="none", sw=0, rx=3) + text(x, y, s, cls)


def chip(x, y, w, h, key, title, sub, stroke="#C8C6C4", fill="#FFFFFF", isz=24):
    ty = y + h / 2 - 2
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.1, rx=7)
            + icon(key, x + 8, y + (h - isz) / 2, isz)
            + text(x + 8 + isz + 8, ty, title, "t12")
            + text(x + 8 + isz + 8, ty + 14, sub, "s11"))


def box(x, y, w, h, key, title, sub, stroke, fill, dash=None, right=True):
    out = rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.2, rx=10, dash=dash)
    if right:
        out += icon(key, x + w - 30, y + 6, 22) + text(x + w - 36, y + 21, title, "hdrr")
        if sub:
            out += text(x + w - 36, y + 35, sub, "g11r")
    else:
        out += icon(key, x + 8, y + 6, 22) + text(x + 36, y + 21, title, "hdr")
        if sub:
            out += text(x + 36, y + 35, sub, "g11")
    return out


def svg(W, H, keys, body, label):
    d = ('<defs><style>%s</style>' % CSS_SVG
         + marker("b", BLUE) + marker("g", GREEN) + marker("o", ORANGE) + marker("p", PURPLE) + marker("k", GRAY)
         + "".join(load_symbol(k) for k in keys) + "</defs>")
    inner = d + '<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H) + "".join(body)
    inline = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>'
              % (W, H, esc(label), inner))
    standalone = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" '
                  'width="%d" height="%d" viewBox="0 0 %d %d">%s</svg>\n' % (W, H, W, H, inner))
    return inline, standalone


# ---------------- Figure: high-level architecture ----------------
def fig_highlevel():
    global P
    P = "h-"
    W, H = 1000, 480
    b = []
    add = b.append
    add(chip(16, 60, 180, 52, "users", "Customer", "browser · phone"))
    add(chip(16, 250, 180, 52, "users", "Café staff", "signed-in tablet"))
    add(chip(236, 150, 200, 56, "swa", "stapp-cafe", "Static Web Apps · order page", stroke="#8FB6E3"))
    add(chip(236, 330, 200, 56, "appreg", "Microsoft Entra ID", "staff sign-in · role Cafe.Staff", stroke=PURPLE))

    add(box(476, 36, 262, 336, "func", "func-cafe-cc", "Flex Consumption · managed identity", BLUE, "#F4F9FE"))
    fns = [("SubmitOrder", "HTTP POST · validate · rate limit"),
           ("GetOrderStatus", "HTTP GET · status only"),
           ("UpdateOrderStatus", "HTTP PUT · staff role only"),
           ("SendNotification", "Queue trigger · exactly once"),
           ("NightlyMaintenance", "Timer · backup · purge")]
    for i, (t, s) in enumerate(fns):
        add(chip(488, 82 + i * 56, 238, 48, "func", t, s, stroke="#8FB6E3", isz=22))

    add(box(778, 36, 206, 196, "storage", "stcafecc", "GZRS · keyless · private", GREEN, "#ECF7F3"))
    add(chip(790, 80, 182, 44, "table", "Tables", "orders · ratelimits", stroke=GREEN, isz=22))
    add(chip(790, 130, 182, 44, "queue", "Queue", "notify · notify-poison", stroke=GREEN, isz=22))
    add(chip(790, 180, 182, 44, "blob", "Blobs", "deployments · backups", stroke=GREEN, isz=22))
    add(chip(778, 262, 206, 56, "acs", "acs-cafe", "Communication Services Email", stroke=PURPLE))
    add(chip(778, 350, 206, 50, "users", "Customer inbox", "Accepted · Preparing · Ready"))

    add(box(236, 410, 748, 56, "monitor", "Azure Monitor", "", GRAY, "#FAFAFA", right=False))
    add(chip(420, 416, 176, 44, "insights", "appi-cafe-cc", "Application Insights", isz=22))
    add(chip(606, 416, 176, 44, "law", "log-cafe-cc", "Log Analytics", isz=22))
    add(chip(792, 416, 184, 44, "alerts", "ag-cafe-ops", "alerts → team email", isz=22))

    add(path("M196 86 H216 V170 H234", BLUE, "b"))
    add(path("M196 276 H216 V188 H234", BLUE, "b"))
    add(path("M106 302 V358 H234", PURPLE, "p"))
    add(path("M436 178 H474", BLUE, "b"))
    add(label_bg(455, 170, "HTTPS", "middle"))
    add(path("M436 358 H456 V300 H474", PURPLE, "p", dash="5 3"))
    add(label_bg(390, 400, "token check", "middle"))
    add(path("M738 104 H776", GREEN, "g"))
    add(path("M776 152 H740", GREEN, "g"))
    add(label_bg(757, 168, "trigger", "middle"))
    add(path("M738 290 H776", PURPLE, "p"))
    add(path("M881 318 V348", PURPLE, "p"))
    add(path("M607 372 V408", GRAY, "k", dash="4 3"))
    add(label_bg(640, 394, "telemetry"))
    return svg(W, H, ["users", "swa", "appreg", "func", "storage", "table", "queue", "blob", "acs",
                      "monitor", "insights", "law", "alerts"], b, "High-level application architecture")


# ---------------- Figure: infrastructure layout ----------------
def fig_infra():
    global P
    P = "i-"
    W, H = 1000, 700
    b = []
    add = b.append
    add(rect(6, 6, 988, 688, fill="none", stroke=GRAY, sw=1, rx=14, dash="7 4"))
    add(icon("sub", 18, 14, 22) + text(46, 30, "Subscription · Azure for Students · subscription-wide guardrails", "hdr"))
    gov = [("policy", "Azure Policy", "9 assignments"), ("budget", "Budget", "$40 · 50/80/100%"),
           ("defender", "Defender for Cloud", "free tier · secure score"), ("activity", "Activity Log", "→ Log Analytics"),
           ("groups", "Entra groups", "staff · admins · devs")]
    for i, (k, t, s) in enumerate(gov):
        add(chip(18 + i * 194, 44, 186, 44, k, t, s, isz=22))

    # app resource group
    add(box(18, 100, 624, 586, "rg", "rg-cafe-app-cc", "Canada Central · workload", GRAY, "none", dash="5 3"))
    add(box(30, 140, 290, 176, "plan", "Compute", "", BLUE, "#F4F9FE", right=False))
    add(chip(42, 172, 266, 42, "plan", "asp-cafe-cc", "Flex Consumption FC1 · Linux", stroke="#8FB6E3", isz=22))
    add(chip(42, 220, 266, 42, "func", "func-cafe-cc", "5 functions · HTTPS only · TLS 1.2", stroke="#8FB6E3", isz=22))
    add(chip(42, 268, 266, 42, "identity", "id-cafe-func", "user-assigned managed identity", stroke="#8FB6E3", isz=22))
    add(box(332, 140, 298, 176, "swa", "Web & email", "", PURPLE, "#F7F4FC", right=False))
    add(chip(344, 172, 274, 42, "swa", "stapp-cafe", "Static Web Apps (Free)", stroke="#B8A9D9", isz=22))
    add(chip(344, 220, 274, 42, "acs", "acs-cafe", "Communication Services", stroke="#B8A9D9", isz=22))
    add(chip(344, 268, 274, 42, "acs", "ecs-cafe", "Email Service · data in Canada", stroke="#B8A9D9", isz=22))

    add(box(30, 328, 600, 184, "vnet", "vnet-cafe-cc · 10.20.0.0/24", "", "#5C8DC4", "#F2F7FC", right=False))
    add(rect(42, 368, 250, 132, fill="#FFFFFF", stroke="#8FB6E3", rx=8))
    add(icon("subnet", 50, 374, 20) + text(76, 389, "snet-func · 10.20.0.0/27", "t12"))
    add(text(52, 412, "Delegated: Microsoft.App/environments", "s11"))
    add(text(52, 430, "Function App outbound (VNet integration)", "s11"))
    add(text(52, 448, "No endpoints allowed in this subnet", "s11"))
    add(icon("func", 52, 460, 22) + text(80, 476, "func-cafe-cc", "s11"))
    add(rect(304, 368, 314, 132, fill="#FFFFFF", stroke="#8FB6E3", rx=8))
    add(icon("subnet", 312, 374, 20) + text(338, 389, "snet-pe · 10.20.0.32/27", "t12"))
    add(icon("nsg", 586, 372, 22))
    add(chip(314, 400, 146, 40, "pe", "pe blob", "→ stcafecc", isz=20))
    add(chip(464, 400, 146, 40, "pe", "pe queue", "→ stcafecc", isz=20))
    add(chip(314, 448, 146, 40, "pe", "pe table", "→ stcafecc", isz=20))
    add(chip(464, 448, 146, 40, "pe", "pe vault", "→ kv-cafe-cc", isz=20))

    add(box(30, 524, 430, 150, "storage", "stcafecc · Standard GZRS", "", GREEN, "#ECF7F3", right=False))
    add(text(38, 562, "public access off · shared key off · CanNotDelete lock", "g11"))
    add(chip(40, 574, 134, 90, "table", "Tables", "orders", stroke=GREEN, isz=22))
    add(text(72, 646, "ratelimits", "s11"))
    add(chip(182, 574, 134, 90, "queue", "Queue", "notify", stroke=GREEN, isz=22))
    add(text(214, 646, "notify-poison", "s11"))
    add(chip(324, 574, 126, 90, "blob", "Blobs", "deployments", stroke=GREEN, isz=22))
    add(text(356, 646, "backups (WORM)", "s11"))
    add(box(472, 524, 158, 150, "dns", "Private DNS", "", "#5C8DC4", "#F2F7FC", right=False))
    for i, z in enumerate(["privatelink.blob", "privatelink.queue", "privatelink.table", "privatelink.vaultcore"]):
        add(text(484, 568 + i * 18, z, "s11"))
    add(text(484, 650, "linked to vnet-cafe-cc", "g11"))

    # shared resource group
    add(box(656, 100, 326, 336, "rg", "rg-cafe-shared-cc", "Canada Central · delete lock", GRAY, "none", dash="5 3"))
    sh = [("kv", "kv-cafe-cc", "Key Vault · RBAC · purge protection"),
          ("law", "log-cafe-cc", "Log Analytics · 30 days · daily cap"),
          ("insights", "appi-cafe-cc", "Application Insights"),
          ("alerts", "ag-cafe-ops", "action group + 8 alert rules"),
          ("workbook", "Operations workbook", "orders · latency · emails")]
    for i, (k, t, s) in enumerate(sh):
        add(chip(668, 148 + i * 56, 302, 48, k, t, s))

    # DR resource group
    add(box(656, 450, 326, 236, "rg", "rg-cafe-dr-ce", "Canada East · recovery region", ORANGE, "#FDF6F0", dash="5 3"))
    add(chip(668, 498, 302, 48, "templates", "Bicep redeploy target", "empty until a drill or failover", stroke="#E5B48A"))
    add(chip(668, 554, 302, 48, "storage", "GZRS secondary copy", "Microsoft-managed · used on failover", stroke="#E5B48A"))
    add(text(670, 626, "Same templates, dr.ce.bicepparam", "s11"))
    add(text(670, 644, "RTO ≤ 4 h · RPO minutes (targets)", "s11"))

    add(text(670, 664, "Receives stcafecc geo-replication", "s11"))
    add(path("M420 674 V681 H654", ORANGE, "o", dash="6 4"))
    return svg(W, H, ["sub", "policy", "budget", "defender", "activity", "groups", "rg", "plan", "func", "identity",
                      "swa", "acs", "vnet", "subnet", "nsg", "pe", "storage", "table", "queue", "blob", "dns", "kv",
                      "law", "insights", "alerts", "workbook", "templates"], b, "Infrastructure layout")


# ---------------- Figure: network topology ----------------
def fig_network():
    global P
    P = "n-"
    W, H = 1000, 540
    b = []
    add = b.append
    add(chip(16, 104, 170, 56, "users", "Internet", "customers · staff · 443"))
    add(chip(236, 20, 210, 56, "swa", "stapp-cafe", "public HTTPS · global", stroke="#B8A9D9"))
    add(chip(236, 104, 210, 56, "func", "func-cafe-cc", "public HTTPS · CORS: stapp", stroke="#8FB6E3"))
    add(chip(790, 104, 194, 56, "acs", "acs-cafe", "Communication Services", stroke="#B8A9D9"))

    add(box(206, 200, 560, 326, "vnet", "vnet-cafe-cc · 10.20.0.0/24 · Canada Central", "", "#5C8DC4", "#F2F7FC", right=False))
    add(rect(220, 244, 228, 124, fill="#FFFFFF", stroke="#8FB6E3", rx=8))
    add(icon("subnet", 228, 250, 20) + text(254, 265, "snet-func · 10.20.0.0/27", "t12"))
    add(text(230, 290, "Delegated to", "s11"))
    add(text(230, 306, "Microsoft.App/environments", "s11"))
    add(text(230, 330, "Function App outbound traffic", "s11"))
    add(text(230, 348, "(VNet integration)", "s11"))
    add(rect(468, 244, 286, 270, fill="#FFFFFF", stroke="#8FB6E3", rx=8))
    add(icon("subnet", 476, 250, 20) + text(502, 265, "snet-pe · 10.20.0.32/27", "t12"))
    add(icon("nsg", 722, 248, 22))
    add(text(478, 288, "NSG: allow 443 from snet-func only", "g11"))
    pes = [("pe blob", "privatelink.blob"), ("pe queue", "privatelink.queue"),
           ("pe table", "privatelink.table"), ("pe vault", "privatelink.vaultcore")]
    for i, (t, s) in enumerate(pes):
        add(chip(480, 300 + i * 52, 262, 44, "pe", t, s, isz=22))
    add(chip(220, 384, 228, 60, "dns", "Private DNS zones ×4", "linked · resolve to private IPs", stroke="#8FB6E3"))
    add(rect(220, 456, 228, 58, fill="#FFFFFF", stroke="#C8C6C4", rx=8, dash="4 3"))
    add(text(230, 478, "10.20.0.64/26 + 10.20.0.128/25", "s11"))
    add(text(230, 496, "reserved for growth", "g11"))

    add(chip(800, 300, 184, 96, "storage", "stcafecc", "public access: off", stroke=GREEN))
    add(text(842, 382, "table · queue · blob", "s11"))
    add(chip(800, 448, 184, 56, "kv", "kv-cafe-cc", "public access: off", stroke=GREEN))

    add(path("M186 124 H210 V48 H234", PURPLE, "p"))
    add(path("M186 138 H234", BLUE, "b"))
    add(path("M340 160 V242", BLUE, "b"))
    add(label_bg(350, 186, "outbound"))
    add(path("M448 306 H478", BLUE, "b"))
    add(path("M742 348 H798", GREEN, "g"))
    add(label_bg(770, 340, "private link", "middle"))
    add(path("M742 478 H798", GREEN, "g"))
    add(path("M446 124 H788", PURPLE, "p"))
    add(label_bg(617, 116, "HTTPS · managed identity token", "middle"))
    add(rect(790, 180, 194, 98, fill="#FFF8E6", stroke="#E3C46F", rx=8))
    add(text(800, 200, "Admin break-glass", "t12"))
    add(text(800, 218, "adminIpAllowList parameter", "s11"))
    add(text(800, 234, "opens one team IP briefly", "s11"))
    add(text(800, 250, "logged + alerted", "s11"))
    return svg(W, H, ["users", "swa", "func", "acs", "vnet", "subnet", "nsg", "pe", "dns", "storage", "kv"],
               b, "Network topology")


FIGS = [
    ("high-level-architecture", fig_highlevel, "Figure 1 · High-level application architecture"),
    ("infrastructure-layout", fig_infra, "Figure 2 · Infrastructure layout: subscription, resource groups and resources"),
    ("network-topology", fig_network, "Figure 3 · Network topology: private data plane, public API"),
]
built = {}
for name, fn, cap in FIGS:
    inline, standalone = fn()
    (svg_dir / ("Campus-Cafe-v5-%s.svg" % name)).write_text(standalone, encoding="utf-8")
    built[name] = '<figure class="fig">%s<figcaption>%s</figcaption></figure>' % (inline, esc(cap))

md = md_path.read_text(encoding="utf-8")
md = re.sub(r"\n## Appendix A.*?(?=\n\*References)", "\n", md, flags=re.S)
md = md.replace("> Draft for review. Diagrams are rough Mermaid sketches; the final PDF will redraw them with official Azure icons.\n",
                "> Prepared by Group 6 for the Work Integrated Project review.\n")
md = re.sub(r"^---\s*$", "", md, flags=re.M)

built["status-strip"] = (
    '<div class="strip"><span class="st">Customer submits</span><span class="ar">→</span>'
    '<span class="st on">Accepted<small>email</small></span><span class="ar">→ staff →</span>'
    '<span class="st on">Preparing<small>email</small></span><span class="ar">→ staff →</span>'
    '<span class="st on">Ready for Pickup<small>email</small></span><span class="ar">→ staff →</span>'
    '<span class="st end">Collected<small>closed · no email</small></span></div>')
blocks = list(re.finditer(r"```mermaid\n(.*?)```", md, re.S))
replace_at = {0: "status-strip", 2: "high-level-architecture", 3: "infrastructure-layout", 4: "network-topology"}
out, last = [], 0
for i, m in enumerate(blocks):
    out.append(md[last:m.start()])
    if i in replace_at:
        out.append("\n" + built[replace_at[i]] + "\n")
    else:
        out.append(m.group(0))
    last = m.end()
out.append(md[last:])
md = "".join(out)
md += ("\n\n<p class=\"credit\"><b>Icon credit:</b> Microsoft Azure Public Service Icons V24 "
       "(Azure_Public_Service_Icons_V24.zip, © Microsoft), used unmodified with product names for architecture "
       "documentation as the pack's terms permit.</p>\n")

HTML = """<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">
<title>Campus Café — Serverless Order Tracking · Proposal</title>
<style>
@page{size:Letter;margin:.55in .6in .6in}
body{font-family:"Segoe UI",Arial,sans-serif;color:#201F1E;font-size:9.4pt;line-height:1.42;
 -webkit-print-color-adjust:exact;print-color-adjust:exact;max-width:7.3in;margin:0 auto}
h1{font-size:22pt;margin:0 0 .05in;font-weight:600;color:#0F3F75;border-bottom:3px solid #0F6CBD;padding-bottom:.06in}
h2{font-size:13pt;margin:.26in 0 .08in;padding-left:.09in;border-left:4px solid #0F6CBD;font-weight:600;break-after:avoid}
.strip{display:flex;flex-wrap:wrap;align-items:center;gap:6px;margin:.08in 0 .1in;break-inside:avoid}
.st{border:1px solid #C8C6C4;border-radius:8px;padding:5px 10px;font-weight:600;font-size:9pt;background:#FAFAFA;text-align:center}
.st small{display:block;font-weight:400;font-size:7.5pt;color:#605E5C}
.st.on{border-color:#0F6CBD;background:#EAF3FC;color:#0F3F75}
.st.end{border-color:#2A9D78;background:#ECF7F3;color:#1B6B52}
.ar{color:#6B6B6B;font-size:8.5pt}
h3{font-size:10.5pt;margin:.14in 0 .05in;color:#0F3F75;break-after:avoid}
p{margin:.04in 0 .07in}
blockquote{margin:.08in 0;padding:.05in .14in;border-left:3px solid #C7E0F4;background:#EFF6FC;color:#0B4F8A}
blockquote p{margin:.02in 0}
table{border-collapse:collapse;width:100%;font-size:8.2pt;margin:.06in 0 .1in}
tr{break-inside:avoid}
th{background:#EAF3FC;text-align:left;padding:3px 6px;border-bottom:1px solid #8FB6E3}
td{padding:3px 6px;border-bottom:1px solid #E1DFDD;vertical-align:top}
code{font-family:Consolas,monospace;font-size:.88em;background:#F3F2F1;padding:0 3px;border-radius:3px}
pre{background:#F7F7F7;border:1px solid #E1DFDD;border-radius:6px;padding:.08in;font-size:7.8pt;break-inside:avoid}
pre code{background:none;padding:0}
ul,ol{margin:.03in 0 .08in;padding-left:1.3em}
li{margin-bottom:.02in}
.fig{margin:.08in 0 .12in;text-align:center;break-inside:avoid}
.fig svg{width:100%;height:auto;max-height:7.6in;border:1px solid #E1DFDD;border-radius:6px}
figcaption{font-size:8pt;color:#605E5C;margin-top:.04in}
.mermaid{text-align:center;margin:.08in 0;break-inside:avoid}
.mermaid svg{max-width:100%;height:auto;max-height:4.6in}
.credit{font-size:7.8pt;color:#605E5C;margin-top:.2in;border-top:1px solid #E1DFDD;padding-top:.06in}
em{color:#605E5C}
input[type=checkbox]{margin-right:4px}
</style></head><body><div id="c"></div>
<script src="https://cdn.jsdelivr.net/npm/marked@12.0.2/marked.min.js"></script>
<script src="https://cdn.jsdelivr.net/npm/mermaid@10.9.1/dist/mermaid.min.js"></script>
<script>
const md = __MD__;
const r = new marked.Renderer();
const baseCode = r.code.bind(r);
r.code = function(code, lang){ if(lang==='mermaid'){ return '<div class="mermaid">'+code+'</div>'; } return baseCode(code, lang); };
document.getElementById('c').innerHTML = marked.parse(md, {renderer: r});
mermaid.initialize({startOnLoad:false, theme:'neutral', flowchart:{htmlLabels:true, useMaxWidth:true}, sequence:{useMaxWidth:true}, fontFamily:'Segoe UI, Arial'});
mermaid.run({querySelector:'.mermaid'}).then(()=>{document.body.setAttribute('data-done','1');});
</script></body></html>"""
out_html.write_text(HTML.replace("__MD__", json.dumps(md)), encoding="utf-8")
print("ok", len(blocks), "mermaid blocks;", len(replace_at), "replaced with icon figures")
