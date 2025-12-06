import pandas as pd
import json

files = {
    'lotto': 'statistieken-lotto-10-25.xlsx'
}

results = {}

for name, f in files.items():
    try:
        df = pd.read_excel(f, sheet_name='2011-2025 45 nummers', header=None, nrows=5)
        rows = []
        for i in range(5):
            # Convert to string and strip, ignore NaNs
            row_data = [str(x).strip() for x in df.iloc[i] if pd.notna(x)]
            rows.append(row_data)
        results[name] = rows
    except Exception as e:
        results[name] = str(e)

print(json.dumps(results, indent=2))
