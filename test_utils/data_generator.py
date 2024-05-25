import csv
import random
import string
import os

class TestCsvGenerator:

    OUTPUT_FILE_PATH = '../csv_reports_app/test_utils/test_products.csv'

    def __init__(self):
        pass

    def _generate_random_name(self, length=10):
        return ''.join(random.choices(string.ascii_uppercase, k=length))

    def _generate_random_category(self):
        categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Toys', 'Sports']
        return random.choice(categories)

    def _generate_random_price(self):
        return round(random.uniform(10.0, 100.0), 2)

    def _generate_random_quantity(self):
        return random.randint(1, 100)

    def generate_test_csv(self, num_products=10):

        headers = ['ID', 'Name', 'Category', 'Price', 'Quantity']

        with open(self.OUTPUT_FILE_PATH, mode='w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(headers)

            for i in range(1, num_products + 1):
                name = self._generate_random_name()
                category = self._generate_random_category()
                price = self._generate_random_price()
                quantity = self._generate_random_quantity()

                writer.writerow([i, name, category, price, quantity])

        print(f'File {self.OUTPUT_FILE_PATH} was generated successfully.')
        return os.path.abspath(self.OUTPUT_FILE_PATH)
