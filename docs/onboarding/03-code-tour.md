# Code tour (no coding experience needed)

You can read all of this on the GitHub website: open the repo → click a folder → click a file.

## Where things are

| Folder / file | What is inside | Do you need it? |
|---|---|---|
| `frontend/` | The 3 web pages (HTML, CSS, JavaScript) | Look only |
| `frontend/config.js` | One setting: the API address the pages call | Changes per environment |
| `src/function_app.py` | **All API functions.** The main file | Yes, read it |
| `src/core/menu.py` | The menu: 15 items with prices (in cents) | Look only |
| `src/core/orders.py` | The rules: what makes an order valid, how the total is calculated | Look only |
| `src/tests/` | 21 automatic tests for the rules | Know they exist |
| `src/host.json` | Settings for the Functions runtime (queue encoding, retries) | Look only |
| `src/requirements.txt` | Python packages the app needs | Look only |
| `docs/` | All documentation (you are here) | Yes |
| `.github/workflows/` | The CI/CD pipeline that deploys the website | See [04](04-github-for-beginners.md) |
| `infra/` | Infrastructure as code (Bicep). Coming soon | Later |

## `src/function_app.py` in plain English

The file has two kinds of lines:

- **Decorators** (lines starting with `@app.`): **configuration**. They tell Azure *when* to run a function and *what storage it may use*. This is the "cloud" part.
- **Function body** (the indented lines under `def`): the **logic**. What to check, what to save, what to answer.

### 1. `health`: is the API alive?

```python
@app.route(route="health", methods=["GET"])
def health(req):
    return ... {"status": "ok"}
```

- Decorator: "a GET to `/api/health` runs this."
- Body: always answers `ok`. Used to check the app is up.

### 2. `submit_order`: place an order

```python
@app.route(route="orders", methods=["POST"])
@app.table_output(arg_name="order_row", connection="OrdersStorage", table_name="orders")
@app.queue_output(arg_name="notify_msg", connection="OrdersStorage", queue_name="notify")
def submit_order(req, order_row, notify_msg):
```

Decorators, read as sentences:
- "A POST to `/api/orders` runs this."
- "This function may write one row to table `orders`."
- "This function may write one message to queue `notify`."
- `connection="OrdersStorage"` is the **name of a setting** that says which storage account. On a laptop it points to a local emulator; in Azure it points to `stcampuscaferk` using managed identity.

Body, in order:
1. Read the order and check it with the rules in `core/orders.py`. Broken rule → answer `400` with the reason.
2. Make a random order ID and a timestamp.
3. Calculate the total from the menu prices.
4. Fill in the table row and the queue message (`.set(...)`).
5. Answer `202` with order ID, status and total.

**Key idea (bindings):** the code never connects to storage itself. It fills two "envelopes"; Azure delivers them after the function finishes. That is why there are no storage keys or connection code anywhere.

### 3. `get_order_status`: check an order

```python
@app.route(route="orders/{orderId}", methods=["GET"])
@app.table_input(arg_name="row", connection="OrdersStorage", table_name="orders",
                 partition_key="{orderId}", row_key="order")
def get_order_status(req, row):
```

- `{orderId}` in the address is a placeholder. `/api/orders/abc-123` → `orderId = abc-123`.
- `table_input`: **before** the code runs, Azure fetches the matching row and hands it over as `row`.
- Body: not a valid ID → `400`. No row → `404`. Otherwise answer with status, name and times. **Never the email.**

## The rules (`src/core/orders.py`)

| Rule | Value |
|---|---|
| Pickup name | 1–40 characters |
| Email domain | `georgebrown.ca` or `gmail.com` only |
| Items per order | 1–10 lines, no duplicates |
| Quantity per item | 1–10 |
| Item IDs | Must exist in `menu.py` |
| Status moves | Forward only, one step at a time |

## What the email worker looks like

The email part has **no Python**. It is the Logic App, built in the portal designer. See [01-azure-tour.md](01-azure-tour.md#the-email-logic-app-step-by-step).
