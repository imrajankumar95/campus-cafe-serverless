# API contract

The agreement between the frontend, the Function App and the background worker. Change this file first (in a PR) before changing behaviour.

- **Base URL:** `https://<function-app>.azurewebsites.net` (local: `http://localhost:7071`)
- **Format:** JSON in, JSON out. `Content-Type: application/json`
- **Max request body:** 4 KB

## Order statuses

| Rank | Status | Who sets it | Email sent |
|---|---|---|---|
| 1 | `Accepted` | System, on submit | Yes |
| 2 | `Preparing` | Staff | Yes |
| 3 | `Ready` | Staff | Yes |
| 4 | `Collected` | Staff | No (order closed) |

Moves are forward-only, one step at a time. Anything else returns `409`.

## Endpoints

### `POST /api/orders` — place an order

Auth: anonymous (public).

Request:

```json
{
  "pickupName": "Sam",
  "email": "sam@georgebrown.ca",
  "items": [
    { "id": "latte", "qty": 2 },
    { "id": "croissant", "qty": 1 }
  ]
}
```

Rules:

| Field | Rule |
|---|---|
| `pickupName` | Required, 1–40 characters after trimming |
| `email` | Required, valid format, domain on the allow-list (`georgebrown.ca`, `gmail.com`) |
| `items` | 1–10 lines, no duplicate `id` |
| `items[].id` | Must exist on the menu (`frontend/menu.js` and `src/core/menu.py` hold the same IDs) |
| `items[].qty` | Whole number 1–10 |

Prices and the total are calculated **on the server** from the menu. The client never sends prices.

Response `202 Accepted`:

```json
{
  "orderId": "3f0c2a8e-6a1b-4c39-9e4b-2b7f0f1c9d11",
  "status": "Accepted",
  "total": 12.15
}
```

Errors: `400` (validation), `413` (body too large), `500` (unexpected).

### `GET /api/orders/{orderId}` — check status

Auth: anonymous. The unguessable GUID is the only "key".

Response `200 OK`:

```json
{
  "orderId": "3f0c2a8e-6a1b-4c39-9e4b-2b7f0f1c9d11",
  "status": "Preparing",
  "pickupName": "Sam",
  "createdAt": "2026-11-11T14:02:11Z",
  "updatedAt": "2026-11-11T14:05:40Z"
}
```

Never returns the email address or the items.

Errors: `400` (not a GUID), `404` (no such order).

### `PUT /api/orders/{orderId}/status` — staff moves an order forward

Auth: function key in header `x-functions-key` (staff only).

Request:

```json
{ "status": "Preparing" }
```

Response `200 OK`: same body as `GET`.

Errors: `400` (unknown status), `401` (missing/wrong key), `404` (no such order), `409` (not the next status, or another update won the race).

### `GET /api/health` — liveness

Auth: anonymous. Response `200 OK`: `{ "status": "ok" }`. Used by the availability test.

## Error body

Every error uses the same shape. The frontend shows `message` to the user.

```json
{ "code": "validation_error", "message": "Quantity must be between 1 and 10." }
```

| `code` | HTTP |
|---|---|
| `validation_error` | 400 |
| `payload_too_large` | 413 |
| `unauthorized` | 401 |
| `not_found` | 404 |
| `invalid_transition` | 409 |
| `conflict` | 409 |
| `internal_error` | 500 |

## Queue message — `notify`

Sent by `SubmitOrder` and `UpdateOrderStatus` (via queue output bindings), consumed by the **Logic App email workflow** (see `adr/0001-cloud-first-design.md`). Plain JSON (`host.json` sets `messageEncoding: "none"`).

```json
{ "orderId": "3f0c2a8e-6a1b-4c39-9e4b-2b7f0f1c9d11", "status": "Preparing", "rank": 2 }
```

Logic App rules:

- Status `Collected` → no email.
- Read the order row (by `orderId`) to get the email address.
- Send the matching email through Communication Services.
- Send fails → Logic App retry policy → run marked failed → alert. Messages that keep failing go to `notify-poison`.
- A rare duplicate email is accepted (queues deliver at least once).

## Table — `orders`

| Field | Example | Notes |
|---|---|---|
| `PartitionKey` | `3f0c2a8e-…` | The orderId |
| `RowKey` | `order` | Fixed |
| `pickupName` | `Sam` | |
| `email` | `sam@georgebrown.ca` | Only personal data. Never logged, never returned |
| `itemsJson` | `[{"id":"latte","qty":2}]` | Table Storage has no arrays, so stored as a JSON string |
| `total` | `12.15` | Server-calculated |
| `status` / `statusRank` | `Preparing` / `2` | |
| `notifyAccepted` / `notifyPreparing` / `notifyReady` | `pending` · `sending` · `sent` | Exactly-once email flags |
| `createdAt` / `updatedAt` | ISO 8601 UTC | |

ETag (built into Table Storage) is used on every update so two writers can't overwrite each other.
