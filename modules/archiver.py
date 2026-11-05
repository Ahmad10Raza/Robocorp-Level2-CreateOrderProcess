"""
Archiver Module.
Handles packaging completed PDF receipts into a ZIP archive.
"""

import os
from pathlib import Path
from RPA.Archive import Archive
from config import RECEIPTS_DIR, ARCHIVE_ZIP_PATH


def archive_receipts(
    folder_path: str = str(RECEIPTS_DIR),
    archive_path: str = str(ARCHIVE_ZIP_PATH)
) -> str:
    """
    Archives all generated PDF receipts into a single ZIP file.

    Args:
        folder_path: Directory containing the PDF receipts.
        archive_path: Destination path for the ZIP archive.

    Returns:
        Path to the generated ZIP file.
    """
    # Remove existing archive if it already exists
    if os.path.exists(archive_path):
        os.remove(archive_path)

    archiver = Archive()
    archiver.archive_folder_with_zip(
        folder=folder_path,
        archive_name=archive_path,
        recursive=False,
        include="*.pdf",
    )

    return archive_path

