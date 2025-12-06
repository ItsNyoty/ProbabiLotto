import pandas as pd

files = {
    'jokerplus': 'statistieken-joker-plus-10-25.xlsx',
    'vikinglotto': 'statistieken-vikinglotto-10-25.xlsx'
}

for name, f in files.items():
    print(f"\n--- Probing {name} ({f}) ---")
    try:
        # Read without header
        df = pd.read_excel(f, header=None, nrows=10)
        
        for i in range(10):
            row = df.iloc[i].tolist()
            # Clean row
            row = [str(x).strip() for x in row if pd.notna(x)]
            print(f"Row {i}: {row}")
            
    except Exception as e:
        print(f"Error: {e}")
