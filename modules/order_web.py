"""
Web Automation Module for Robot Spare Bin Industries order portal.
Handles navigation, modal dismissal, form entry, previewing, and resilient submission with retry.
"""

import time
from typing import Dict, Any
from robocorp import browser
from config import ROBOT_ORDER_URL, MAX_SUBMIT_RETRIES, RETRY_DELAY_SEC


def open_robot_order_website(url: str = ROBOT_ORDER_URL):
    """Navigates to the robot ordering page."""
    browser.goto(url)


def close_annoying_modal():
    """
    Dismisses the disclaimer/rights modal that appears on initial load
    and before each new order.
    """
    page = browser.page()
    # Selector handles various button variants ('OK', 'I guess so...', modal primary buttons)
    modal_button = page.locator(
        ".modal button:text('OK'), "
        ".modal button:text('I guess so...'), "
        ".modal button.btn-warning, "
        ".modal button.btn-dark"
    )

    if modal_button.count() > 0 and modal_button.first.is_visible():
        modal_button.first.click()


def fill_order_form(order: Dict[str, Any]):
    """
    Fills out the robot specifications in the order form.

    Args:
        order: Dictionary with keys 'Head', 'Body', 'Legs', and 'Address'.
    """
    page = browser.page()

    # 1. Select Head
    page.select_option("#head", str(order["Head"]))

    # 2. Select Body Radio Button
    body_selector = f"#id-body-{order['Body']}"
    page.click(body_selector)

    # 3. Enter number of Legs
    legs_selector = "input[placeholder='Enter the part number for the legs'], input[type='number']"
    page.fill(legs_selector, str(order["Legs"]))

    # 4. Enter Shipping Address
    page.fill("#address", str(order["Address"]))


def preview_robot():
    """Clicks the Preview button and waits for the robot preview image to load."""
    page = browser.page()
    page.click("button#preview")
    page.wait_for_selector("#robot-preview-image", state="visible", timeout=5000)


def submit_order_with_retry(max_retries: int = MAX_SUBMIT_RETRIES):
    """
    Submits the order by clicking the Order button.
    The RobotSpareBin server randomly throws a 500 alert error.
    This function implements retry logic until the receipt is displayed.

    Args:
        max_retries: Maximum number of submission attempts before raising an error.
    """
    page = browser.page()

    for attempt in range(1, max_retries + 1):
        page.click("button#order")

        # Check if receipt is already visible
        receipt_locator = page.locator("#receipt")
        if receipt_locator.is_visible():
            return

        # Check for server error alert
        error_locator = page.locator(".alert-danger")
        if error_locator.is_visible():
            print(f"Server error encountered on submission attempt {attempt}/{max_retries}. Retrying...")
            time.sleep(RETRY_DELAY_SEC)
            continue

        time.sleep(RETRY_DELAY_SEC)

    raise RuntimeError(
        f"Failed to submit order after {max_retries} attempts due to persistent server errors."
    )


def order_another_robot():
    """Clicks 'Order another robot' button to reset the form for the next order."""
    page = browser.page()
    page.click("button#order-another")

