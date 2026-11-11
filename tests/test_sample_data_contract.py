"""Local sanity test for the tiny synthetic CSV contract; does not require Azure or Spark."""
import csv
import unittest
from pathlib import Path


class SampleDataContractTests(unittest.TestCase):
    def test_sample_has_required_columns_and_unique_line_ids(self):
        path = Path(__file__).parents[1] / "data" / "sample" / "sales.csv"
        with path.open(newline="", encoding="utf-8") as source:
            rows = list(csv.DictReader(source))
        self.assertTrue(rows)
        required = {
            "order_id", "order_line_id", "order_date", "customer_id", "product_id",
            "product_name", "store_id", "quantity", "unit_price", "discount_pct"
        }
        self.assertTrue(required.issubset(rows[0].keys()))
        line_ids = [row["order_line_id"] for row in rows]
        self.assertEqual(len(line_ids), len(set(line_ids)))

    def test_sample_values_follow_basic_rules(self):
        path = Path(__file__).parents[1] / "data" / "sample" / "sales.csv"
        with path.open(newline="", encoding="utf-8") as source:
            rows = list(csv.DictReader(source))
        for row in rows:
            self.assertGreater(int(row["quantity"]), 0)
            self.assertGreaterEqual(float(row["unit_price"]), 0)
            self.assertGreaterEqual(float(row["discount_pct"]), 0)
            self.assertLessEqual(float(row["discount_pct"]), 1)


if __name__ == "__main__":
    unittest.main()
