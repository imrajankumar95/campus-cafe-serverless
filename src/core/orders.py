import re
from dataclasses import dataclass


MENU_PRICES_CENTS = {
    "espresso": 295,
    "americano": 325,
    "latte": 445,
    "cappuccino": 445,
    "mocha": 495,
    "cold-brew": 425,
    "iced-latte": 475,
    "iced-caramel": 545,
    "iced-americano": 375,
    "matcha-latte": 525,
    "croissant": 325,
    "muffin": 325,
    "bagel": 375,
    "chicken-sandwich": 845,
    "avocado-toast": 895,
}
STATUS_RANKS = {
    "Accepted": 1,
    "Preparing": 2,
    "Ready": 3,
    "Collected": 4,
}
EMAIL_DOMAINS = {"georgebrown.ca", "gmail.com"}
EMAIL_PATTERN = re.compile(r"^[^@\s]+@[^@\s]+\.[^@\s]+$")


@dataclass
class OrderValidationError(Exception):
    code: str
    message: str
    status_code: int = 400


def validate_order(payload):
    if not isinstance(payload, dict):
        raise OrderValidationError("validation_error", "Request body must be a JSON object.")

    pickup_name = payload.get("pickupName")
    if not isinstance(pickup_name, str):
        raise OrderValidationError("validation_error", "Pickup name is required.")
    pickup_name = pickup_name.strip()
    if not pickup_name or len(pickup_name) > 40:
        raise OrderValidationError("validation_error", "Pickup name must be 1–40 characters.")

    email = payload.get("email")
    if not isinstance(email, str):
        raise OrderValidationError("validation_error", "A valid email is required.")
    email = email.strip()
    if len(email) > 100 or not EMAIL_PATTERN.fullmatch(email):
        raise OrderValidationError("validation_error", "A valid email is required.")
    if email.rsplit("@", 1)[1].lower() not in EMAIL_DOMAINS:
        raise OrderValidationError("validation_error", "Email domain must be georgebrown.ca or gmail.com.")

    items = payload.get("items")
    if not isinstance(items, list) or not 1 <= len(items) <= 10:
        raise OrderValidationError("validation_error", "An order must contain 1–10 item lines.")

    normalized_items = []
    seen_ids = set()
    total_cents = 0
    for item in items:
        if not isinstance(item, dict):
            raise OrderValidationError("validation_error", "Each item must be an object.")
        item_id = item.get("id")
        if not isinstance(item_id, str) or item_id not in MENU_PRICES_CENTS:
            raise OrderValidationError("validation_error", "Item is not on the menu.")
        if item_id in seen_ids:
            raise OrderValidationError("validation_error", "Duplicate item IDs are not allowed.")
        seen_ids.add(item_id)

        quantity = item.get("qty")
        if isinstance(quantity, bool) or not isinstance(quantity, int) or not 1 <= quantity <= 10:
            raise OrderValidationError("validation_error", "Quantity must be a whole number from 1 to 10.")

        normalized_items.append({"id": item_id, "qty": quantity})
        total_cents += MENU_PRICES_CENTS[item_id] * quantity

    return {
        "pickupName": pickup_name,
        "email": email,
        "items": normalized_items,
        "total": total_cents / 100,
    }


def next_status(current_status, requested_status):
    if requested_status not in STATUS_RANKS:
        raise OrderValidationError("validation_error", "Unknown order status.")
    if STATUS_RANKS[requested_status] != STATUS_RANKS.get(current_status, 0) + 1:
        raise OrderValidationError(
            "invalid_transition",
            "Status must move forward by exactly one step.",
            409,
        )
    return STATUS_RANKS[requested_status]
