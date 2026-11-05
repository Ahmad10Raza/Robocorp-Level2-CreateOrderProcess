"""
RobotSpareBin Industries Inc. - Robot Order Automation
Robocorp Certificate Level II / Sema4.ai Action Implementation.

Orchestrates the entire end-to-end robot ordering workflow:
1. Downloads orders CSV data file.
2. Navigates to the robot ordering website.
3. Iterates over each order row:
   - Dismisses rights disclaimer modal.
   - Fills robot configuration form (head, body, legs, address).
   - Previews the assembled robot.
   - Submits the order with resilient retry logic on 500 server errors.
   - Stores the order receipt HTML as a PDF.
   - Captures a screenshot of the previewed robot.
   - Embeds the screenshot into the PDF receipt.
   - Clicks 'Order another robot' to reset the form.
4. Packages all generated PDF receipts into a single ZIP archive.
"""

from typing import Dict, Any, List
from sema4ai.actions import action
from robocorp import browser

import config
from modules.order_data import download_orders_csv, load_orders
from modules.order_web import (
    open_robot_order_website,
    close_annoying_modal,
    fill_order_form,
    preview_robot,
    submit_order_with_retry,
    order_another_robot,
)
from modules.receipt_manager import (
    store_receipt_as_pdf,
    take_robot_screenshot,
    embed_screenshot_to_receipt,
)
from modules.archiver import archive_receipts


@action
def order_robots_process() -> str:
    """
    Executes the RobotSpareBin robot ordering process:
    Downloads the orders CSV, opens the ordering portal, submits orders with retry logic,
    generates PDF receipts with embedded robot screenshots, and packages them into a ZIP archive.

    Returns:
        Summary message including the path to the generated ZIP archive.
    """
    # 1. Initialize output directories
    config.ensure_directories_exist()

    # 2. Configure browser execution
    browser.configure(
        headless=config.BROWSER_HEADLESS,
        slowmo=config.BROWSER_SLOWMO,
    )

    # 3. Download and parse order data
    print("Downloading orders CSV...")
    download_orders_csv(config.ORDERS_CSV_URL, str(config.ORDERS_CSV_PATH))
    orders: List[Dict[str, Any]] = load_orders(str(config.ORDERS_CSV_PATH))
    print(f"Loaded {len(orders)} orders to process.")

    # 4. Open ordering website
    print(f"Opening order portal: {config.ROBOT_ORDER_URL}")
    open_robot_order_website(config.ROBOT_ORDER_URL)

    # 5. Process each order sequentially
    for index, order in enumerate(orders, start=1):
        order_num = order["Order number"]
        print(f"[{index}/{len(orders)}] Processing Order #{order_num}...")

        # Dismiss modal on first load or after ordering another robot
        close_annoying_modal()

        # Fill the robot specifications
        fill_order_form(order)

        # Preview assembled robot
        preview_robot()

        # Submit order with automatic retry on intermittent server 500 errors
        submit_order_with_retry(max_retries=config.MAX_SUBMIT_RETRIES)

        # Capture PDF receipt and preview screenshot
        pdf_path = store_receipt_as_pdf(order_num)
        screenshot_path = take_robot_screenshot(order_num)

        # Embed screenshot into the PDF receipt
        embed_screenshot_to_receipt(screenshot_path, pdf_path)

        # Reset form for next order
        order_another_robot()

    # 6. Archive all PDF receipts into a ZIP file
    print("Archiving generated PDF receipts...")
    zip_path = archive_receipts(
        folder_path=str(config.RECEIPTS_DIR),
        archive_path=str(config.ARCHIVE_ZIP_PATH),
    )

    summary = (
        f"Robot order processing completed successfully!\n"
        f"- Total Orders Processed: {len(orders)}\n"
        f"- PDF Receipts Folder: {config.RECEIPTS_DIR}\n"
        f"- Screenshots Folder: {config.SCREENSHOTS_DIR}\n"
        f"- ZIP Archive Created: {zip_path}"
    )
    print(summary)
    return summary
