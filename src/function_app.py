import json
import logging
import os
import uuid
from datetime import datetime, timedelta, timezone

import azure.functions as func
from azure.communication.email import EmailClient
from azure.core import MatchConditions
from azure.core.exceptions import ResourceModifiedError, ResourceNotFoundError
from azure.identity import DefaultAzureCredential
from azure.data.tables import UpdateMode

from core.orders import (
    STATUS_RANKS,
    OrderValidationError,
    next_status,
    validate_order,
)
from core.storage import notify_queue, table_client

app = func.FunctionApp()
MAX_REQUEST_BYTES = 4096
NOTIFIABLE_STATUSES = {"Accepted", "Preparing", "Ready"}
STATUS_FLAGS = {
    "Accepted": "notifyAccepted",
    "Preparing": "notifyPreparing",
    "Ready": "notifyReady",
}


def json_response(body, status_code=200):
    return func.HttpResponse(
        json.dumps(body),
        status_code=status_code,
        mimetype="application/json",
    )


def error_response(code, message, status_code):
    return json_response({"code": code, "message": message}, status_code)


def utc_now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z")


def get_order_id(raw_order_id):
    try:
        return str(uuid.UUID(raw_order_id))
    except (ValueError, AttributeError, TypeError):
        raise OrderValidationError("validation_error", "Order ID must be a GUID.")


def entity_etag(entity):
    metadata = getattr(entity, "metadata", None)
    if metadata is not None:
        etag = getattr(metadata, "etag", None)
        if etag:
            return etag
        if hasattr(metadata, "get"):
            etag = metadata.get("etag")
            if etag:
                return etag
    etag = entity.get("etag")
    if not etag:
        raise RuntimeError("The order entity did not include an ETag.")
    return etag


def public_order(entity):
    return {
        "orderId": entity["PartitionKey"],
        "status": entity["status"],
        "pickupName": entity["pickupName"],
        "createdAt": entity["createdAt"],
        "updatedAt": entity["updatedAt"],
    }


def notification_message(order_id, status):
    return json.dumps(
        {"orderId": order_id, "status": status, "rank": STATUS_RANKS[status]},
        separators=(",", ":"),
    )


@app.route(route="health", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def health(req: func.HttpRequest) -> func.HttpResponse:
    return json_response({"status": "ok"})


@app.route(route="orders", methods=["POST"], auth_level=func.AuthLevel.ANONYMOUS)
def submit_order(req: func.HttpRequest) -> func.HttpResponse:
    body = req.get_body()
    if len(body) > MAX_REQUEST_BYTES:
        return error_response("payload_too_large", "Request body must be 4 KB or smaller.", 413)
    try:
        payload = json.loads(body)
        order = validate_order(payload)
        order_id = str(uuid.uuid4())
        now = utc_now()
        entity = {
            "PartitionKey": order_id,
            "RowKey": "order",
            "pickupName": order["pickupName"],
            "email": order["email"],
            "itemsJson": json.dumps(order["items"], separators=(",", ":")),
            "total": order["total"],
            "status": "Accepted",
            "statusRank": STATUS_RANKS["Accepted"],
            "notifyAccepted": "pending",
            "notifyPreparing": "pending",
            "notifyReady": "pending",
            "createdAt": now,
            "updatedAt": now,
        }
        table_client().create_entity(entity=entity)
        notify_queue().send_message(notification_message(order_id, "Accepted"))
        return json_response(
            {"orderId": order_id, "status": "Accepted", "total": order["total"]},
            202,
        )
    except OrderValidationError as exc:
        return error_response(exc.code, exc.message, exc.status_code)
    except (json.JSONDecodeError, UnicodeDecodeError):
        return error_response("validation_error", "Request body must be valid JSON.", 400)
    except Exception:
        logging.exception("Failed to submit order.")
        return error_response("internal_error", "The order could not be placed.", 500)


@app.route(route="orders/{orderId}", methods=["GET"], auth_level=func.AuthLevel.ANONYMOUS)
def get_order(req: func.HttpRequest) -> func.HttpResponse:
    try:
        order_id = get_order_id(req.route_params.get("orderId"))
        entity = table_client().get_entity(partition_key=order_id, row_key="order")
        return json_response(public_order(entity))
    except OrderValidationError as exc:
        return error_response(exc.code, exc.message, exc.status_code)
    except ResourceNotFoundError:
        return error_response("not_found", "No order found with that ID.", 404)
    except Exception:
        logging.exception("Failed to retrieve order.")
        return error_response("internal_error", "The order could not be retrieved.", 500)


@app.route(
    route="orders/{orderId}/status",
    methods=["PUT"],
    auth_level=func.AuthLevel.FUNCTION,
)
def update_order_status(req: func.HttpRequest) -> func.HttpResponse:
    try:
        body = req.get_body()
        if len(body) > MAX_REQUEST_BYTES:
            return error_response("payload_too_large", "Request body must be 4 KB or smaller.", 413)
        order_id = get_order_id(req.route_params.get("orderId"))
        try:
            payload = json.loads(body)
        except (json.JSONDecodeError, UnicodeDecodeError):
            return error_response("validation_error", "Request body must be valid JSON.", 400)
        if not isinstance(payload, dict):
            return error_response("validation_error", "Request body must be a JSON object.", 400)

        requested_status = payload.get("status")
        if not isinstance(requested_status, str):
            return error_response("validation_error", "Status is required.", 400)

        table = table_client()
        entity = table.get_entity(partition_key=order_id, row_key="order")
        next_rank = next_status(entity["status"], requested_status)
        entity["status"] = requested_status
        entity["statusRank"] = next_rank
        entity["updatedAt"] = utc_now()
        table.update_entity(
            entity=entity,
            mode=UpdateMode.REPLACE,
            etag=entity_etag(entity),
            match_condition=MatchConditions.IfNotModified,
        )
        if requested_status in NOTIFIABLE_STATUSES:
            notify_queue().send_message(notification_message(order_id, requested_status))
        return json_response(public_order(entity))
    except OrderValidationError as exc:
        return error_response(exc.code, exc.message, exc.status_code)
    except ResourceNotFoundError:
        return error_response("not_found", "No order found with that ID.", 404)
    except ResourceModifiedError:
        return error_response("conflict", "Another update changed this order. Try again.", 409)
    except Exception:
        logging.exception("Failed to update order status.")
        return error_response("internal_error", "The order status could not be updated.", 500)


def send_email(entity, status):
    mode = os.getenv("EMAIL_MODE", "log").lower()
    if mode == "log":
        logging.info(
            "Notification logged for orderId=%s status=%s",
            entity["PartitionKey"],
            status,
        )
        return
    if mode != "acs":
        raise RuntimeError("EMAIL_MODE must be 'log' or 'acs'.")

    endpoint = os.getenv("ACS_ENDPOINT")
    sender = os.getenv("EMAIL_SENDER")
    if not endpoint or not sender:
        raise RuntimeError("ACS_ENDPOINT and EMAIL_SENDER are required when EMAIL_MODE=acs.")
    client = EmailClient(endpoint, DefaultAzureCredential())
    message = {
        "senderAddress": sender,
        "recipients": {"to": [{"address": entity["email"]}]},
        "content": {
            "subject": f"Campus Café order {status}",
            "plainText": (
                f"Hi {entity['pickupName']}, your Campus Café order "
                f"{entity['PartitionKey']} is {status.lower()}."
            ),
        },
    }
    client.begin_send(message).result()


@app.queue_trigger(
    arg_name="message",
    queue_name="notify",
    connection="AzureWebJobsStorage",
)
def send_notification(message: func.QueueMessage) -> None:
    notification = json.loads(message.get_body().decode("utf-8"))
    order_id = get_order_id(notification.get("orderId"))
    status = notification.get("status")
    rank = notification.get("rank")
    if status not in STATUS_FLAGS or rank != STATUS_RANKS[status]:
        raise ValueError("Queue message has an invalid notification status or rank.")

    table = table_client()
    entity = table.get_entity(partition_key=order_id, row_key="order")
    if entity["statusRank"] > rank:
        logging.info("Skipped outdated notification orderId=%s rank=%s", order_id, rank)
        return

    flag = STATUS_FLAGS[status]
    if entity[flag] == "sent":
        logging.info("Skipped duplicate notification orderId=%s status=%s", order_id, status)
        return

    claim_time = datetime.now(timezone.utc)
    claimed_at = entity.get(f"{flag}ClaimedAt")
    if entity[flag] == "sending" and claimed_at:
        try:
            previous_claim = datetime.fromisoformat(claimed_at.replace("Z", "+00:00"))
            if claim_time - previous_claim < timedelta(minutes=5):
                logging.info("Notification already processing orderId=%s status=%s", order_id, status)
                return
        except ValueError:
            logging.warning("Invalid notification claim timestamp for orderId=%s", order_id)

    entity[flag] = "sending"
    entity[f"{flag}ClaimedAt"] = utc_now()
    try:
        table.update_entity(
            entity=entity,
            mode=UpdateMode.REPLACE,
            etag=entity_etag(entity),
            match_condition=MatchConditions.IfNotModified,
        )
    except ResourceModifiedError:
        logging.info("Skipped concurrent notification claim orderId=%s status=%s", order_id, status)
        return

    try:
        send_email(entity, status)
        entity = table.get_entity(partition_key=order_id, row_key="order")
        entity[flag] = "sent"
        entity.pop(f"{flag}ClaimedAt", None)
        table.update_entity(
            entity=entity,
            mode=UpdateMode.REPLACE,
            etag=entity_etag(entity),
            match_condition=MatchConditions.IfNotModified,
        )
    except Exception:
        logging.exception("Notification delivery failed for orderId=%s status=%s", order_id, status)
        try:
            entity = table.get_entity(partition_key=order_id, row_key="order")
            if entity[flag] == "sending":
                entity[flag] = "pending"
                entity.pop(f"{flag}ClaimedAt", None)
                table.update_entity(
                    entity=entity,
                    mode=UpdateMode.REPLACE,
                    etag=entity_etag(entity),
                    match_condition=MatchConditions.IfNotModified,
                )
        except (ResourceNotFoundError, ResourceModifiedError):
            logging.warning("Could not release notification claim orderId=%s status=%s", order_id, status)
        raise
