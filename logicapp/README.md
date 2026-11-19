# Email Logic App: import guide for teammates

`notify-workflow.json` is the email worker (board item CLD-7). Import it into **your own** subscription to get the same design without rebuilding it click by click.

The file contains no keys, subscription IDs or personal data. Account-specific values are placeholders.

## What it does

Queue `notify` → parse message → skip if `Collected` → read the order row (email, name) → send email through Communication Services (managed identity) → delete the message. A message that fails 5 times is moved to `notify-poison`. Details: [docs/onboarding/01-azure-tour.md](../docs/onboarding/01-azure-tour.md#the-email-logic-app-step-by-step).

## Before you start

You need, in your subscription: a storage account with queues `notify` + `notify-poison` and table `orders`, plus a Communication Services resource with a connected email domain.

## Steps (portal only, ~20 min)

### 1. Create the Logic App
Logic apps → **+ Add** → **Consumption (Multi-tenant)** → your resource group, name `logic-campus-cafe-notify-<initials>`, your region → Create.

### 2. Turn on its identity
Logic App → **Settings → Identity** → System assigned **On** → Save.

### 3. Give it access (IAM on the **target** resource → Add role assignment → Managed identity → Logic app)

| Target | Role |
|---|---|
| Storage account | Storage Queue Data Message Processor |
| Storage account | Storage Queue Data Reader |
| Storage account | Storage Table Data Reader |
| Queue `notify-poison` only (Storage account → Queues → `notify-poison` → Access Control) | Storage Queue Data Message Sender |
| Communication Services resource | Communication and Email Service Owner |

Wait about 5 minutes for roles to apply.

### 4. Create the two connections
Logic app designer → add trigger **Azure Queues → When there are messages in a queue (V2)** → new connection, auth **Logic Apps Managed Identity**. Then add any **Azure Table Storage** action (e.g. Get entity (V2)) → new connection, auth **Logic Apps Managed Identity**. **Publish** (the workflow itself does not matter yet).

This creates connections named `azurequeues` and `azuretables` and adds a `parameters` block with their IDs at the bottom of the code.

### 5. Paste the workflow
1. Open `notify-workflow.json`, find and replace the placeholders:

   | Placeholder | Your value | Where to find it |
   |---|---|---|
   | `<STORAGE_ACCOUNT>` (5 places) | e.g. `stcampuscafexy` | Storage account name |
   | `<ACS_ENDPOINT_HOST>` | e.g. `acs-campus-cafe-xy.canada.communication.azure.com` | Communication Services → Overview → Endpoint, without `https://` and trailing `/` |
   | `<SENDER_ADDRESS>` | e.g. `DoNotReply@<guid>.azurecomm.net` | Email Communication Service → Provision domains → domain → MailFrom |

2. Logic App → designer → **Code** view.
3. Replace **only the `"definition": { ... }` part** with the file's `definition`. **Keep your own `"parameters"` block** at the bottom (it holds your connection IDs).
4. **Publish.**

If your connections got different names (e.g. `azurequeues-1`), change `['azurequeues']` / `['azuretables']` in the file to match the names in your `parameters` block.

### 6. Test
1. Storage browser → table `orders` → add entity: PartitionKey `test-1`, RowKey `order`, `pickupName` = your name, `email` = your email.
2. Queue `notify` → **Add message** → `{"orderId":"test-1","status":"Accepted","rank":1}` → **untick "Encode the message body in Base64"**.
3. Run, or wait up to 3 minutes. Expect a green run and an email.

### 7. Save cost
**Disable** the Logic App when you are not testing. The 3-minute polling is billed (about $1.80/month when enabled).

## Keeping it in sync

If you change the workflow in the portal, export it (Code view → copy), replace your values with the placeholders again, and update this file in a pull request.
