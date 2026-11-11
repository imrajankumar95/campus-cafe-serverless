# Project board

A Jira-style view of every step needed to finish the project. Update the **Status** column as work moves. When an item is Done, its "Done when" must be true and provable (screenshot in `evidence/`, merged PR, or test output).

**Legend:** ✅ Done · 🔄 In progress · ⬜ To do · ⏸ Stretch (after feedback)

## Progress

| Sprint | Dates | Goal | Status |
|---|---|---|---|
| S0 Setup | Nov 3–10 | Account, repo, tools, email, frontend | ✅ Mostly done |
| S1 Build | Nov 11–15 | Backend working locally, then in Azure with real email | 🔄 Started |
| S2 Harden + release | Nov 16–20 | CI/CD, security, monitoring, tests, `v1.0.0` | ⬜ |
| UAT | ~Nov 21 | Submit to professor for feedback | ⬜ |
| S3 Iterate | Nov 22–Dec 12 | Feedback fixes, stretch items, demo video | ⬜ |

> Dates were re-planned on Nov 11: S0 ran 5 days late, so the feedback build moved from Nov 19 to ~Nov 21.

---

## E1 · Platform setup (S0)

| ID | Task | Status | Done when |
|---|---|---|---|
| PLAT-1 | Check allowed region | ✅ | Canada Central passes validation |
| PLAT-2 | Check Static Web Apps availability | ✅ | Free SWA deployed in test RG (then deleted) |
| PLAT-3 | Budget alert | ✅ | `budget-campus-cafe` $20/month with 50/80/100% + forecast alerts |
| PLAT-4 | Register resource providers | ✅ | Web, Storage, Insights, OperationalInsights, ManagedIdentity registered |
| PLAT-5 | Create ACS Email + managed domain | ✅ | Test email received on GBC + Gmail |
| PLAT-6 | Install dev tools | ✅ | Python 3.12, Core Tools 4, Azurite, Bicep, VS Code extensions |
| PLAT-7 | Check remaining credit | ⏸ | Credit not visible on student sub; budget alert covers it |
| PLAT-8 | Delete `rg-swa-test` | ⬜ | RG no longer listed |

## E2 · Repo + ways of working (S0)

| ID | Task | Status | Done when |
|---|---|---|---|
| REPO-1 | Create repo + skeleton | ✅ | `campus-cafe-serverless` public on GitHub |
| REPO-2 | Git identity = imrajankumar95 | ✅ | Commits show imrajankumar95 |
| REPO-3 | Merge settings (squash only, auto-delete branches) | 🔄 | Settings → General saved |
| REPO-4 | Ruleset on `main` (PR + 1 approval) | ⬜ | Direct push to `main` is rejected |
| REPO-5 | Invite 4 teammates | 🔄 | 4 collaborators accepted |
| REPO-6 | Decision records (ADRs) | ⬜ | 4 files in `docs/adr/` |
| REPO-7 | API contract | 🔄 | `docs/api.md` merged |

## E3 · Frontend

| ID | Task | Status | Done when |
|---|---|---|---|
| WEB-1 | Home, Menu, Order pages | ✅ | PR #1 + #2 merged |
| WEB-2 | Connect to real API | ⬜ | `config.js` points at Function App; order placed from browser |
| WEB-3 | Host on Static Web Apps | ⬜ | Public URL works; API CORS allows only that URL |
| WEB-4 | Staff page (move order to next status) | ⬜ | Staff can advance an order from the browser |

## E4 · Backend core (S1)

| ID | Task | Status | Done when |
|---|---|---|---|
| API-1 | Functions project skeleton in `src/` | ✅ | `func start` runs; `GET /api/health` returns 200 locally |
| API-2 | Core logic: menu, validation, status rules | ✅ | Unit tests pass (`pytest`) |
| API-3 | `SubmitOrder` (POST) | ⬜ | Order saved in Azurite table + message in `notify` queue; bad input → 400 |
| API-4 | `GetOrderStatus` (GET) | ⬜ | Returns status, never email; unknown id → 404 |
| API-5 | `UpdateOrderStatus` (PUT) | ⬜ | Needs function key; next status only, else 409; ETag check |
| API-6 | `SendNotification` (queue) | ⬜ | One email per status; duplicates + outdated skipped; `EMAIL_MODE=log` works |
| API-7 | Real email via ACS + managed identity | ⬜ | Email arrives for Accepted, Preparing, Ready |

## E5 · Infrastructure as code (S1)

| ID | Task | Status | Done when |
|---|---|---|---|
| IAC-1 | Bicep: storage, table, queue | ⬜ | Deployed from laptop with `az deployment group create` |
| IAC-2 | Bicep: Flex plan, Function App, managed identity, RBAC | ⬜ | App runs with no connection strings |
| IAC-3 | Bicep: Log Analytics + App Insights | ⬜ | Function logs visible in App Insights |
| IAC-4 | Bicep: import existing ACS resources | ⬜ | Re-deploy shows no changes to ACS |
| IAC-5 | **Walking skeleton** | ⬜ | Real order in Azure → real email received |

## E6 · CI/CD (S2)

| ID | Task | Status | Done when |
|---|---|---|---|
| CICD-1 | CI on every PR: lint, tests, `bicep build` | ⬜ | PR can't merge if CI fails |
| CICD-2 | OIDC login from GitHub to Azure | ⬜ | No secrets stored; workflow logs in |
| CICD-3 | CD on merge: deploy Bicep + function code + frontend | ⬜ | Merge to `main` updates Azure |
| CICD-4 | Smoke test after deploy | ⬜ | Pipeline fails if `/api/health` or submit fails |

## E7 · Security (S2)

| ID | Task | Status | Done when |
|---|---|---|---|
| SEC-1 | Input limits, email allow-list, escaped email templates | ⬜ | Bad input rejected; tests cover it |
| SEC-2 | Keyless: storage shared-key off, HTTPS only, TLS 1.2 | ⬜ | Settings verified in portal |
| SEC-3 | CORS locked to the frontend URL | ⬜ | Calls from other sites are blocked |

## E8 · Monitoring (S2)

| ID | Task | Status | Done when |
|---|---|---|---|
| OBS-1 | Logs carry `orderId`, never email | ⬜ | KQL query shows an order's full journey |
| OBS-2 | Alerts: function failures, poison queue | ⬜ | Each alert fired once on purpose, email received |
| OBS-3 | Dashboard (workbook) + availability test | ⬜ | Screenshot in `evidence/` |

## E9 · Release v1.0.0 (S2)

| ID | Task | Status | Done when |
|---|---|---|---|
| REL-1 | Test matrix run end to end | ⬜ | All scenarios pass; screenshots saved |
| REL-2 | README with architecture, setup, screenshots | ⬜ | A stranger could run it from the README |
| REL-3 | Runbooks (poison replay, add staff key, redeploy) | ⬜ | Files in `docs/runbooks/` |
| REL-4 | Tag `v1.0.0` + GitHub Release | ⬜ | Release page exists |
| REL-5 | Submit to professor | ⬜ | Submitted; feedback logged as issues |

## E10 · Stretch + final (S3)

| ID | Task | Status | Done when |
|---|---|---|---|
| STR-1 | Professor feedback fixes | ⬜ | All feedback issues closed |
| STR-2 | Private endpoints toggle (on for demo only) | ⏸ | Storage unreachable from internet; app still works |
| STR-3 | DR redeploy to second region | ⏸ | Bicep deploys there; recovery time recorded |
| STR-4 | Nightly cleanup timer | ⏸ | Orders > 30 days purged |
| STR-5 | Rate limits | ⏸ | Too many orders → 429 |
| STR-6 | Demo video | ⬜ | Recorded and submitted by Dec 12 |
| STR-7 | Tear down Azure resources | ⬜ | Evidence saved first; RG deleted; cost stops |

---

## How to use this board

1. Start of session: pick the top ⬜ item in the current sprint → set it to 🔄.
2. Create a branch named after it, e.g. `feat/API-3-submit-order`.
3. Finish → check "Done when" → PR → merge → set ✅ (in the same PR).
4. Max 2 items 🔄 at once.
5. Friday: update the Progress table.
