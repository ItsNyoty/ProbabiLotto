import pandas as pd
import os

files = [
    'statistieken-joker-plus-10-25.xlsx',
    'statistieken-vikinglotto-10-25.xlsx',
    'statistieken-lotto-10-25.xlsx'
]

import sys
# Force UTF-8 for file output
sys.stdout = open('inspect_keno.txt', 'w', encoding='utf-8')

f = 'statistieken-keno-10-25.xlsx'
print(f"\n--- Inspecting {f} ---")
if os.path.exists(f):
    try:
        # Header is at row 3 (index 3) based on previous inspection
        df = pd.read_excel(f, sheet_name='Resultaten', header=3)
        print("Columns:", df.columns.tolist())
        print("Last 20 rows:")
        print(df.tail(20).to_string())
    except Exception as e:
        print(f"Error reading {f}: {e}")
else:
    print(f"File not found: {f}")

sys.stdout.close()
