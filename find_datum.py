import pandas as pd
import sys

sys.stdout = open('find_datum_log.txt', 'w')

f = 'statistieken-lotto-10-25.xlsx'
print(f"--- Searching for 'Datum' in {f} ---")

try:
    df = pd.read_excel(f, sheet_name='Resultaten', header=None, nrows=100)
    
    for i, row in df.iterrows():
        row_str = [str(x).lower() for x in row]
        if any('datum' in x for x in row_str) or any('date' in x for x in row_str):
            print(f"Found header at row {i}")
            print(f"Row content: {row.tolist()}")
            break
except Exception as e:
    print(f"Error: {e}")

sys.stdout.close()
