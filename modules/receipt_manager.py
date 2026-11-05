"""
Receipt Manager Module.
Handles converting HTML receipts to PDF, capturing screenshots of assembled robots,
and embedding the screenshot into the PDF receipt.
"""

from pathlib import Path
from robocorp import browser
from RPA.PDF import PDF
from config import RECEIPTS_DIR, SCREENSHOTS_DIR


def store_receipt_as_pdf(order_number: str) -> str:
    """
    Extracts the receipt HTML from the page and exports it as a PDF document.

    Args:
        order_number: Unique identifier for the order.

    Returns:
        Path to the generated PDF file.
    """
    page = browser.page()
    receipt_html = page.locator("#receipt").inner_html()

    pdf_path = RECEIPTS_DIR / f"receipt_{order_number}.pdf"

    pdf = PDF()
    pdf.html_to_pdf(receipt_html, str(pdf_path))

    return str(pdf_path)


def take_robot_screenshot(order_number: str) -> str:
    """
    Captures a screenshot of the assembled robot preview on the page.

    Args:
        order_number: Unique identifier for the order.

    Returns:
        Path to the saved screenshot image.
    """
    page = browser.page()
    screenshot_path = SCREENSHOTS_DIR / f"robot_{order_number}.png"

    page.locator("#robot-preview-image").screenshot(path=str(screenshot_path))

    return str(screenshot_path)


def embed_screenshot_to_receipt(screenshot_path: str, pdf_path: str):
    """
    Embeds the captured robot image into the PDF receipt document.

    Args:
        screenshot_path: Path to the robot image screenshot.
        pdf_path: Path to the target PDF receipt.
    """
    pdf = PDF()
    pdf.add_watermark_image_to_pdf(
        image_path=screenshot_path,
        source_path=pdf_path,
        output_path=pdf_path,
    )

