import pandas as pd

files = {
    'lotto': 'statistieken-lotto-10-25.xlsx'
}

for name, f in files.items():
    try:
        xl = pd.ExcelFile(f)
        print(f"\n--- {name} Sheets ---")
        print(xl.sheet_names)
    except Exception as e:
        print(f"Error reading {f}: {e}")
