"""Order rules: validation of new orders and the status lifecycle.

Pure Python with no Azure imports, so it is fast and easy to unit test.
"""
import re

from core.menu import is_on_menu, price_cents

ALLOWED_EMAIL_DOMAINS = {"georgebrown.ca", "gmail.com"}
MAX_NAME_LENGTH = 40
MAX_LINES = 10
MAX_QTY = 10

# Lifecycle: each status has a rank; staff can only move forward one step.
STATUS_RANK = {"Accepted": 1, "Preparing": 2, "Ready": 3, "Collected": 4}
NOTIFY_STATUSES = {"Accepted", "Preparing", "Ready"}  # Collected sends no email

EMAIL_PATTERN = re.compile(r"^[^@\s]+@([^@\s]+\.[^@\s]+)$")


class ValidationError(Exception):
    """Raised when an order breaks a rule. The message is safe to show the user."""


def validate_order(body) -> dict:
    """Check a POST /api/orders body. Return a clean order or raise ValidationError."""
    if not isinstance(body, dict):
        raise ValidationError("Request body must be a JSON object.")

    name = body.get("pickupName")
    if not isinstance(name, str) or not name.strip():
        raise ValidationError("Please enter a name for pickup.")
    name = name.strip()
    if len(name) > MAX_NAME_LENGTH:
        raise ValidationError(f"Name must be at most {MAX_NAME_LENGTH} characters.")

    email = body.get("email")
    if not isinstance(email, str):
        raise ValidationError("Please enter a valid email.")
    email = email.strip().lower()
    match = EMAIL_PATTERN.match(email)
    if not match:
        raise ValidationError("Please enter a valid email.")
    if match.group(1) not in ALLOWED_EMAIL_DOMAINS:
        raise ValidationError("Only @georgebrown.ca and @gmail.com emails are accepted.")

    items = body.get("items")
    if not isinstance(items, list) or not items:
        raise ValidationError("Your order is empty.")
    if len(items) > MAX_LINES:
        raise ValidationError(f"An order can have at most {MAX_LINES} different items.")

    clean_items = []
    seen = set()
    for line in items:
        if not isinstance(line, dict):
            raise ValidationError("Each item must have an id and qty.")
        item_id = line.get("id")
        qty = line.get("qty")
        if not isinstance(item_id, str) or not is_on_menu(item_id):
            raise ValidationError("One of the items is not on the menu.")
        if item_id in seen:
            raise ValidationError("Each item can appear only once.")
        # bool is a subclass of int in Python, so reject True/False explicitly.
        if not isinstance(qty, int) or isinstance(qty, bool) or not 1 <= qty <= MAX_QTY:
            raise ValidationError(f"Quantity must be between 1 and {MAX_QTY}.")
        seen.add(item_id)
        clean_items.append({"id": item_id, "qty": qty})

    return {"pickupName": name, "email": email, "items": clean_items}


def total_cents(items) -> int:
    return sum(price_cents(line["id"]) * line["qty"] for line in items)


def can_move(current: str, target: str) -> bool:
    """Staff can only move an order forward exactly one step."""
    if current not in STATUS_RANK or target not in STATUS_RANK:
        return False
    return STATUS_RANK[target] == STATUS_RANK[current] + 1