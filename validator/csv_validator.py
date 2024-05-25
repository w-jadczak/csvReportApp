import os
import pandas as pd

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