from service import DataProcessor, DataframeLoader, ReportGenerator
from validator import InputCsvValidator
import argparse
import sys
def main():

    parser = argparse.ArgumentParser(description='Process product data from CSV file and generate report.')
    parser.add_argument('path', type=str, help='Path to input CSV file.')
    args = parser.parse_args()

    validator = InputCsvValidator()
    loader = DataframeLoader(args.path)

    try:
        validator.validate_path(args.path)
        df = loader.load_data()
        validator.validate_data(df)
    except (FileNotFoundError, ValueError) as e:
        print(f"Validation error: {e}")
        sys.exit(1)

    dp = DataProcessor(df)
    report_generator = ReportGenerator(dp)
    report_generator.generate_report('report.csv')

if __name__ == "__main__":
    main()