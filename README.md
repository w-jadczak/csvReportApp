# CSV Reports Application

## Description
Simple CSV Reports Application is designed to generate reports from CSV data. 

## Features
- **Data Loading:** Load CSV data from a specified file path. The CSV file should have following format:
  ~~~
  | ID | Name | Category | Price | Quantity |
  |----|------|----------|-------|----------|
  |    |      |          |       |          |
  |    |      |          |       |          |
    ~~~
- **Data Processing:** Analyze loaded data, calculate statistics.
- **Report Generation:** Create CSV reports in format:
  ~~~
    | Data              | Value   |
    |-------------------|---------|
    | Total products    |         |
    | Average price     |         |
    | Total stock value |         |
    |-------------------|---------|-------------------|
    |Most Expensive Products by Category:             |
    |----------------|------------------------|-------|
    | Category       | Most expensive product | Price |
    |----------------|------------------------|-------|
    |                |                        |       |
    |                |                        |       |
    |                |                        |       |
~~~

## Usage
### Running the Application
To run the CSV Reports Application, follow these steps:
1. Clone the repository to your local machine.
2. Navigate to the project directory.
3. Execute the `run_csv_analysis.py` script to start the application.

### Running Tests
To run the tests for the CSV Reports Application, follow these steps:
1. Navigate to the project directory.
2. Execute the `tests.py` script to run all the unit tests.

## Dependencies
- pandas: Used for data manipulation and analysis.
- unittest: Used for running unit tests.

## License
This project is licensed under the [License Name] License - see the [LICENSE](LICENSE) file for details.
