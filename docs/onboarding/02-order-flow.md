# One order, from click to email

Follow a single order through the system. Each step says where you can **see** it in the portal.

| # | What happens | Who does it | See it in the portal |
|---|---|---|---|
| 1 | Student fills the order form and clicks **Place order** | Browser (Static Web App page) | The site URL |
| 2 | Browser sends `POST /api/orders` with name, email, items | Browser | Function App → **Monitoring → Log stream** |
| 3 | Function checks the input: name, email domain, menu items, quantities. Bad input → `400` error, nothing saved | Function `submit_order` | App Insights → **Failures** (for errors) |
| 4 | Function calculates the total from the server-side menu (the browser never sends prices) | Function | — |
| 5 | Function saves one row in table `orders` (status `Accepted`) | Function (output binding) | Storage browser → Tables → `orders` |
| 6 | Function puts a small message on queue `notify`: `{"orderId": "...", "status": "Accepted", "rank": 1}`. No email in it | Function (output binding) | Storage browser → Queues → `notify` |
| 7 | Function answers `202 Accepted` with the order ID and total. The student sees "Order placed!" | Function | — |
| 8 | Within 3 minutes the Logic App finds the message | Logic App trigger | Logic App → **Run history** |
| 9 | Logic App reads the order row to get the email address and name | Logic App (Get entity) | Click the run → **Get entity** step → Outputs |
| 10 | Logic App calls Communication Services → email sent | Logic App (HTTP) | HTTP step shows `202` |
| 11 | Logic App deletes the queue message | Logic App | `notify` queue is empty again |
| 12 | Student checks status any time with `GET /api/orders/{orderId}` (never returns the email) | Function `get_order_status` | — |

## When something goes wrong

| Problem | What happens | Where to look |
|---|---|---|
| Bad input (e.g. quantity 0) | `400` returned, nothing saved, no email | Response message explains why |
| Email service down | Logic App run fails, message stays in the queue, retried on the next check | Run history: red runs with code `WillRetry` |
| Message keeps failing (5 times) | Copied to `notify-poison`, removed from `notify`, run marked failed with `MovedToPoison` | Storage browser → Queues → `notify-poison` |
| Unknown order ID on status check | `404 Not Found` | — |

## Later (staff side, being built)

Staff call `PUT /api/orders/{orderId}/status` with a secret key to move the order one step forward (Accepted → Preparing → Ready → Collected). Each move puts a new message on `notify`, and the same Logic App emails the student. Skipping a step returns `409`.

## Deeper dive

[docs/learning/how-submit-order-works.md](../learning/how-submit-order-works.md) explains the submit and status functions line by line, including a real bug we hit and fixed.
