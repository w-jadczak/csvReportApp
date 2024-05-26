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

class TestDataProcessor(SetUpTestData):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.df = pd.read_csv(cls.csv_file_path)
        cls.processor = DataProcessor(cls.df)

    def test_total_products(self):
        # Given & Then:
        self.assertEqual(self.processor.total_products(), PRODUCTS_NUM)

    def test_average_price(self):
        # Given:
        expected_average_price = self.df["Price"].mean()
        # Then:
        self.assertEqual(self.processor.average_price(), expected_average_price)

    def test_total_value(self):
        # Given:
        expected_total_value = (self.df['Price'] * self.df['Quantity']).sum()
        # Then:
        self.assertEqual(self.processor.total_value(), expected_total_value)

    def test_most_expensive_product_per_category(self):
        # Given:
        expected_df = self.df.loc[self.df.groupby('Category')['Price'].idxmax(), ['Category', 'Name', 'Price']]
        result_df = self.processor.most_expensive_product_per_category()
        # Then:
        pd.testing.assert_frame_equal(result_df.reset_index(drop=True), expected_df.reset_index(drop=True))

class TestDataframeLoader(SetUpTestData):
    def test_load_dataframe(self):
        # Given:
        loader = DataframeLoader(self.csv_file_path)
        # When:
        df = loader.load_data()
        # Then:
        self.assertFalse(df.empty)
        self.assertEqual(len(df), PRODUCTS_NUM)
        self.assertListEqual(list(df.columns), ["ID", "Name", "Category", "Price", "Quantity"])

class TestInputCsvValidator(unittest.TestCase):
    def setUp(self):
        # Given:
        self.validator = InputCsvValidator()

    def test_validate_data_not_empty(self):
        # When:
        df = pd.DataFrame({"ID": [1], "Name": ["Product"], "Category": ["Category"], "Price": [10], "Quantity": [1]})
        # Then:
        self.assertIsNone(self.validator.validate_data(df))

        # When:
        df_empty = pd.DataFrame()
        # Then:
        with self.assertRaises(ValueError):
            self.validator.validate_data(df_empty)

    def test_validate_columns(self):
        # When:
        df = pd.DataFrame({"ID": [1], "Name": ["Product"], "Category": ["Category"], "Price": [10], "Quantity": [1]})
        # Then:
        self.assertIsNone(self.validator._validate_columns(df))

        # When:
        df_missing_column = pd.DataFrame({"ID": [1], "Name": ["Product"], "Price": [10], "Quantity": [1]})
        # Then:
        with self.assertRaises(ValueError):
            self.validator._validate_columns(df_missing_column)

    def test_validate_path(self):
        # When:
        with patch("os.path.exists", return_value=True):
            # Then:
            self.assertIsNone(self.validator.validate_path("existing_path.csv"))

        # When:
        with self.assertRaises(FileNotFoundError):
            # Then:
            self.validator.validate_path("non_existing_path.csv")

class TestReportGenerator(SetUpTestData):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Given:
        cls.df = pd.read_csv(cls.csv_file_path)
        cls.processor = DataProcessor(cls.df)
        cls.report_generator = ReportGenerator(cls.processor)
        cls.report_file_path = 'test_report.csv'

    @classmethod
    def tearDownClass(cls):
        super().tearDownClass()
        if os.path.exists(cls.report_file_path):
            os.remove(cls.report_file_path)

    def test_generate_report(self):
        # When:
        self.report_generator.generate_report(self.report_file_path)

        # Then:
        self.assertTrue(os.path.exists(self.report_file_path))

        # When:
        with open(self.report_file_path, 'r') as file:
            general_data = pd.read_csv(file, nrows=3)
            file.seek(0)
            specific_data = pd.read_csv(file, skiprows=4)

        # Then:
        expected_general_data = pd.DataFrame({
            'Data': ['Total products', 'Average price', 'Total stock value'],
            'Value': [
                int(self.processor.total_products()),
                round(self.processor.average_price(), 2),
                round(self.processor.total_value(), 2)
            ]
        })
        pd.testing.assert_frame_equal(general_data, expected_general_data)

        # Then:
        most_expensive_data = {
            'Category': self.processor.most_expensive_product_per_category()['Category'],
            'Most expensive product': self.processor.most_expensive_product_per_category()['Name'],
            'Price': self.processor.most_expensive_product_per_category()['Price']
        }
        expected_specific_data = pd.DataFrame(most_expensive_data)
        expected_specific_data.reset_index(drop=True, inplace=True)
        specific_data.reset_index(drop=True, inplace=True)
        pd.testing.assert_frame_equal(specific_data, expected_specific_data)

if __name__ == "__main__":
    unittest.main()
