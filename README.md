# Campus Café — Serverless Order Tracking

Event-driven, serverless order tracking for a campus café on Azure.
Customers order online and get an email each time staff move the order forward: **Accepted → Preparing → Ready**.

> **Status:** Sprint 0 (setup). Target `v1.0.0`: Nov 19, 2026.

## Planned architecture

| Layer | Service |
|---|---|
| Compute | Azure Functions, Flex Consumption, Python 3.12 (4 functions) |
| Data + messaging | Azure Storage: Table `orders`, Queue `notify` (+ poison queue) |
| Email | Azure Communication Services (managed domain) |
| Identity | User-assigned managed identity, no keys or connection strings |
| Infrastructure + delivery | Bicep, GitHub Actions with OpenID Connect |
| Observability | Application Insights, Log Analytics, alerts |

- Design proposal and diagrams: [docs/design](docs/design)
- How the project is run (sprints, backlog, Definition of Done): [docs/project-management.md](docs/project-management.md)
- Local API and Azure deployment steps: [docs/deployment.md](docs/deployment.md)

## Repository layout

```
src/        Azure Functions app (Python)
infra/      Bicep templates
frontend/   Customer pages: home, menu, order + tracking (vanilla JS)
docs/       Design, ADRs, API contract, runbooks, retros
evidence/   Screenshots proving each sprint's work
.github/    Workflows, issue and PR templates
```

## License

[MIT](LICENSE)
