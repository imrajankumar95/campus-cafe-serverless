# Azure tour

Everything lives in **one resource group**: `rg-campus-cafe-prod` (Canada Central). Open it in the portal and follow this table top to bottom.

Names below are Rajan's (suffix `-rk`). In your own subscription use your initials.

## The resources

| Resource | Type | What it does | Where to click to see it working |
|---|---|---|---|
| `stcampuscaferk` | Storage account | Holds the data: table `orders`, queues `notify` and `notify-poison` | **Storage browser** → Tables → `orders` (one row per order) · Queues → `notify` |
| `func-campus-cafe-rk` | Function App (Flex Consumption, Python 3.12) | The API: submit order, get status, health check | **Overview** → URL, then add `/api/health` in a browser → `{"status": "ok"}` |
| `func-campus-cafe-rk-uami` | User-assigned managed identity | The Function App's "ID card" for logging in to storage | **Azure role assignments** → its roles on the storage account |
| `logic-campus-cafe-notify-rk` | Logic App (Consumption) | Email worker: reads the queue, looks up the order, sends the email | **Logic app designer** (the flow) · **Run history** (every run, green or red) |
| `acs-campus-cafe-rk` | Communication Services | Sends the emails | **Overview** → Endpoint (the Logic App calls this) |
| `ecs-campus-cafe-rk` | Email Communication Service | Owns the sender domain `...azurecomm.net` | **Provision domains** → domain verified |
| `swa-campus-cafe-rk` | Static Web App (Free) | Hosts the 3 web pages | **Overview** → URL opens the site |
| `log-campus-cafe-rk` | Log Analytics workspace | Stores all logs (daily cap 0.1 GB to control cost) | **Logs** → run queries |
| `appi-campus-cafe-rk` | Application Insights | Function App monitoring: requests, failures, timings | **Live metrics**, **Failures** |
| `azurequeues`, `azuretables` | API connections | Saved "logins" the Logic App uses (managed identity, no keys) | Open one → **Edit API connection** → auth type |
| `budget-campus-cafe` | Budget (subscription level) | Emails at 50/80/100% of $20/month | Cost Management → Budgets |

## Who can access what (IAM)

Every arrow below is an IAM role assignment. Open the **target** resource → **Access control (IAM)** → **Role assignments** to see it.

| Identity (who) | Target (what) | Role | Why |
|---|---|---|---|
| Function App identity (`...-uami`) | Storage account | Storage Blob Data Owner | Functions host needs it to run |
| Function App identity | Storage account | Storage Queue Data Contributor | Put messages on `notify` |
| Function App identity | Storage account | Storage Table Data Contributor | Write and read orders |
| Logic App identity (system-assigned) | Storage account | Storage Queue Data Message Processor | Read and delete queue messages |
| Logic App identity | Storage account | Storage Queue Data Reader | List queues in the designer |
| Logic App identity | Storage account | Storage Table Data Reader | Read the email address (read only) |
| Logic App identity | Queue `notify-poison` **only** | Storage Queue Data Message Sender | Move failed messages there, nothing else |
| Logic App identity | `acs-campus-cafe-rk` | Communication and Email Service Owner | Send email (only built-in role available) |

**Least privilege:** the Logic App can read the table but not change it, and can only send messages to the poison queue. Each identity gets only what its job needs.

## The email Logic App, step by step

Open **Logic app designer** and match these boxes:

1. **When there are messages in a queue (V2)**: checks `notify` every 3 minutes. One run per message.
2. **Parse JSON**: turns the message text into fields (`orderId`, `status`, `rank`). Unknown status → fails.
3. **Condition: status is not "Collected"**
   - True → **Get entity**: read the order row (email + name) → **HTTP**: call Communication Services to send the email (logs in with managed identity).
   - False → nothing (no email for collected orders).
4. **Delete message - done**: removes the message once handled.
5. **Check retries** (runs only if step 3 failed): after 5 failed tries, copy the message to `notify-poison`, delete it from `notify`, and mark the run Failed. Before that, mark the run Failed and let the queue retry.

**Note:** the built-in "Send email" connector only accepted a connection string (a key). We used a plain **HTTP** action with managed identity instead, so the design stays keyless.

## What costs money

Almost nothing while idle: under $1/month. The Logic App polling (about $1.80/month at every 3 minutes) is the biggest item. It is **disabled** when not testing. Emails cost fractions of a cent each.
