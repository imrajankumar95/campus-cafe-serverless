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
    "kv": "10245-icon-service-Key-Vaults.svg",
    "defender": "10241-icon-service-Microsoft-Defender-for-Cloud.svg",
    "policy": "10316-icon-service-Policy.svg",
    "health": "10004-icon-service-Service-Health.svg",
    "templates": "10009-icon-service-Templates.svg",
}

BLUE, ORANGE, DARK, GRAY = "#0F6CBD", "#C75B12", "#323130", "#6B6B6B"
PHASE = {
    "v1": ("#F4F3EF", "#B4B2A9", None),
    "NOW": ("#E1F5EE", "#1D9E75", "#1D9E75"),
    "NEXT": ("#FAEEDA", "#BA7517", "#BA7517"),
    "LATER": ("#EEEDFE", "#7F77DD", "#7F77DD"),
}
P = "a-"


def esc(s):
    return html.escape(s, quote=False)


def load_symbol(key, fname):
    raw = (icons_dir / fname).read_text(encoding="utf-8")
    m = re.search(r"<svg\b[^>]*>(.*)</svg>\s*$", raw, re.S)
    inner = re.sub(r"<title>.*?</title>", "", m.group(1), flags=re.S)
    inner = re.sub(r'id="([^"]+)"', lambda mm: 'id="%s%s"' % (P, mm.group(1)), inner)
    inner = re.sub(r'url\(#([^)]+)\)', lambda mm: 'url(#%s%s)' % (P, mm.group(1)), inner)
    return '<symbol id="%sic-%s" viewBox="0 0 18 18">%s</symbol>' % (P, key, inner)


def marker(name, color):
    return ('<marker id="%s%s" viewBox="0 0 10 10" refX="9" refY="5" markerWidth="10" markerHeight="10" '
            'markerUnits="userSpaceOnUse" orient="auto"><path d="M0 0L10 5L0 10z" fill="%s"/></marker>' % (P, name, color))


def icon(key, x, y, size):
    return '<use href="#%sic-%s" x="%s" y="%s" width="%s" height="%s"/>' % (P, key, x, y, size, size)


def text(x, y, s, cls):
    return '<text x="%s" y="%s" class="%s">%s</text>' % (x, y, cls, esc(s))


def rect(x, y, w, h, fill="#FFFFFF", stroke="#C8C6C4", sw=1.2, rx=8, dash=None):
    d = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<rect x="%s" y="%s" width="%s" height="%s" rx="%s" fill="%s" stroke="%s" stroke-width="%s"%s/>' % (
        x, y, w, h, rx, fill, stroke, sw, d)


def path(d, color, mk, dash=None, sw=1.8):
    ds = ' stroke-dasharray="%s"' % dash if dash else ""
    return '<path d="%s" fill="none" stroke="%s" stroke-width="%s"%s marker-end="url(#%s%s)"/>' % (d, color, sw, ds, P, mk)


def badge(cx, cy, n, color):
    return ('<circle cx="%s" cy="%s" r="10" fill="%s" stroke="#FFFFFF" stroke-width="1.5"/>' % (cx, cy, color)
            + '<text x="%s" y="%s" class="num">%s</text>' % (cx, cy + 4.2, n))


def pill(x, y, phase):
    col = PHASE[phase][2]
    return (rect(x, y, 42, 14, fill=col, stroke="#FFFFFF", sw=1, rx=7)
            + '<text x="%s" y="%s" class="pill">%s</text>' % (x + 21, y + 10.2, phase))


def chip(x, y, w, h, key, title, sub, stroke="#C8C6C4", fill="#FFFFFF", isz=22):
    ty = y + h // 2 - 2
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.1, rx=7)
            + icon(key, x + 8, y + (h - isz) / 2, isz)
            + text(x + 8 + isz + 7, ty, title, "t12")
            + text(x + 8 + isz + 7, ty + 15, sub, "s11"))


def chip3(x, y, w, h, key, title, l1, l2, stroke="#C8C6C4", fill="#FFFFFF"):
    return (rect(x, y, w, h, fill=fill, stroke=stroke, sw=1.1, rx=7)
            + icon(key, x + 9, y + (h - 28) / 2, 28)
            + text(x + 46, y + 20, title, "t12")
            + text(x + 46, y + 36, l1, "s11")
            + text(x + 46, y + 51, l2, "s11"))


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
    '.pill{font:700 8.5px "Segoe UI",Arial,sans-serif;fill:#fff;text-anchor:middle;letter-spacing:.04em}'
    '.lbl{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130}'
    '.lblr{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130;text-anchor:end}'
    '.lblm{font:400 11.5px "Segoe UI",Arial,sans-serif;fill:#323130;text-anchor:middle}'
    '.hdrr{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E;text-anchor:end}'
    '.hdrm{font:600 13px "Segoe UI",Arial,sans-serif;fill:#201F1E;text-anchor:middle}'
    '.g11r{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B;text-anchor:end}'
    '.g11m{font:400 11px "Segoe UI",Arial,sans-serif;fill:#6B6B6B;text-anchor:middle}'
)


def defs(keys):
    return ('<defs><style>%s</style>' % CSS_SVG
            + marker("ah-blue", BLUE) + marker("ah-orange", ORANGE) + marker("ah-dark", DARK) + marker("ah-gray", GRAY)
            + "".join(load_symbol(k, ICONS[k]) for k in keys) + "</defs>")


def wrap(W, H, body, label):
    inline = ('<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 %d %d" role="img" aria-label="%s">%s</svg>'
              % (W, H, esc(label), body))
    standalone = ('<?xml version="1.0" encoding="UTF-8"?>\n<svg xmlns="http://www.w3.org/2000/svg" width="%d" height="%d" '
                  'viewBox="0 0 %d %d">%s</svg>\n' % (W, H, W, H, body))
    return inline, standalone


# ---------------- Diagram A: architecture with security additions ----------------
def build_arch():
    global P
    P = "a-"
    W, H = 1000, 752
    s = [defs(["users", "sub", "rg", "plan", "func", "storage", "table", "blob", "queue", "acs", "insights",
               "law", "diag", "identity", "alerts", "budget", "kv", "defender", "policy", "health"])]
    add = s.append
    add('<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))
    add(rect(92, 8, 200, 52))
    add(icon("users", 102, 18, 32) + text(144, 31, "Customer", "t14") + text(144, 48, "Browser or Postman", "s11"))
    add(rect(334, 8, 200, 52))
    add(icon("users", 344, 18, 32) + text(386, 31, "Café staff", "t14") + text(386, 48, "Entra sign-in (next)", "s11"))
    add(pill(486, 1, "NEXT"))

    add(rect(4, 70, 992, 674, fill="none", stroke="#6B6B6B", sw=1, rx=14, dash="7 4"))
    add(text(962, 88, "Subscription · Azure for Students", "hdrr") + icon("sub", 968, 74, 22))
    add(rect(14, 98, 822, 636, fill="none", stroke="#6B6B6B", sw=1.2, rx=12, dash="5 3"))
    add(text(804, 113, "Resource group · rg-campus-cafe", "hdrr") + icon("rg", 810, 98, 22))
    add(text(804, 128, "Canada Central (primary) · delete locks", "g11r"))

    add(rect(44, 140, 780, 204, fill="#FAFAFA", stroke="#C8C6C4", sw=1, rx=10))
    add(text(56, 157, "Compute", "t13"))
    add(rect(54, 164, 760, 172, fill="#F4F9FE", stroke=BLUE, sw=1.1, rx=10, dash="5 3"))
    add(text(776, 183, "asp-campus-cafe", "hdrr") + icon("plan", 782, 166, 24))
    add(text(776, 199, "App Service plan · Flex Consumption (FC1) · Linux", "g11r"))
    add(rect(66, 208, 736, 122, fill="#EAF3FC", stroke=BLUE, sw=1.3, rx=10))
    add(text(766, 226, "func-campus-cafe", "hdrr") + icon("func", 772, 210, 24))
    add(text(766, 242, "Function App · max 5 instances · identity id-campus-cafe-func", "g11r"))
    add(fn_card(76, 252, "SubmitOrder", "HTTP trigger · anonymous", "validate · throttle · enqueue"))
    add(fn_card(318, 252, "UpdateOrderStatus", "HTTP trigger · key → Entra (next)", "check status · save · enqueue"))
    add(fn_card(560, 252, "SendNotification", "Queue trigger · notify", "template · send · mark notified"))

    add(rect(44, 374, 516, 170, fill="#FAFAFA", stroke="#C8C6C4", sw=1, rx=10))
    add(text(56, 391, "Data", "t13"))
    add(rect(52, 400, 500, 136, fill="#ECF7F3", stroke="#2A9D78", sw=1.3, rx=10))
    add(pill(502, 393, "NOW"))
    add(icon("storage", 62, 405, 24) + text(94, 421, "stcampuscafe", "t13"))
    add(text(94, 436, "Storage account · Standard GZRS · TLS 1.2 · keyless", "g11"))
    add(svc_chip(62, 446, 156, 82, "table", "Table service", "orders", "PK date · RK orderId", "#2A9D78"))
    add(svc_chip(224, 446, 156, 82, "blob", "Blob service", "host state", "deployment package", "#2A9D78"))
    add(svc_chip(386, 446, 156, 82, "queue", "Queue service", "notify", "notify-poison (auto)", "#2A9D78"))

    add(rect(584, 374, 240, 170, fill="#F7F4FC", stroke="#B8A9D9", sw=1, rx=10))
    add(text(596, 391, "Email", "t13"))
    add(chip(594, 400, 220, 42, "acs", "acs-campus-cafe", "Communication Services", stroke="#B8A9D9"))
    add(chip(594, 448, 220, 42, "acs", "ecs-campus-cafe", "Email Communication Service", stroke="#B8A9D9"))
    add(chip(594, 496, 220, 42, "acs", "Azure-managed domain", "cap 5/min · 10/hour", stroke="#B8A9D9"))

    add(rect(858, 384, 130, 96))
    add('<rect x="905" y="398" width="36" height="25" rx="3" fill="#FFFFFF" stroke="#6B6B6B" stroke-width="1.6"/>'
        '<path d="M906 400 L923 413 L940 400" fill="none" stroke="#6B6B6B" stroke-width="1.6" stroke-linejoin="round"/>')
    add(text(923, 448, "Customer inbox", "hdrm") + text(923, 465, "3 status emails", "g11m"))

    add(rect(858, 548, 130, 104, fill="#FFFFFF", stroke=GRAY, sw=1.1, rx=8, dash="5 3"))
    add(text(923, 570, "Canada East", "hdrm"))
    add(text(923, 588, "DR region", "g11m"))
    add(text(923, 604, "geo-copy of storage", "g11m"))
    add(text(923, 620, "+ pilot-light app", "g11m"))
    add(text(923, 638, "see page 3", "g11m"))
    add(path("M836 600 L856 600", GRAY, "ah-gray", dash="5 4", sw=1.5))

    add(rect(44, 552, 780, 174, fill="#F8F8F8", stroke="#BDBDBD", sw=1, rx=10))
    add(text(56, 568, "Platform services · monitoring, security, cost", "t13"))
    add(chip(54, 574, 184, 40, "insights", "Application Insights", "appi-campus-cafe", stroke="#BDBDBD"))
    add(chip(246, 574, 184, 40, "diag", "Diagnostic setting", "queue service → log", stroke="#BDBDBD"))
    add(chip(438, 574, 184, 40, "identity", "Managed identity", "id-campus-cafe-func", stroke="#BDBDBD"))
    add(chip(630, 574, 184, 40, "law", "Log Analytics", "log-campus-cafe · 30 d", stroke="#BDBDBD"))
    add(chip(54, 620, 184, 40, "alerts", "Alert rule · metric", "failed requests ≥ 1", stroke="#BDBDBD"))
    add(chip(246, 620, 184, 40, "alerts", "Alert rule · log", "poison message (opt.)", stroke="#BDBDBD"))
    add(chip(438, 620, 184, 40, "alerts", "Action group", "ag-campus-cafe · email", stroke="#BDBDBD"))
    add(chip(630, 620, 184, 40, "budget", "Cost budget", "budget-campus-cafe · $5", stroke="#BDBDBD"))
    add(chip(54, 676, 184, 40, "kv", "Key Vault", "ACS secret · soft delete", stroke=PHASE["NEXT"][1], fill=PHASE["NEXT"][0]))
    add(chip(246, 676, 184, 40, "defender", "Defender for Cloud", "free tier · secure score", stroke=PHASE["NOW"][1], fill=PHASE["NOW"][0]))
    add(chip(438, 676, 184, 40, "policy", "Azure Policy + locks", "Canada only, TLS, tags", stroke=PHASE["NOW"][1], fill=PHASE["NOW"][0]))
    add(chip(630, 676, 184, 40, "health", "Health alerts", "Azure outage notices", stroke=PHASE["NOW"][1], fill=PHASE["NOW"][0]))
    add(pill(192, 669, "NEXT") + pill(384, 669, "NOW") + pill(576, 669, "NOW") + pill(768, 669, "NOW"))

    add(path("M192 60 L192 250", BLUE, "ah-blue"))
    add(path("M192 322 L192 398", BLUE, "ah-blue"))
    add(path("M434 60 L434 250", ORANGE, "ah-orange"))
    add(path("M434 322 L434 398", ORANGE, "ah-orange"))
    add(path("M464 446 L464 362 L640 362 L640 324", DARK, "ah-dark"))
    add(path("M720 324 L720 398", DARK, "ah-dark"))
    add(path("M824 432 L856 432", DARK, "ah-dark"))
    add(path("M66 290 L29 290 L29 594 L52 594", GRAY, "ah-gray", dash="5 4", sw=1.5))
    add(path("M500 574 L500 538", GRAY, "ah-gray", dash="5 4", sw=1.5))
    add(path("M338 538 L338 572", GRAY, "ah-gray", dash="5 4", sw=1.5))
    add(text(348, 562, "diagnostic logs", "g11"))
    add(text(510, 562, "RBAC roles, no keys", "g11"))
    add(badge(208, 120, 1, BLUE) + text(224, 124, "POST /api/orders", "lbl"))
    add(badge(208, 359, 2, BLUE) + text(224, 363, "save + enqueue", "lbl"))
    add(badge(450, 120, 3, ORANGE) + text(466, 124, "PUT /status", "lbl"))
    add(badge(418, 359, 4, ORANGE) + text(406, 363, "save + enqueue", "lblr"))
    add(badge(500, 362, 5, DARK) + text(516, 356, "queue trigger", "lbl"))
    add(badge(738, 360, 6, DARK) + text(754, 364, "send email", "lbl"))
    add(badge(841, 417, 7, DARK))
    return wrap(W, H, "".join(s), "Campus Café architecture with security additions")


# ---------------- Diagram B: disaster recovery ----------------
def build_dr():
    global P
    P = "d-"
    W, H = 1000, 410
    s = [defs(["users", "func", "kv", "storage", "health", "templates"])]
    add = s.append
    add('<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))
    add(rect(390, 8, 220, 46))
    add(icon("users", 400, 15, 30) + text(440, 28, "Clients", "t13") + text(440, 44, "Postman or browser", "s11"))
    add(path("M390 31 L135 31 L135 122", BLUE, "ah-blue"))
    add(path("M610 31 L865 31 L865 122", BLUE, "ah-blue", dash="6 4"))
    add(text(150, 50, "normal traffic", "lbl"))
    add(text(700, 50, "after failover (new URL)", "lbl"))

    add(rect(16, 72, 454, 228, fill="#F4F9FE", stroke="#6B6B6B", sw=1.1, rx=12, dash="6 4"))
    add(text(246, 92, "Canada Central · primary", "hdrm"))
    add(text(246, 108, "rg-campus-cafe · delete locks", "g11m"))
    add(rect(530, 72, 454, 228, fill="#FBF8F1", stroke="#6B6B6B", sw=1.1, rx=12, dash="6 4"))
    add(text(754, 92, "Canada East · DR region", "hdrm"))
    add(text(754, 108, "rg-campus-cafe-dr · built by Bicep", "g11m"))

    v1, now, nxt = PHASE["v1"], PHASE["NOW"], PHASE["NEXT"]
    add(chip3(30, 124, 210, 60, "func", "Function App · live", "3 functions", "max 5 instances", stroke=v1[1], fill="#FFFFFF"))
    add(chip3(252, 124, 210, 60, "kv", "Key Vault", "ACS connection secret", "soft delete on", stroke=nxt[1], fill=nxt[0]))
    add(chip3(30, 200, 210, 60, "health", "Health alerts", "Service + Resource Health", "email the team", stroke=now[1], fill=now[0]))
    add(chip3(252, 200, 210, 60, "storage", "Storage account · GZRS", "table, queue, blob", "zone + geo redundant", stroke=now[1], fill=now[0]))
    add(chip3(538, 124, 210, 60, "kv", "Key Vault · DR", "same ACS secret", "set by runbook", stroke=nxt[1], fill=nxt[0]))
    add(chip3(760, 124, 210, 60, "func", "Function App · pilot light", "code deployed, stopped", "about $0 while idle", stroke=nxt[1], fill=nxt[0]))
    add(chip3(538, 200, 210, 60, "storage", "Storage · geo copy", "async copy of all data", "writable after failover", stroke=now[1], fill=now[0]))
    add(chip3(760, 200, 210, 60, "storage", "Backup storage", "nightly table export", "soft delete + versions", stroke=nxt[1], fill=nxt[0]))
    add(pill(414, 117, "NEXT") + pill(192, 193, "NOW") + pill(414, 193, "NOW"))
    add(pill(700, 117, "NEXT") + pill(922, 117, "NEXT") + pill(700, 193, "NOW") + pill(922, 193, "NEXT"))

    add(path("M462 154 L536 154", GRAY, "ah-gray", dash="5 4", sw=1.6))
    add(text(500, 136, "secret", "lblm") + text(500, 148, "copy", "lblm"))
    add(path("M462 230 L536 230", DARK, "ah-dark", dash="5 4", sw=1.8))
    add(text(500, 212, "geo", "lblm") + text(500, 224, "copy", "lblm"))
    add(path("M357 260 L357 322 L865 322 L865 262", DARK, "ah-dark", dash="5 4", sw=1.6))
    add(text(611, 315, "nightly table export", "lblm"))

    add(rect(390, 346, 220, 48, fill=now[0], stroke=now[1], sw=1.1, rx=8))
    add(icon("templates", 400, 357, 26) + text(436, 366, "GitHub + Bicep", "t12") + text(436, 382, "same code + settings, any region", "s11"))
    add(pill(562, 339, "NOW"))
    add(path("M390 370 L135 370 L135 302", DARK, "ah-dark", sw=1.5))
    add(path("M610 370 L950 370 L950 302", DARK, "ah-dark", sw=1.5))
    add(text(145, 360, "deploy", "lbl"))
    add(text(905, 360, "deploy", "lbl"))
    return wrap(W, H, "".join(s), "Campus Café disaster recovery: primary and DR regions")


# ---------------- Diagram C: security layers ----------------
def build_sec():
    global P
    P = "s-"
    W, H = 1000, 474
    s = [defs(["users", "identity", "templates", "func", "budget", "kv", "storage", "table", "defender", "alerts", "policy"])]
    add = s.append
    add('<rect width="%d" height="%d" fill="#FFFFFF"/>' % (W, H))
    bands = [
        ("Identity", "Who can do what", [
            ("users", "Staff sign-in", "Entra ID + MFA (security defaults)", "NEXT"),
            ("identity", "Managed identity", "RBAC, least privilege", "v1"),
            ("templates", "GitHub OIDC deploy", "RG-scoped, no stored keys", "NOW")]),
        ("Public API", "Stop bad or too many requests", [
            ("func", "Validate input", "schema, size cap, fixed templates", "NOW"),
            ("func", "Throttle", "per IP and per email", "NOW"),
            ("budget", "Cost guard", "max 5 instances + $5 budget", "v1")]),
        ("Secrets and data", "Protect keys and customer data", [
            ("kv", "Key Vault", "ACS secret by reference", "NEXT"),
            ("storage", "Keyless storage", "encrypted at rest, TLS 1.2", "v1"),
            ("table", "Data hygiene", "no PII in logs, purge old orders", "NOW")]),
        ("Network", "Limit who can reach what", [
            ("func", "HTTPS only", "TLS 1.2 minimum", "v1"),
            ("storage", "VNet integration", "storage service endpoint", "LATER"),
            (None, "Private endpoints", "plus Front Door + WAF", "LATER")]),
        ("Detect and govern", "See problems, enforce rules", [
            ("defender", "Defender for Cloud", "free tier, secure score", "NOW"),
            ("alerts", "Activity Log alerts", "role changes, deletes", "NOW"),
            ("policy", "Azure Policy + locks", "Canada only, TLS, tags", "NOW")]),
        ("Pipeline", "Keep bad code out", [
            (None, "Repo protection", "branch rules, secret scanning", "NOW"),
            (None, "Dependency checks", "Dependabot + CodeQL", "NOW"),
            ("templates", "Bicep what-if", "preview before deploy", "NOW")]),
    ]
    y = 8
    for title, purpose, chips in bands:
        add(rect(8, y, 984, 64, fill="#FAFAFA", stroke="#D2D0CE", sw=1, rx=10))
        add(text(22, y + 28, title, "t13"))
        add(text(22, y + 45, purpose, "g11"))
        x = 210
        for key, ct, cs, ph in chips:
            fill, stroke, _ = PHASE[ph]
            add(rect(x, y + 8, 254, 48, fill=fill, stroke=stroke, sw=1.1, rx=7))
            tx = x + 12
            if key:
                add(icon(key, x + 9, y + 20, 24))
                tx = x + 41
            add(text(tx, y + 27, ct, "t12") + text(tx, y + 44, cs, "s11"))
            if ph != "v1":
                add(pill(x + 254 - 48, y + 13, ph))
            x += 262
        y += 72
    lx = 210
    for ph, label in (("v1", "Already in v1"), ("NOW", "Now · free"), ("NEXT", "Next · cents"), ("LATER", "Later · costs money")):
        fill, stroke, _ = PHASE[ph]
        add(rect(lx, 452, 14, 14, fill=fill, stroke=stroke, sw=1.1, rx=3) + text(lx + 20, 463, label, "s11"))
        lx += 170
    return wrap(W, H, "".join(s), "Campus Café security layers by order of work")


arch_inline, arch_file = build_arch()
dr_inline, dr_file = build_dr()
sec_inline, sec_file = build_sec()
(out_dir / "campus-cafe-v2-architecture.svg").write_text(arch_file, encoding="utf-8")
(out_dir / "campus-cafe-v2-disaster-recovery.svg").write_text(dr_file, encoding="utf-8")
(out_dir / "campus-cafe-v2-security.svg").write_text(sec_file, encoding="utf-8")

CSS = """
:root{--blue:#0F6CBD;--orange:#C75B12;--dark:#323130;--line:#E1DFDD;--bg:#F3F2F1;
 --now:#1D9E75;--next:#BA7517;--later:#7F77DD}
*{box-sizing:border-box}
@page{size:11in 8.5in;margin:0}
html,body{margin:0;padding:0}
body{font-family:"Segoe UI",Arial,sans-serif;color:#201F1E;font-size:8.8pt;line-height:1.33;
 -webkit-print-color-adjust:exact;print-color-adjust:exact}
.page{width:11in;height:8.5in;padding:.34in .45in .5in;position:relative;overflow:hidden;
 break-after:page;page-break-after:always;background:#fff}
.page:last-child{break-after:auto;page-break-after:auto}
.hdr{border-bottom:2px solid var(--blue);padding-bottom:.05in;margin-bottom:.09in}
h1{font-size:17pt;margin:0;font-weight:600;letter-spacing:-.2px}
.sub{color:#605E5C;font-size:9pt;margin-top:1px}
.chips{display:flex;gap:6px;margin-top:.05in;flex-wrap:wrap}
.chip{background:#EFF6FC;border:1px solid #C7E0F4;color:#0B4F8A;border-radius:12px;padding:1px 9px;font-size:8pt;white-space:nowrap}
h2{font-size:10.2pt;margin:0 0 .045in;padding-left:.09in;border-left:4px solid var(--blue);font-weight:600}
.cols{display:grid;grid-template-columns:1fr 1fr;gap:.32in}
.cols3{display:grid;grid-template-columns:1fr 1fr 1fr;gap:.2in}
.blk{margin-bottom:.11in}
p{margin:0 0 .04in}
ul{margin:0;padding-left:1.1em}
li{margin-bottom:.022in}
code{font-family:Consolas,"Courier New",monospace;font-size:.9em;background:var(--bg);padding:0 3px;border-radius:3px;white-space:nowrap}
table{border-collapse:collapse;width:100%;font-size:7.9pt;line-height:1.25}
th{background:var(--bg);text-align:left;padding:2.5px 5px;border-bottom:1px solid #C8C6C4;font-weight:600}
td{padding:2.2px 5px;border-bottom:1px solid var(--line);vertical-align:top}
ol.steps{list-style:none;margin:0;padding:0;counter-reset:s}
ol.steps li{position:relative;padding-left:.28in;margin-bottom:.035in;counter-increment:s}
ol.steps li::before{content:counter(s);position:absolute;left:0;top:1px;width:.19in;height:.19in;border-radius:50%;
 background:var(--dark);color:#fff;font-weight:700;font-size:7.8pt;text-align:center;line-height:.19in}
ol.steps li.c::before{background:var(--blue)}
ol.steps li.s::before{background:var(--orange)}
ol.steps.dr li::before{background:var(--now)}
.callout{border:1px solid #F1C8A4;background:#FFF7F0;border-radius:6px;padding:.05in .11in}
.box{background:#FAF9F8;border:1px solid var(--line);border-radius:6px;padding:.06in .11in}
.note{font-size:7.5pt;color:#605E5C;margin-top:.03in}
.tag{display:inline-block;color:#fff;font-weight:700;font-size:6.8pt;border-radius:7px;padding:0 5px;letter-spacing:.03em;vertical-align:1px}
.tag.now{background:var(--now)}.tag.next{background:var(--next)}.tag.later{background:var(--later)}
.kpi{display:flex;gap:.12in;margin-bottom:.08in}
.kpi div{flex:1;border:1px solid var(--line);border-radius:6px;padding:.05in .1in;background:#FAF9F8}
.kpi b{font-size:12pt;display:block;color:var(--blue)}
.phase{border:1px solid var(--line);border-radius:8px;overflow:hidden}
.phase .ph{color:#fff;font-weight:600;padding:.05in .1in;font-size:10pt}
.phase .ph span{font-weight:400;font-size:8pt;opacity:.95;margin-left:6px}
.phase .bd{padding:.06in .1in}
.phase h3{font-size:8.6pt;margin:.03in 0 .02in;color:#323130}
figure{margin:0}
figure svg{width:100%;height:auto;display:block;margin:0 auto}
.fa svg{max-height:6.7in}.fd svg{max-height:3.75in}.fs svg{max-height:4.25in}
figcaption{font-size:7.6pt;color:#605E5C;margin-top:.03in}
.refs{font-size:7.6pt}
.refs li{margin-bottom:.02in}
.foot{position:absolute;left:.45in;right:.45in;bottom:.22in;display:flex;justify-content:space-between;font-size:7.5pt;color:#8A8886}
a{color:#0F6CBD;text-decoration:none}
"""

FOOT = '<div class="foot"><span>Campus Café · Project proposal v2 · Group 6</span><span>Page %d of 5</span></div>'

PAGE1 = """
<section class="page">
 <div class="hdr">
  <h1>Campus Café — Serverless Order Tracking on Azure</h1>
  <div class="sub">Project proposal v2 · with disaster recovery and security · Group 6 · George Brown College · Work Integrated Project · October 2026</div>
  <div class="chips"><span class="chip">Serverless</span><span class="chip">Event-driven (queue trigger)</span>
   <span class="chip">DR: pilot light in Canada East</span><span class="chip">Security: 6 layers</span><span class="chip">est. under $2 / month</span></div>
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
    <h2>What is new in v2</h2>
    <ul>
     <li><b>Disaster recovery (page 3):</b> data is copied to a second region (Canada East). A stopped copy of the app waits there. If Canada Central goes down, we follow a 4-step runbook. Target: back online within 4 hours.</li>
     <li><b>Security (page 4):</b> six layers of protection, from who can sign in to what code can be deployed.</li>
     <li><b>Order of work (page 5):</b> every new item is tagged <span class="tag now">NOW</span> free, <span class="tag next">NEXT</span> cents, or <span class="tag later">LATER</span> costs money.</li>
    </ul>
   </div>
   <div class="blk">
    <h2>How it works (numbers match the diagram on page 2)</h2>
    <ol class="steps">
     <li class="c">The customer sends an order: <code>POST /api/orders</code> over HTTPS.</li>
     <li class="c"><code>SubmitOrder</code> validates and rate-limits it, saves it as <code>Accepted</code> in the Table, and puts a message on Queue <code>notify</code>.</li>
     <li class="s">Staff send a status update: <code>PUT /status</code> (function key today, Entra sign-in next).</li>
     <li class="s"><code>UpdateOrderStatus</code> allows only the next valid status, saves it, and queues a message (none for <code>Collected</code>).</li>
     <li>The queue message triggers <code>SendNotification</code>. A failed message retries, then moves to the poison queue and raises an alert.</li>
     <li><code>SendNotification</code> sends the email through Azure Communication Services and marks that status as notified.</li>
     <li>The customer receives the email (three per order).</li>
    </ol>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>Architecture at a glance</h2>
    <ul>
     <li><b>Primary region, Canada Central:</b> resource group <code>rg-campus-cafe</code> with a Flex Consumption Function App (3 functions), one geo-redundant storage account (Table, Queue, Blob) and Azure Communication Services Email.</li>
     <li><b>Platform:</b> managed identity, Application Insights, Log Analytics, alerts, budget. New: Key Vault, Defender for Cloud, Azure Policy with delete locks, Azure outage alerts.</li>
     <li><b>DR region, Canada East:</b> <code>rg-campus-cafe-dr</code> with a stopped Function App, a DR Key Vault and a backup storage account. Built from the same Bicep code.</li>
    </ul>
   </div>
   <div class="blk">
    <h2>Design principles</h2>
    <ul>
     <li><b>Serverless, event-driven:</b> pay per execution; the queue decouples HTTP from email.</li>
     <li><b>Reliable:</b> retries, poison queue, geo-redundant data, a tested failover runbook.</li>
     <li><b>Secure by layers:</b> identity, API checks, secrets, network, detection, safe deployments.</li>
     <li><b>Observable:</b> Application Insights + Log Analytics; alerts email the team.</li>
     <li><b>Cost-aware:</b> free tiers first; anything that costs real money waits for "later".</li>
    </ul>
   </div>
   <div class="blk">
    <h2>Estimated cost per month</h2>
    <table>
     <tr><th>Item</th><th>Estimate</th></tr>
     <tr><td>Azure Functions (Flex Consumption)</td><td>Within free grant (250,000 executions, 100,000 GB-s)</td></tr>
     <tr><td>Storage (GZRS) + backup storage</td><td>Cents (data is a few MB)</td></tr>
     <tr><td>Communication Services Email</td><td>$0.00025 per email</td></tr>
     <tr><td>Application Insights + Log Analytics</td><td>Within 5 GB free</td></tr>
     <tr><td>Key Vault (primary + DR)</td><td>Cents (billed per operation)</td></tr>
     <tr><td>DR Function App (stopped)</td><td>About $0 while idle</td></tr>
     <tr><td>Defender free tier, Policy, alerts, budget</td><td>Free; optional log alert about $0.50+</td></tr>
     <tr><td><b>Total</b></td><td><b>Under $2, covered by Azure for Students ($100 credit)</b></td></tr>
    </table>
    <div class="note">Estimates; confirm in the Azure Pricing Calculator.</div>
   </div>
  </div>
 </div>
 """ + FOOT % 1 + """
</section>
"""

PAGE2 = """
<section class="page">
 <div class="hdr"><h1>Architecture</h1>
  <div class="sub">Primary region with security additions. Tags show order of work: <span class="tag now">NOW</span> <span class="tag next">NEXT</span></div></div>
 <figure class="fa">
  __ARCH__
  <figcaption>Figure 1. Numbers 1–7 follow the flow on page 1: customer order = 1–2 (blue), staff status update = 3–4 (orange), notification = 5–7 (shared).
  Dashed lines = identity (RBAC), diagnostic logs and telemetry. The dashed box on the right points to the DR region on page 3.</figcaption>
 </figure>
 """ + FOOT % 2 + """
</section>
"""

PAGE3 = """
<section class="page">
 <div class="hdr"><h1>Disaster recovery strategy</h1>
  <div class="sub">Pattern: backup and restore with a "pilot light" — a cheap, switched-off copy of the app in a second region</div></div>
 <figure class="fd">
  __DR__
  <figcaption>Figure 2. Solid blue = normal traffic. Dashed = data copies and the after-failover path. Tags show order of work.</figcaption>
 </figure>
 <div class="cols" style="margin-top:.1in">
  <div>
   <div class="kpi">
    <div><b>RTO ≤ 4 hours</b>How fast we are back online after a region outage.</div>
    <div><b>RPO: minutes</b>How much recent data we could lose. Geo-copy is not instant and has no time guarantee for tables and queues.</div>
   </div>
   <div class="blk">
    <h2>Failover runbook (if Canada Central fails)</h2>
    <ol class="steps dr">
     <li><b>Detect:</b> outage alert arrives. Check the storage account's <i>Last Sync Time</i> to see how much data might be missing.</li>
     <li><b>Fail over storage:</b> start the storage account failover. It usually takes under an hour.</li>
     <li><b>Start the DR app:</b> switch on the pilot-light Function App (or deploy it with Bicep).</li>
     <li><b>Switch and fix:</b> give clients the DR URL; re-queue any order whose email was not marked as sent.</li>
    </ol>
    <div class="note">After recovery: re-enable geo-redundancy (the account becomes locally redundant after failover), then move back.</div>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>What can go wrong, and what protects us</h2>
    <table>
     <tr><th>Problem</th><th>Protection</th></tr>
     <tr><td>A request or instance fails</td><td>Automatic retries, then poison queue + alert</td></tr>
     <tr><td>One datacenter (zone) goes down</td><td>Storage keeps copies in 3 zones (GZRS)</td></tr>
     <tr><td>The whole region goes down</td><td>Geo-copy in Canada East + pilot-light app + runbook</td></tr>
     <tr><td>Someone deletes or breaks data</td><td>Delete locks, soft delete, nightly table export</td></tr>
     <tr><td>A bad code release</td><td>Redeploy the previous version from GitHub with Bicep</td></tr>
     <tr><td>The email service is down</td><td>Messages wait in the queue and retry later</td></tr>
    </table>
   </div>
   <div class="blk">
    <h2>How we test it</h2>
    <ul>
     <li>Talk through the runbook as a team (tabletop).</li>
     <li>Deploy the full stack to Canada East from Bicep, smoke-test, then delete it.</li>
     <li>Practise a <i>planned</i> failover on a test storage account: no data loss, geo-redundancy kept.</li>
    </ul>
   </div>
  </div>
 </div>
 """ + FOOT % 3 + """
</section>
"""

PAGE4 = """
<section class="page">
 <div class="hdr"><h1>Security strategy</h1>
  <div class="sub">Defence in depth: six layers, so one mistake does not expose the whole system</div></div>
 <figure class="fs">
  __SEC__
  <figcaption>Figure 3. Each box is one control. Grey = already in v1; colour and tag = when we add it.</figcaption>
 </figure>
 <div class="cols" style="margin-top:.1in">
  <div class="blk">
   <h2>Threats we cover</h2>
   <table>
    <tr><th>Threat</th><th>Example in our app</th><th>Control</th></tr>
    <tr><td>Spoofing</td><td>Someone pretends to be staff</td><td>Entra sign-in + MFA</td></tr>
    <tr><td>Tampering</td><td>Order status changed without permission</td><td>RBAC, staff-only endpoint, logs</td></tr>
    <tr><td>Repudiation</td><td>"I never changed that order"</td><td>Signed-in identity in logs</td></tr>
    <tr><td>Information disclosure</td><td>Customer emails leak</td><td>TLS, keyless storage, no PII in logs</td></tr>
    <tr><td>Denial of service</td><td>Flood of fake orders</td><td>Throttling, max 5 instances, $5 budget</td></tr>
    <tr><td>Elevation of privilege</td><td>App gets more access than needed</td><td>Least-privilege roles, no stored keys</td></tr>
   </table>
  </div>
  <div class="blk">
   <h2>Two things to know</h2>
   <div class="callout"><ul>
    <li><b>Email abuse:</b> customers type their own email address, so an attacker could make the café email strangers. Throttling per IP and per email, plus fixed email templates, stop this.</li>
    <li><b>Network rules apply to the whole Function App.</b> We cannot IP-restrict only the staff endpoint without splitting it into its own app, so staff protection comes from sign-in instead.</li>
   </ul></div>
   <div class="note">Free tools first: Entra security defaults (MFA), Defender for Cloud free tier, Azure Policy, GitHub secret scanning.</div>
  </div>
 </div>
 """ + FOOT % 4 + """
</section>
"""

PAGE5 = """
<section class="page">
 <div class="hdr"><h1>Order of work and plan</h1>
  <div class="sub">What we build first, what follows, and what waits until there is a budget</div></div>
 <div class="cols3 blk">
  <div class="phase"><div class="ph" style="background:var(--now)">NOW<span>about 1 day · free</span></div><div class="bd">
   <h3>Disaster recovery</h3><ul><li>GZRS storage</li><li>Delete locks + soft delete</li><li>Azure outage alerts</li><li>Bicep + GitHub Actions</li><li>Written runbook</li></ul>
   <h3>Security</h3><ul><li>Input validation + throttling</li><li>No personal data in logs</li><li>Defender for Cloud (free)</li><li>Azure Policy</li><li>GitHub OIDC + secret scanning</li></ul></div></div>
  <div class="phase"><div class="ph" style="background:var(--next)">NEXT<span>cents</span></div><div class="bd">
   <h3>Disaster recovery</h3><ul><li>Pilot-light app in Canada East</li><li>DR Key Vault</li><li>Nightly table export + backup storage</li><li>DR drill (planned failover)</li></ul>
   <h3>Security</h3><ul><li>Key Vault for the ACS secret</li><li>Entra sign-in + MFA for staff</li></ul></div></div>
  <div class="phase"><div class="ph" style="background:var(--later)">LATER<span>costs money</span></div><div class="bd">
   <h3>Disaster recovery</h3><ul><li>Automatic failover routing (Traffic Manager or Front Door)</li><li>Zone-redundant compute</li><li>Active-active in two regions</li></ul>
   <h3>Security</h3><ul><li>VNet integration + storage service endpoint</li><li>Private endpoints</li><li>Front Door + web application firewall</li></ul></div></div>
 </div>
 <div class="cols">
  <div>
   <div class="blk">
    <h2>Build plan</h2>
    <table>
     <tr><th>Phase</th><th>Work</th><th>Output</th></tr>
     <tr><td>1 Secure base</td><td>Resource group, GZRS storage, monitoring, identity, locks, Policy</td><td>Safe, wired environment</td></tr>
     <tr><td>2 Core flow</td><td>Order + status functions, queue, table, validation, throttling</td><td>Statuses advance</td></tr>
     <tr><td>3 Email</td><td>Notification function, Communication Services, Key Vault</td><td>3 customer emails</td></tr>
     <tr><td>4 Watch</td><td>Alerts, Defender, outage alerts, Activity Log alerts</td><td>Problems reach the team</td></tr>
     <tr><td>5 Recover</td><td>Bicep for Canada East, pilot light, table export, runbook</td><td>DR ready</td></tr>
     <tr><td>6 Prove it</td><td>Demo script, DR drill, README</td><td>Live demo and report</td></tr>
    </table>
   </div>
  </div>
  <div>
   <div class="blk">
    <h2>Risks and things to confirm</h2>
    <div class="callout"><ul>
     <li><b>Email limits:</b> the Azure-managed domain allows 5 emails/min and 10/hour. ACS Email retires 30 Sep 2028, so email stays behind one function and can be swapped.</li>
     <li><b>Data loss on failover:</b> the most recent writes may not have reached Canada East yet.</li>
     <li><b>To confirm in the portal:</b> Flex Consumption in Canada East, GZRS in Canada Central, Entra sign-in on Flex, budgets on the student subscription.</li>
    </ul></div>
   </div>
   <div class="blk">
    <h2>References and credits</h2>
    <ul class="refs">
     <li><b>Icons:</b> Microsoft Azure Public Service Icons V24, file <code>Azure_Public_Service_Icons_V24.zip</code> (© Microsoft). Used unmodified, with the product name beside each icon, for architecture documentation, as the pack's Terms of Use permit.</li>
     <li><b>Microsoft documentation:</b>
      <a href="https://learn.microsoft.com/en-us/azure/storage/common/storage-disaster-recovery-guidance">Storage DR and failover</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/storage/common/storage-redundancy">Storage redundancy</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/reliability/regions-paired">Region pairs</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/reliability/reliability-functions">Functions reliability</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/reliability/reliability-key-vault">Key Vault reliability</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/azure-functions/functions-networking-options">Functions networking</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/azure-functions/manage-connections">Functions connections and roles</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/communication-services/concepts/service-limits">ACS limits</a> ·
      <a href="https://learn.microsoft.com/en-us/azure/communication-services/acs-retirement-and-breaking-changes-guide">ACS retirement</a></li>
    </ul>
   </div>
  </div>
 </div>
 """ + FOOT % 5 + """
</section>
"""

doc = ('<!DOCTYPE html><html lang="en"><head><meta charset="utf-8">'
       '<title>Campus Café — Project proposal v2</title>'
       '<style>%s</style></head><body>%s%s%s%s%s</body></html>'
       % (CSS, PAGE1, PAGE2.replace("__ARCH__", arch_inline), PAGE3.replace("__DR__", dr_inline),
          PAGE4.replace("__SEC__", sec_inline), PAGE5))
(out_dir / "campus-cafe-proposal-v2.html").write_text(doc, encoding="utf-8")
print("ok", len(doc))
