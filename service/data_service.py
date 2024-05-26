import pandas as pd

class DataframeLoader:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        df = pd.read_csv(self.path)
        return df

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
            specific_df.to_csv(file, index=False, header=True)

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