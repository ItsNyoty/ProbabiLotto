import pandas as pd
import os

file_path = 'statistieken-lotto-10-25.xlsx'

try:
    if not os.path.exists(file_path):
        print(f"Error: {file_path} not found.")
    else:
        xls = pd.ExcelFile(file_path)
        print("Sheet names:", xls.sheet_names)
        for sheet in xls.sheet_names:
            print(f"\n--- Sheet: {sheet} ---")
            df = pd.read_excel(file_path, sheet_name=sheet, header=None)
            print(df.head(10).to_string())
        print("\nData Types:")
        print(df.dtypes)
except Exception as e:
    print(f"An error occurred: {e}")
