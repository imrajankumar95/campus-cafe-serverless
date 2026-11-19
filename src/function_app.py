import json
import uuid
from datetime import datetime, timezone

import azure.functions as func

from core.orders import validate_order, total_cents, ValidationError, can_move, STATUS_RANK

# Default for every HTTP route: public. Staff route will override this later.
app = func.FunctionApp(http_auth_level=func.AuthLevel.ANONYMOUS)


@app.route(route="health", methods=["GET"])
def health(req: func.HttpRequest) -> func.HttpResponse:
    return func.HttpResponse(
        json.dumps({"status": "ok"}),
        status_code=200,
        mimetype="application/json",
    )


def json_response(status: int, body: dict) -> func.HttpResponse:
    return func.HttpResponse(json.dumps(body), status_code=status, mimetype="application/json")


def load_rows(rows: str) -> list:
    data = json.loads(rows) if rows else []
    return [data] if isinstance(data, dict) else data


@app.route(route="orders", methods=["POST"])
@app.table_output(arg_name="order_row", connection="OrdersStorage", table_name="orders")
@app.queue_output(arg_name="notify_msg", connection="OrdersStorage", queue_name="notify")
def submit_order(req: func.HttpRequest, order_row: func.Out[str], notify_msg: func.Out[str]) -> func.HttpResponse:
    try:
        order = validate_order(req.get_json())
    except ValueError:
        return json_response(400, {"code": "validation_error", "message": "Body must be valid JSON."})
    except ValidationError as e:
        return json_response(400, {"code": "validation_error", "message": str(e)})

    order_id = str(uuid.uuid4())
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    total = total_cents(order["items"]) / 100

    order_row.set(json.dumps({
        "PartitionKey": order_id,
        "RowKey": "order",
        "pickupName": order["pickupName"],
        "email": order["email"],
        "itemsJson": json.dumps(order["items"]),
        "total": total,
        "status": "Accepted",
        "statusRank": 1,
        "createdAt": now,
        "updatedAt": now,
    }))
    notify_msg.set(json.dumps({"orderId": order_id, "status": "Accepted", "rank": 1}))

    return json_response(202, {"orderId": order_id, "status": "Accepted", "total": total})


@app.route(route="orders/{orderId}", methods=["GET"])
@app.table_input(arg_name="rows", connection="OrdersStorage", table_name="orders",
                 partition_key="{orderId}")
def get_order_status(req: func.HttpRequest, rows: str) -> func.HttpResponse:
    order_id = req.route_params.get("orderId")
    try:
        uuid.UUID(order_id)
    except ValueError:
        return json_response(400, {"code": "validation_error", "message": "Order ID must be a GUID."})

    entities = load_rows(rows)
    order = next((e for e in entities if e.get("RowKey") == "order"), None)
    if not order:
        return json_response(404, {"code": "not_found", "message": "Order not found."})

    latest = max(entities, key=lambda e: e.get("statusRank", 0))
    return json_response(200, {
        "orderId": order_id,
        "status": latest["status"],
        "pickupName": order["pickupName"],
        "createdAt": order["createdAt"],
        "updatedAt": latest.get("updatedAt", order["updatedAt"]),
    })


@app.route(route="orders/{orderId}/status", methods=["PUT"], auth_level=func.AuthLevel.FUNCTION)
@app.table_input(arg_name="rows", connection="OrdersStorage", table_name="orders",
                 partition_key="{orderId}")
@app.table_output(arg_name="status_row", connection="OrdersStorage", table_name="orders")
@app.queue_output(arg_name="notify_msg", connection="OrdersStorage", queue_name="notify")
def update_order_status(req: func.HttpRequest, rows: str,
                        status_row: func.Out[str], notify_msg: func.Out[str]) -> func.HttpResponse:
    order_id = req.route_params.get("orderId")
    try:
        uuid.UUID(order_id)
    except ValueError:
        return json_response(400, {"code": "validation_error", "message": "Order ID must be a GUID."})

    try:
        target = req.get_json().get("status")
    except (ValueError, AttributeError):
        return json_response(400, {"code": "validation_error", "message": 'Body must be JSON like {"status": "Preparing"}.'})
    if target not in STATUS_RANK:
        return json_response(400, {"code": "validation_error", "message": "Unknown status."})

    entities = load_rows(rows)
    if not entities:
        return json_response(404, {"code": "not_found", "message": "Order not found."})

    current = max(entities, key=lambda e: e.get("statusRank", 0))
    if not can_move(current["status"], target):
        return json_response(409, {"code": "invalid_transition",
                                   "message": f"Cannot move from {current['status']} to {target}."})

    rank = STATUS_RANK[target]
    now = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    status_row.set(json.dumps({
        "PartitionKey": order_id,
        "RowKey": f"status-{rank}",
        "status": target,
        "statusRank": rank,
        "updatedAt": now,
    }))
    notify_msg.set(json.dumps({"orderId": order_id, "status": target, "rank": rank}))

    return json_response(200, {"orderId": order_id, "status": target, "updatedAt": now})