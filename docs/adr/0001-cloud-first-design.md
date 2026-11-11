# 0001. Cloud-first design: platform features over application code

- Status: Accepted
- Date: 2026-11-11

## Context

This is a cloud computing project. The grade and the portfolio value come from the Azure infrastructure, DevOps and operations, not from application code. By Nov 11 the work was about 70% code (frontend, validation, tests) and 30% cloud. The target is 30% code, 70% cloud and DevOps.

## Decision

Let Azure do the work wherever a managed feature exists, and keep the Python code to small HTTP functions.

| Need | Before (code) | After (platform) |
|---|---|---|
| Save order / send queue message | Storage SDK helper module | **Function bindings** (Table output, Queue output), configured by connection settings |
| Read an order | Storage SDK query | **Table input binding** |
| Send emails on each status | `SendNotification` Python function with ACS SDK and exactly-once logic | **Logic App** (designer UI): queue trigger → read order → ACS "Send email" action |
| Retries, failed messages | Custom code | Built-in queue retries + `notify-poison` queue + Logic App run history + alert |
| Credentials | Connection strings | **User-assigned managed identity** + RBAC roles, set in the portal |
| Infrastructure | — | Built in the **portal** first (learning), then reproduced in **Bicep** (teammate) and deployed by **GitHub Actions** |

Code that stays: `core/` validation and status rules (with tests), and 3–4 thin HTTP functions.

## Alternatives considered

- **All-code backend (original plan):** more control, but makes the project developer-heavy.
- **API Management in front of Functions:** good cloud skill, but adds cost and setup time. Possible stretch.

## Consequences

- Much less code to write, review and explain.
- More portal work: storage, identity, RBAC, app settings, Logic App, monitoring. That's the skill set being graded.
- Exactly-once email is no longer guaranteed. A rare duplicate email is accepted and documented.
- Logic App Consumption costs a few cents a month (queue polling + actions). Covered by the $20 budget.
- To verify during build: Logic App connections to Storage and ACS using managed identity.
