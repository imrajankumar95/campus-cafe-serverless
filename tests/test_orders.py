import sys
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

from core.orders import OrderValidationError, next_status, validate_order


class ValidateOrderTests(unittest.TestCase):
    def setUp(self):
        self.payload = {
            "pickupName": " Sam ",
            "email": "sam@gmail.com",
            "items": [{"id": "latte", "qty": 2}, {"id": "croissant", "qty": 1}],
        }

    def test_trims_fields_and_calculates_total_from_server_menu(self):
        order = validate_order(self.payload)
        self.assertEqual(order["pickupName"], "Sam")
        self.assertEqual(order["email"], "sam@gmail.com")
        self.assertEqual(order["total"], 12.15)

    def test_rejects_duplicate_item_ids(self):
        self.payload["items"].append({"id": "latte", "qty": 1})
        with self.assertRaisesRegex(OrderValidationError, "Duplicate"):
            validate_order(self.payload)

    def test_rejects_boolean_quantity(self):
        self.payload["items"][0]["qty"] = True
        with self.assertRaisesRegex(OrderValidationError, "whole number"):
            validate_order(self.payload)

    def test_rejects_email_domain_outside_allow_list(self):
        self.payload["email"] = "sam@example.com"
        with self.assertRaisesRegex(OrderValidationError, "Email domain"):
            validate_order(self.payload)


class StatusTransitionTests(unittest.TestCase):
    def test_allows_only_next_forward_status(self):
        self.assertEqual(next_status("Accepted", "Preparing"), 2)
        with self.assertRaises(OrderValidationError) as error:
            next_status("Accepted", "Ready")
        self.assertEqual(error.exception.status_code, 409)

    def test_rejects_unknown_status(self):
        with self.assertRaises(OrderValidationError) as error:
            next_status("Accepted", "Cooking")
        self.assertEqual(error.exception.status_code, 400)


if __name__ == "__main__":
    unittest.main()
