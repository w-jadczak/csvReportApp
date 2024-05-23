from AppScript import DataProcessor, DataframeLoader, ReportGenerator, InputCsvValidator

def main():
    validator = InputCsvValidator()
    loader = DataframeLoader('products.csv', validator)
    df = loader.load_data()

    dp = DataProcessor(df)

    report_generator = ReportGenerator(dp)
    report_generator.generate_report('report.csv')

if __name__ == "__main__":
    main()