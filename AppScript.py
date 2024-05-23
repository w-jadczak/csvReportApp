import pandas as pd
import os

class InputCsvValidator:
    def __init__(self):
        pass

    def validate_data(self, df: pd.DataFrame):
        self._validate_not_empty(df)
        self._validate_columns(df)

    def validate_path(self, path):
        if not os.path.exists(path):
            raise FileNotFoundError(f"Provided file path: {path} does not exist.")

    def _validate_not_empty(self, df: pd.DataFrame):
        if df.empty:
            raise ValueError("Provided CSV file cannot be empty.")

    def _validate_columns(self, df: pd.DataFrame):
        required_columns = {"ID", "Name", "Category", "Price", "Quantity"}
        if not required_columns.issubset(df.columns):
            missing_columns = required_columns - set(df.columns)
            raise ValueError(f"Provided CSV file is missing following columns: {', '.join(missing_columns)}")

class DataframeLoader:
    def __init__(self, path, validator: InputCsvValidator):
        self.path = path
        self.validator = validator

    def load_data(self):
        try:
            self.validator.validate_path(self.path)
            df = pd.read_csv(self.path)
            self.validator.validate_data(df)
            return df
        except (FileNotFoundError, ValueError) as e:
            print(f"Validation error: {e}")
            return None

class DataProcessor:
    def __init__(self, df: pd.DataFrame):
        self.df = df

    def total_products(self):
        return len(self.df)

    def average_price(self):
        return self.df["Price"].mean()

    def total_value(self):
        return (self.df['Price'] * self.df['Quantity']).sum()

    def most_expensive_product_per_category(self):
        idx =  self.df.groupby('Category')['Price'].idxmax()
        return self.df.loc[idx, ['Category', 'Name', 'Price']]

class ReportGenerator:
    def __init__(self, dp: DataProcessor):
        self.dp = dp

    def generate_report(self, output_csv_file_path):

        general_df = self._generate_general_dataframes()
        specific_df = self._generate_specific_dataframes()

        with open(output_csv_file_path, mode='w', newline='') as file:
            general_df.to_csv(file, index=False)
            file.write('\n')
            specific_df.to_csv(file, index=False, header=False)

    def _generate_general_dataframes(self):
        general_data = {
            'Data': ['Total products', 'Average price', 'Total stock value'],
            'Value': [
                int(self.dp.total_products()),
                round(self.dp.average_price(), 2),
                round(self.dp.total_value(), 2)
            ]
        }
        general_df = pd.DataFrame(general_data)

        return general_df

    def _generate_specific_dataframes(self):
        most_expensive_data = {
            'Category': self.dp.most_expensive_product_per_category()['Category'],
            'Most expensive product': self.dp.most_expensive_product_per_category()['Name'],
            'Price': self.dp.most_expensive_product_per_category()['Price']
        }
        most_expensive_products = pd.DataFrame(most_expensive_data)

        return most_expensive_products




