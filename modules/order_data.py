"""
Order Data Management Module.
Handles downloading, reading, and parsing the orders CSV file.
"""

from typing import List, Dict, Any
from RPA.HTTP import HTTP
from RPA.Tables import Tables
from config import ORDERS_CSV_URL, ORDERS_CSV_PATH


def download_orders_csv(url: str = ORDERS_CSV_URL, target_path: str = str(ORDERS_CSV_PATH)) -> str:
    """
    Downloads the orders CSV file from the given URL.

    Args:
        url: The download URL for the orders CSV.
        target_path: Local filesystem destination path.

    Returns:
        The target path of the downloaded file.
    """
    http = HTTP()
    http.download(
        url=url,
        target_file=target_path,
        overwrite=True,
    )
    return target_path


def load_orders(csv_path: str = str(ORDERS_CSV_PATH)) -> List[Dict[str, Any]]:
    """
    Reads the downloaded CSV file and converts it into a list of row dictionaries.

    Args:
        csv_path: Local path to the orders CSV file.

    Returns:
        List of order dictionaries containing Order number, Head, Body, Legs, and Address.
    """
    tables = Tables()
    table = tables.read_table_from_csv(
        path=csv_path,
        header=True,
    )

    orders: List[Dict[str, Any]] = []
    for row in table:
        orders.append({
            "Order number": str(row["Order number"]).strip(),
            "Head": str(row["Head"]).strip(),
            "Body": str(row["Body"]).strip(),
            "Legs": str(row["Legs"]).strip(),
            "Address": str(row["Address"]).strip(),
        })

    return orders

