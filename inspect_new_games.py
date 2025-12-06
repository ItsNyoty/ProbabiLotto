import pandas as pd
import os

files = [
    'statistieken-extra-lotto-10-25.xlsx',
    'statistieken-joker-plus-10-25.xlsx',
    'statistieken-pick3-10-25.xlsx'
]

for file_path in files:
    print(f"\n\n=== Inspecting {file_path} ===")
    try:
        if not os.path.exists(file_path):
            print("File not found.")
            continue
            
        # Read first few rows to find header
        df_head = pd.read_excel(file_path, header=None, nrows=20)
        print("First 20 rows raw:")
        print(df_head.to_string())
        
    except Exception as e:
        print(f"Error: {e}")
