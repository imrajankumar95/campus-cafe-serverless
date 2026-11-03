# Campus Café Serverless — Project Playbook

Solo build, run like an enterprise team.

- **Final due:** Dec 12, 2026 (demo video + possible presentation)
- **Feedback build (v1.0.0):** Nov 19 → submit ~Nov 20
- **Capacity:** ~3.5 hrs/day · **Budget:** ≤ $50 CAD (≈ $35 USD) total

---

## Part 1 — How the project is managed

### 1.1 Tool: GitHub Projects (Jira equivalent, free, lives next to the code)

| Jira | GitHub |
|---|---|
| Epic | Issue with label `epic` + sub-issues |
| Story / Task | Issue (user story template) |
| Sprint | **Iteration** field in the Project |
| Story points | **Estimate** number field |
| Board | Project **Board** view (by Status) |
| Backlog | Project **Table** view, grouped by Epic |
| Burndown | Project **Insights** chart |
| Fix version | Milestone `v1.0.0` |
| Components | Labels `area:api`, `area:infra`, `area:web`, `area:ops` |

Recruiters can see the board. That is part of the portfolio.

### 1.2 Sprints

| Sprint | Dates | Goal | Capacity |
|---|---|---|---|
| S0 Setup | Nov 3–5 | Guardrails, ACS, repo, board, backlog, ADRs, tools | ~10 pts |
| S1 Build | Nov 6–12 | 4 functions working locally, then in Azure with real email | ~24 pts |
| S2 Harden + Release | Nov 13–19 | Web, CI/CD, security, monitoring, tests, `v1.0.0` | ~24 pts |
| UAT | ~Nov 20 | Submit to professor for feedback | — |
| S3 Iterate | Nov 21–Dec 12 | Feedback fixes, stretch items, demo video | as needed |

**Estimate scale:** 1, 2, 3, 5 (1 pt ≈ 1 hr). Anything above 5 → split it.

### 1.3 Ceremonies (solo version)

| Ceremony | When | Time | Output |
|---|---|---|---|
| Sprint planning | First day of sprint | 30 min | Stories moved into the iteration; total ≤ capacity |
| Daily standup | Start of every session | 5 min | Comment on the pinned "Sprint N log" issue: yesterday / today / blockers |
| Refinement | Mid-sprint | 15 min | Next sprint's stories have acceptance criteria + estimates |
| Sprint review | Last day of sprint | 30 min | 2-min screen recording of what works → reuse in demo video |
| Retro | After review | 15 min | `docs/retros.md`: keep / stop / try |
| Status update | Every Friday | 5 min | Project status update: On track / At risk / Off track |

### 1.4 Working agreements

- **Board columns:** Backlog → Ready → In Progress → In Review → Done
- **WIP limit:** max 2 items In Progress.
- **Definition of Ready:** acceptance criteria written, estimate set, no blocker.
- **Definition of Done:**
  - merged to `main` through a PR, CI green
  - acceptance criteria checked
  - deployed (if it runs in Azure)
  - evidence screenshot in `evidence/sprint-N/`
  - docs updated if behaviour changed
- **Branches:** `feat/<issue#>-short-name`, `fix/...`, `chore/...`, `docs/...`. Short-lived, squash-merge, delete after merge.
- **Commits:** Conventional Commits — `feat(orders): add submit endpoint`.
- **PRs:** body says `Closes #<issue>` so the issue closes and the card moves to Done.
- **Every session ends with:** a commit pushed + board updated.
- **Releases:** SemVer tags. `v1.0.0` at end of S2, `v1.1.0` after feedback.

### 1.5 Risk register

Lives in [`risks.md`](risks.md). Review it at every sprint planning.

---

## Part 2 — Sprint 0, step by step

Names below use the suffix `rk`. Every group member deploys the same design, so names like `acs-campus-cafe` will collide. Keep your suffix on every globally unique name.

| Resource | Name |
|---|---|
| Resource group | `rg-campus-cafe-prod` |
| Communication Services | `acs-campus-cafe-rk` |
| Email Communication Service | `ecs-campus-cafe-rk` |
| Tags (every resource) | `app=campus-cafe` · `env=prod` · `owner=rajan` · `costCenter=gbc-t465` |

### Day 1 (Nov 3) — Account guardrails, ACS, tools (~3.5 hrs)

**A. Account guardrails (~45 min)**

1. **Credit left.** Portal search → **Education** → Overview → note credit remaining.
   - Azure for Students has a spending limit: when credit runs out, resources stop. Your card is not charged unless you upgrade. The $50 CAD budget protects your credit.
2. **Allowed regions.** Portal search → **Policy** → Assignments → scope = *Azure for Students*.
   - Open the region assignment (name like "Allowed resource deployment regions") → **Parameters** → write down the list.
   - Can't find it? Start creating a Storage account in **Canada Central** → **Review + create**. Validation fails with `RequestDisallowedByAzure` if the region is blocked. Cancel either way.
   - Pick: **primary region** (Canada Central if allowed) + **DR region** (second allowed region).
3. **Static Web Apps check.** Start creating a Static Web App (Free plan) → **Review + create**. Note whether validation passes. Cancel.
4. **Resource providers.** Subscriptions → Azure for Students → Settings → **Resource providers** → register:
   - `Microsoft.Web`, `Microsoft.Storage`, `Microsoft.Communication`
   - `Microsoft.Insights`, `Microsoft.OperationalInsights`, `Microsoft.ManagedIdentity`
   - Stretch later: `Microsoft.Network`, `Microsoft.App`
5. **Budget.** Subscriptions → Azure for Students → Cost Management → **Budgets** → Add:
   - name `budget-campus-cafe`, monthly, amount **35** (USD)
   - alerts: Actual 50%, 80%, 100% + Forecasted 100% → your email
   - If the Budgets blade isn't available for this offer: check Cost analysis every Friday instead and note it in the risk register.
6. **Screenshot** each result → save for `evidence/sprint-0/`.

**B. ACS Email (~30 min) — do today, before onboarding closes**

1. Create resource group `rg-campus-cafe-prod` in your primary region, with the tags above.
2. Create **Email Communication Services** → `ecs-campus-cafe-rk` → data location **Canada**.
3. Open it → **Provision domains** → add **Azure managed domain**. It verifies instantly.
4. Create **Communication Services** → `acs-campus-cafe-rk` → data location **Canada** (must match step 2).
5. Open `acs-campus-cafe-rk` → **Email → Domains → Connect domain** → pick `ecs-campus-cafe-rk` + managed domain.
6. **Email → Try Email** → send to your GBC address and your Gmail. Check spam.
7. Note the sender address (`DoNotReply@<guid>.azurecomm.net`). Screenshot the received email.

**C. Dev tools (~45 min)**

1. Install Python 3.12, Functions Core Tools v4, Azurite. Update Azure CLI, then install Bicep:
   - `winget install Python.Python.3.12`
   - `winget install Microsoft.Azure.FunctionsCoreTools`
   - `npm install -g azurite`
   - `az upgrade`
   - `az bicep install`
2. VS Code extensions: **Azure Functions**, **Azure Resources**, **Bicep**, **Python**, **Azurite**.
3. Restart the terminal. Check `py -3.12 --version`, `func --version`, `az bicep version`.

**Day 1 done when:** regions known, budget set, test email received, tools verified.

### Day 2 (Nov 4) — Repo, board, backlog (~3.5 hrs)

**D. Repo (~45 min)**

The local folder `C:\dev\campus-cafe-serverless` already holds the skeleton: README, LICENSE, `.gitignore`, templates, empty folders. It sits **outside OneDrive** on purpose; syncing `.venv` and Azurite files causes locks and slowness. GitHub is the backup.

1. Local repo: `git init -b main` → `git add .` → first commit.
2. GitHub → New repo `campus-cafe-serverless` → public → **empty** (no README, `.gitignore` or license; they already exist locally).
3. `git remote add origin ...` → `git push -u origin main`.
4. **After** the first push (the ruleset blocks direct pushes): Settings → Rules → **New branch ruleset** for `main`:
   - require a pull request (0 approvals, since you're solo)
   - block force pushes
   - add "require status checks" later, once CI exists
5. Settings → General → allow **squash merging** only; tick **automatically delete head branches**.
6. Settings → Code security → enable **secret scanning** + **push protection** + **Dependabot alerts**.
7. ✅ Already in the skeleton: issue templates (user story, bug), PR template, folders `src/`, `web/`, `infra/`, `docs/adr/`, `evidence/sprint-0/`, `.github/workflows/`, VS Code extension recommendations.

**E. Project board (~30 min)**

1. Repo → **Projects** → New project → template **Team planning** (or **Iterative development**) → name `Campus Café Delivery`.
2. Fields:
   - **Status:** Backlog, Ready, In Progress, In Review, Done
   - **Iteration:** S0 Nov 3–5, S1 Nov 6–12, S2 Nov 13–19, S3 Nov 21–Dec 12
   - **Estimate:** number
   - **Priority:** P1 / P2 / P3
3. Views:
   - **Board:** current iteration, grouped by Status
   - **Backlog:** table grouped by parent issue (epic)
   - **Roadmap:** by Iteration
4. Workflows: item added → Backlog · issue closed → Done · PR merged → Done.
5. Labels:
   - types: `epic`, `story`, `bug`, `chore`, `docs`, `spike`, `risk`, `blocked`
   - areas: `area:api`, `area:infra`, `area:web`, `area:ops`
6. Milestone `v1.0.0` (due Nov 19).

**F. Backlog (~1.5 hrs)** — create the epics, then each story as a sub-issue (Part 3).

### Day 3 (Nov 5) — Design docs, spike, ceremonies (~3.5 hrs)

**G. ADRs (~1 hr)** in `docs/adr/` (template below):

- `0001-flex-consumption.md`: Flex vs old Consumption (retiring 2028)
- `0002-keyless-managed-identity.md`: no connection strings, no Key Vault in v1
- `0003-staff-auth-function-key.md`: function key now, Entra later if the GBC tenant allows
- `0004-region-and-environments.md`: chosen region (from Day 1); local = dev, Azure = prod

**H. `docs/api.md` (~45 min)**

- Endpoints: `POST /api/orders`, `GET /api/orders/{id}`, `PUT /api/orders/{id}/status`
- Request/response examples, error codes (400, 404, 409)
- Queue message `{orderId, status, rank}`
- Table `orders` fields

**I. Spike: hello-world function (~45 min)** on branch `spike/hello-func`. Proves the toolchain; delete after.

- `func init spike --python`
- `func new --name hello --template "HTTP trigger" --authlevel anonymous`
- `func start` → open `http://localhost:7071/api/hello`

**J. Close Sprint 0 (~45 min)**

1. **Review:** check the S0 issues against Definition of Done.
2. **Retro:** first entry in `docs/retros.md`.
3. **Sprint 1 planning:** move S1 stories to Ready, confirm total ≈ 24 pts.
4. **First status update** on the Project.

---

## Part 3 — Backlog (epics → stories)

| Epic | Story | Acceptance criteria (short) | Pts | Sprint |
|---|---|---|---|---|
| **Platform** | Account guardrails | Regions recorded, providers registered, budget alerts set | 1 | S0 |
| | ACS Email ready | Test email received from managed domain | 1 | S0 |
| | Dev toolchain | Hello-world function runs locally | 2 | S0 |
| | Repo + board + templates | Ruleset on `main`, templates merged, board live | 3 | S0 |
| | Backlog created | All stories below exist with estimates | 1 | S0 |
| | ADRs + API contract | 4 ADRs + `api.md` merged | 2 | S0 |
| **Orders** | Core rules + unit tests | Forward-only transitions, validation, allow-list; tests pass | 4 | S1 |
| | Submit order | POST returns 202 + orderId; row saved as Accepted; message queued; bad input → 400 | 3 | S1 |
| | Get order status | GET returns status + timestamps, never email; unknown id → 404 | 2 | S1 |
| **Staff** | Update order status | Function key required; next status only, else 409; ETag check; message queued | 3 | S1 |
| **Notifications** | Send notification | One email per status; duplicate → skipped; outdated → skipped; `EMAIL_MODE=log` works | 5 | S1 |
| **Infra** | Bicep core | Storage, Flex plan, function app, managed identity, RBAC, Log Analytics + App Insights deploy cleanly | 5 | S1 |
| | Walking skeleton | Real order in Azure → real email | 3 | S1 |
| **Web** | Order + status pages | Customer orders and checks status in the browser | 3 | S2 |
| | Staff page | Staff moves an order forward with the key | 2 | S2 |
| | Hosting + CORS | Pages live (SWA or GitHub Pages); API accepts only that origin | 1 | S2 |
| **CI/CD** | CI on PR | Ruff + pytest + `bicep build` must pass to merge | 2 | S2 |
| | CD on main | OIDC login, Bicep deploy, code deploy, smoke test | 4 | S2 |
| **Security** | Input + email safety | Body limit, fixed menu, escaped templates, allow-list | 2 | S2 |
| | Keyless hardening | Shared key off, HTTPS only, TLS 1.2, CORS locked | 2 | S2 |
| **Ops** | Logs + alerts | Logs carry orderId; alerts for failures + poison queue fired once | 3 | S2 |
| | Dashboard + uptime | Workbook + availability test on `/api/health` | 2 | S2 |
| **Release** | Test matrix + evidence | All scenarios run, screenshots saved | 2 | S2 |
| | Docs + `v1.0.0` | README, runbooks, CHANGELOG, tag + GitHub Release | 2 | S2 |
| **Stretch** | Private endpoints toggle | On for demo only, deploy still works | 5 | S3 |
| | DR redeploy | Bicep deploy to DR region, RTO recorded | 3 | S3 |
| | Nightly cleanup timer | Purge > 30 days, snapshot to blob | 2 | S3 |
| | Rate limits | Per-IP / per-email limits → 429 | 3 | S3 |
| | Entra staff sign-in | Only if GBC tenant allows app registrations | 5 | S3 |
| | Demo video | Recorded, edited, submitted | 3 | S3 |

---

## Part 4 — Templates

### User story (`.github/ISSUE_TEMPLATE/user_story.md`)

```markdown
---
name: User story
about: A unit of user-visible value
labels: story
---
**As a** <customer | staff | operator>
**I want** <capability>
**So that** <benefit>

### Acceptance criteria
- [ ] Given ... when ... then ...
- [ ] ...

### Notes / design links

### Definition of Done
- [ ] Merged via PR, CI green
- [ ] Acceptance criteria verified
- [ ] Deployed (if applicable)
- [ ] Evidence screenshot in evidence/
- [ ] Docs updated
```

### Pull request (`.github/pull_request_template.md`)

```markdown
## What
## Why
Closes #

## How tested
- [ ] Unit tests
- [ ] Ran locally (Azurite)
- [ ] Verified in Azure (if deployed)

## Checklist
- [ ] No secrets or connection strings added
- [ ] Logs don't contain email addresses
- [ ] Docs / ADR updated if a decision changed
```

### ADR (`docs/adr/NNNN-title.md`)

```markdown
# NNNN. Title
- Status: Accepted
- Date: 2026-11-05

## Context
What problem or constraint forced a decision.

## Decision
What we chose.

## Alternatives considered
Option — why not.

## Consequences
What gets easier, what gets harder, what we must watch.
```
