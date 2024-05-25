import unittest
import pandas as pd
import os
from unittest.mock import patch
from service.data_service import DataframeLoader, DataProcessor, ReportGenerator
from validator.csv_validator import InputCsvValidator
from test_utils.data_generator import TestCsvGenerator

PRODUCTS_NUM = 10

class SetUpTestData(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        csv_generator = TestCsvGenerator()
        cls.csv_file_path = csv_generator.generate_test_csv(num_products=PRODUCTS_NUM)

    @classmethod
    def tearDownClass(cls):
        os.remove(cls.csv_file_path)
class TestDataframeLoader(SetUpTestData):

    def test_load_dataframe(self):
        loader = DataframeLoader(self.csv_file_path)
        df = loader.load_data()
        self.assertFalse(df.empty)
        self.assertEqual(len(df), PRODUCTS_NUM)
        self.assertListEqual(list(df.columns), ["ID", "Name", "Category", "Price", "Quantity"])

class TestInputCsvValidator(unittest.TestCase):

    def setUp(self):
        self.validator = InputCsvValidator()

    def test_validate_data_not_empty(self):
        df = pd.DataFrame({"ID": [1], "Name": ["Product"], "Category": ["Category"], "Price": [10], "Quantity": [1]})
        self.assertIsNone(self.validator.validate_data(df))

        df_empty = pd.DataFrame()
        with self.assertRaises(ValueError):
            self.validator.validate_data(df_empty)

    def test_validate_columns(self):

        df = pd.DataFrame({"ID": [1], "Name": ["Product"], "Category": ["Category"], "Price": [10], "Quantity": [1]})
        self.assertIsNone(self.validator._validate_columns(df))

        df_missing_column = pd.DataFrame({"ID": [1], "Name": ["Product"], "Price": [10], "Quantity": [1]})
        with self.assertRaises(ValueError):
            self.validator._validate_columns(df_missing_column)

    def test_validate_path(self):

        with patch("os.path.exists", return_value=True):
            self.assertIsNone(self.validator.validate_path("existing_path.csv"))

        with self.assertRaises(FileNotFoundError):
            self.validator.validate_path("non_existing_path.csv")

if __name__ == "__main__":
    unittest.main()
