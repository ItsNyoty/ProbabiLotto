import pandas as pd
import os

files = [
    'statistieken-euromillions-10-25.xlsx',
    'statistieken-keno-10-25.xlsx',
    'statistieken-joker-plus-10-25.xlsx'
]

for file_path in files:
    print(f"\n\n=== Inspecting {file_path} ===")
    try:
        if not os.path.exists(file_path):
            print("File not found.")
            continue
            
        xls = pd.ExcelFile(file_path)
        print("Sheet names:", xls.sheet_names)
        
        # Try to read 'Resultaten' if it exists, otherwise first sheet
        sheet_to_read = 'Resultaten' if 'Resultaten' in xls.sheet_names else xls.sheet_names[0]
        
        df = pd.read_excel(file_path, sheet_name=sheet_to_read, header=None)
        print(f"First 15 rows of {sheet_to_read}:")
        print(df.head(15).to_string())
        
    except Exception as e:
        print(f"Error: {e}")
