# Risk register

Review at every sprint planning. Close a risk when it can no longer happen.

| Risk | Likelihood | Impact | Response | Status |
|---|---|---|---|---|
| Canada regions blocked by student policy | High (reference repo hit it) | Proposal region changes | Check in S0; pick allowed region; record in ADR-0004 | Open |
| Static Web Apps blocked on student subscription | Medium | No SWA hosting | Fallback: GitHub Pages (free) | Open |
| ACS Email onboarding closes | Medium | No real email | Create in S0; `EMAIL_MODE=log` fallback | Open |
| Managed email domain limit (10/hr) | High during testing | Demo emails delayed | Test in log mode; real email only for demo | Open |
| Credit burn | Low | Budget overrun | Budget alerts; private endpoints only on for 1–2 days | Open |
