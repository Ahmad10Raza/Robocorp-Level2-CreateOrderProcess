import os
import unittest
import tempfile
from pathlib import Path
import config
from modules.order_data import load_orders
from modules.archiver import archive_receipts


class TestRobotOrderModules(unittest.TestCase):
    def test_config_paths(self):
        config.ensure_directories_exist()
        self.assertTrue(config.OUTPUT_DIR.exists())
        self.assertTrue(config.RECEIPTS_DIR.exists())
        self.assertTrue(config.SCREENSHOTS_DIR.exists())

    def test_load_orders(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            test_csv = Path(tmpdir) / "test_orders.csv"
            test_csv.write_text(
                "Order number,Head,Body,Legs,Address\n"
                "1,1,2,3,Test Address 123\n"
                "2,4,1,5,Test Address 456\n"
            )

            orders = load_orders(str(test_csv))
            self.assertEqual(len(orders), 2)
            self.assertEqual(orders[0]["Order number"], "1")
            self.assertEqual(orders[0]["Head"], "1")
            self.assertEqual(orders[0]["Body"], "2")
            self.assertEqual(orders[0]["Legs"], "3")
            self.assertEqual(orders[0]["Address"], "Test Address 123")

    def test_archive_receipts(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            receipts_dir = Path(tmpdir) / "receipts"
            receipts_dir.mkdir()
            pdf_sample = receipts_dir / "receipt_1.pdf"
            pdf_sample.write_text("%PDF-1.4 mock")

            zip_path = Path(tmpdir) / "orders.zip"
            result = archive_receipts(str(receipts_dir), str(zip_path))

            self.assertTrue(os.path.exists(result))
            self.assertEqual(result, str(zip_path))


if __name__ == "__main__":
    unittest.main()
