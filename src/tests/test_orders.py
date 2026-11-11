import pytest

from core.orders import ValidationError, can_move, total_cents, validate_order


def make_order(**overrides):
    order = {
        "pickupName": "Sam",
        "email": "sam@georgebrown.ca",
        "items": [{"id": "latte", "qty": 2}],
    }
    order.update(overrides)
    return order


def test_valid_order_is_cleaned():
    result = validate_order(make_order(pickupName="  Sam ", email="SAM@Gmail.com"))
    assert result["pickupName"] == "Sam"
    assert result["email"] == "sam@gmail.com"


@pytest.mark.parametrize(
    "overrides",
    [
        {"pickupName": ""},
        {"pickupName": "x" * 41},
        {"email": "not-an-email"},
        {"email": "sam@yahoo.com"},
        {"items": []},
        {"items": [{"id": "pizza", "qty": 1}]},
        {"items": [{"id": "latte", "qty": 0}]},
        {"items": [{"id": "latte", "qty": 11}]},
        {"items": [{"id": "latte", "qty": "2"}]},
        {"items": [{"id": "latte", "qty": True}]},
        {"items": [{"id": "latte", "qty": 1}, {"id": "latte", "qty": 1}]},
    ],
)
def test_invalid_orders_are_rejected(overrides):
    with pytest.raises(ValidationError):
        validate_order(make_order(**overrides))


def test_body_must_be_an_object():
    with pytest.raises(ValidationError):
        validate_order(["not", "a", "dict"])


def test_total_is_calculated_from_server_prices():
    items = [{"id": "latte", "qty": 2}, {"id": "croissant", "qty": 1}]
    assert total_cents(items) == 445 * 2 + 325


@pytest.mark.parametrize(
    "current, target, allowed",
    [
        ("Accepted", "Preparing", True),
        ("Preparing", "Ready", True),
        ("Ready", "Collected", True),
        ("Accepted", "Ready", False),      # skips a step
        ("Ready", "Preparing", False),     # goes backward
        ("Collected", "Collected", False), # no move
        ("Accepted", "Cancelled", False),  # unknown status
    ],
)
def test_status_moves_forward_one_step_only(current, target, allowed):
    assert can_move(current, target) is allowed