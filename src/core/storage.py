import os
from functools import lru_cache

from azure.core.exceptions import ResourceExistsError
from azure.data.tables import TableServiceClient
from azure.identity import DefaultAzureCredential
from azure.storage.queue import QueueClient


@lru_cache(maxsize=1)
def table_client():
    connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    if connection_string:
        service = TableServiceClient.from_connection_string(connection_string)
    else:
        account_name = os.getenv("AzureWebJobsStorage__accountName")
        if not account_name:
            raise RuntimeError("Set AzureWebJobsStorage__accountName or STORAGE_CONNECTION_STRING.")
        credential = DefaultAzureCredential()
        service = TableServiceClient(
            endpoint=f"https://{account_name}.table.core.windows.net",
            credential=credential,
        )
    try:
        service.create_table(table_name="orders")
    except ResourceExistsError:
        pass
    return service.get_table_client("orders")


@lru_cache(maxsize=1)
def notify_queue():
    connection_string = os.getenv("STORAGE_CONNECTION_STRING")
    if connection_string:
        client = QueueClient.from_connection_string(connection_string, "notify")
    else:
        account_name = os.getenv("AzureWebJobsStorage__accountName")
        if not account_name:
            raise RuntimeError("Set AzureWebJobsStorage__accountName or STORAGE_CONNECTION_STRING.")
        client = QueueClient(
            account_url=f"https://{account_name}.queue.core.windows.net",
            queue_name="notify",
            credential=DefaultAzureCredential(),
        )
    try:
        client.create_queue()
    except ResourceExistsError:
        pass
    return client
