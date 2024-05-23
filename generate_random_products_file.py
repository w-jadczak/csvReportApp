import csv
import random
import string

def generate_random_name(length=10):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

def generate_random_category():
    categories = ['Electronics', 'Clothing', 'Books', 'Home & Garden', 'Toys', 'Sports']
    return random.choice(categories)

def generate_random_price():
    return round(random.uniform(10.0, 100.0), 2)

def generate_random_quantity():
    return random.randint(1, 100)

num_products = 10

output_file = 'products.csv'

headers = ['ID', 'Name', 'Category', 'Price', 'Quantity']

with open(output_file, mode='w', newline='') as file:
    writer = csv.writer(file)

    writer.writerow(headers)

    for i in range(1, num_products + 1):
        name = generate_random_name()
        category = generate_random_category()
        price = generate_random_price()
        quantity = generate_random_quantity()

        writer.writerow([i, name, category, price, quantity])

print(f'File {output_file} was generated succesfully.')
