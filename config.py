"""
Configuration and constants for the Robot Order Process automation.
Centralizes URLs, file paths, selectors, and execution parameters.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
OUTPUT_DIR = BASE_DIR / "output"
RECEIPTS_DIR = OUTPUT_DIR / "receipts"
SCREENSHOTS_DIR = OUTPUT_DIR / "screenshots"

# File Paths
ORDERS_CSV_PATH = OUTPUT_DIR / "orders.csv"
ARCHIVE_ZIP_PATH = OUTPUT_DIR / "orders.zip"

# Remote URLs
ROBOT_ORDER_URL = "https://robotsparebinindustries.com/#/robot-order"
ORDERS_CSV_URL = "https://robotsparebinindustries.com/orders.csv"

# Automation Parameters
MAX_SUBMIT_RETRIES = 10
RETRY_DELAY_SEC = 0.5

# Browser Configuration
BROWSER_HEADLESS = False
BROWSER_SLOWMO = 100


def ensure_directories_exist():
    """Ensure all required output directories exist before processing."""
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    RECEIPTS_DIR.mkdir(parents=True, exist_ok=True)
    SCREENSHOTS_DIR.mkdir(parents=True, exist_ok=True)

