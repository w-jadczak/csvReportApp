import pandas as pd

class DataframeLoader:
    def __init__(self, path):
        self.path = path

    def load_data(self):
        return pd.read_csv(self.path)

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

        general_data = {
            'Data' : ['Total products', 'Average price', 'Total stock value'],
            'Value' : [self.dp.total_products(), self.dp.average_price(), self.dp.total_value()]
        }

        general_df = pd.DataFrame(general_data)
        most_expensive_products = self.dp.most_expensive_product_per_category()

        with open(output_csv_file_path, mode='w', newline='') as file:
            general_df.to_csv(file, index=False)
            file.write('\n')
            file.write('Category, Most expensive product, Price\n')
            most_expensive_products.to_csv(file, index=False, header=False)


