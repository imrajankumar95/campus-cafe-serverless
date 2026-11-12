import json
import sys
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

import azure.functions as func

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))
import function_app


def request(method, url, body=b"", route_params=None):
    return func.HttpRequest(
        method=method,
        url=url,
        headers={"Content-Type": "application/json"},
        params={},
        route_params=route_params or {},
        body=body,
    )


class FakeTable:
    def __init__(self, entity=None):
        self.entity = entity
        self.created = []
        self.updated = []

    def create_entity(self, entity):
        self.created.append(entity)

    def get_entity(self, partition_key, row_key):
        if self.entity is None:
            raise AssertionError("Unexpected order lookup.")
        return self.entity

    def update_entity(self, **kwargs):
        self.updated.append(kwargs)


class FakeQueue:
    def __init__(self):
        self.messages = []

    def send_message(self, message):
        self.messages.append(message)


class FakeEntity(dict):
    def __init__(self, *args, etag, **kwargs):
        super().__init__(*args, **kwargs)
        self.metadata = SimpleNamespace(etag=etag)


class FunctionHttpTests(unittest.TestCase):
    def test_submit_order_persists_server_total_and_enqueues_notification(self):
        table = FakeTable()
        queue = FakeQueue()
        body = json.dumps({
            "pickupName": "Sam",
            "email": "sam@gmail.com",
            "items": [{"id": "latte", "qty": 2}],
        }).encode()

        with patch.object(function_app, "table_client", return_value=table), patch.object(
            function_app, "notify_queue", return_value=queue
        ):
            response = function_app.submit_order(request("POST", "/api/orders", body))

        result = json.loads(response.get_body())
        self.assertEqual(response.status_code, 202)
        self.assertEqual(result["total"], 8.90)
        self.assertEqual(table.created[0]["total"], 8.90)
        self.assertEqual(json.loads(queue.messages[0])["status"], "Accepted")

    def test_submit_order_rejects_body_over_limit_without_storage_access(self):
        with patch.object(function_app, "table_client") as table:
            response = function_app.submit_order(
                request("POST", "/api/orders", b"x" * (function_app.MAX_REQUEST_BYTES + 1))
            )

        self.assertEqual(response.status_code, 413)
        table.assert_not_called()

    def test_get_order_does_not_return_private_order_data(self):
        entity = {
            "PartitionKey": "7e3170f2-fcb5-4db4-b482-2f237bef2e32",
            "RowKey": "order",
            "status": "Accepted",
            "pickupName": "Sam",
            "email": "sam@gmail.com",
            "itemsJson": '[{"id":"latte","qty":1}]',
            "createdAt": "2026-11-11T12:00:00Z",
            "updatedAt": "2026-11-11T12:00:00Z",
        }
        with patch.object(function_app, "table_client", return_value=FakeTable(entity)):
            response = function_app.get_order(
                request(
                    "GET",
                    "/api/orders/7e3170f2-fcb5-4db4-b482-2f237bef2e32",
                    route_params={"orderId": entity["PartitionKey"]},
                )
            )

        result = json.loads(response.get_body())
        self.assertEqual(response.status_code, 200)
        self.assertNotIn("email", result)
        self.assertNotIn("items", result)

    def test_status_update_uses_etag_and_enqueues_next_notification(self):
        order_id = "7e3170f2-fcb5-4db4-b482-2f237bef2e32"
        entity = FakeEntity(
            {
                "PartitionKey": order_id,
                "RowKey": "order",
                "status": "Accepted",
                "statusRank": 1,
                "pickupName": "Sam",
                "createdAt": "2026-11-11T12:00:00Z",
                "updatedAt": "2026-11-11T12:00:00Z",
            },
            etag="test-etag",
        )
        table = FakeTable(entity)
        queue = FakeQueue()
        body = json.dumps({"status": "Preparing"}).encode()

        with patch.object(function_app, "table_client", return_value=table), patch.object(
            function_app, "notify_queue", return_value=queue
        ):
            response = function_app.update_order_status(
                request(
                    "PUT",
                    f"/api/orders/{order_id}/status",
                    body,
                    route_params={"orderId": order_id},
                )
            )

        self.assertEqual(response.status_code, 200)
        self.assertEqual(table.updated[0]["etag"], "test-etag")
        self.assertEqual(json.loads(queue.messages[0])["status"], "Preparing")


if __name__ == "__main__":
    unittest.main()
