# Glossary

| Term | Meaning in this project |
|---|---|
| **202 Accepted** | HTTP answer meaning "saved, the rest happens later" (the email) |
| **400 / 404 / 409 / 500** | Bad input / not found / not allowed right now (wrong status step) / server crashed |
| **ADR** | Architecture Decision Record. A short file explaining a big design choice and why. In `docs/adr/` |
| **API** | The set of web addresses the frontend calls, e.g. `POST /api/orders`. Rules in `docs/api.md` |
| **Azurite** | Fake Azure Storage that runs on a laptop for testing |
| **Bicep** | Microsoft's language for describing Azure resources as code (infrastructure as code) |
| **Binding** | A decorator that connects a function to storage without connection code. Output = write, input = read |
| **Branch / commit / PR / merge** | See [04-github-for-beginners.md](04-github-for-beginners.md) |
| **CI/CD** | Continuous integration / delivery. Automatic test and deploy on every merge (GitHub Actions) |
| **CORS** | Browser rule: only allowed websites may call our API. We will allow only our Static Web App |
| **Curl** | Command-line tool to send a web request. Used to test the API without the website |
| **Decorator** | A line starting with `@` above a Python function. Here it is Azure configuration |
| **Dequeue count** | How many times the queue has handed out the same message. Used to detect messages that keep failing |
| **Event-driven** | Parts react to events (a message arriving) instead of calling each other and waiting |
| **Flex Consumption** | Function App plan that scales to zero and bills per use |
| **Function App** | Azure service that runs small pieces of code when triggered |
| **GUID / UUID** | A random, unguessable ID, e.g. `0fd82ffd-ae7c-4db6-ab12-7d60b05f0fb0`. Our order IDs |
| **IAM / RBAC** | Access control: who (identity) gets which role on which resource |
| **Least privilege** | Give each identity only the permissions its job needs |
| **Logic App** | Azure workflow service built with a visual designer. Our email worker |
| **Managed identity** | An identity Azure gives a resource so it can log in to other services without passwords or keys |
| **OIDC** | Short-lived login token from GitHub to Azure. No stored password |
| **PartitionKey / RowKey** | The two-part address of a table row. Ours: order ID + `order` |
| **Poison queue** | `notify-poison`. Where messages go after failing 5 times, so they stop retrying |
| **Pop receipt** | One-time proof a run holds a queue message. Needed to delete it |
| **Queue** | A to-do list of messages between services. Ours: `notify` |
| **Serverless** | No servers to manage; pay per use; scales to zero |
| **Static Web App** | Azure hosting for plain web pages, deployed from GitHub |
| **System-assigned vs user-assigned identity** | System: belongs to one resource, deleted with it. User: a separate resource that can be shared |
| **Table Storage** | Simple cheap database of rows (no SQL). Ours: `orders` |
| **Trigger** | What starts a function or Logic App: a web request, a queue message, a timer |
| **Validation** | Checking input before trusting it (name length, email domain, menu items) |
