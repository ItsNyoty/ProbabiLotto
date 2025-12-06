import pandas as pd
import os

GAME_CONFIG = {
    'lotto': {
        'file': 'statistieken-lotto-10-25.xlsx',
        'sheet': 'Resultaten',
        'header_row': 8,
        'cols': {'Datum': 'Date', '1': 'B1', '2': 'B2', '3': 'B3', '4': 'B4', '5': 'B5', '6': 'B6', 'Bonus': 'Bonus'},
        'range': (1, 45),
        'count': 6
    },
    'euromillions': {
        'file': 'statistieken-euromillions-10-25.xlsx',
        'sheet': 'Resultaten', # Assumed based on pattern
        'header_row': 0, # Need to verify, usually 0 or similar to Lotto
        'cols': {'Datum': 'Date', '1': 'B1', '2': 'B2', '3': 'B3', '4': 'B4', '5': 'B5', 'S1': 'S1', 'S2': 'S2'},
        'range': (1, 50),
        'stars_range': (1, 12),
        'count': 5,
        'stars_count': 2
    },
    'keno': {
        'file': 'statistieken-keno-10-25.xlsx',
        'sheet': 'Resultaten',
        'header_row': 0,
        'cols': {'Datum': 'Date'}, # Keno has 20 numbers, need dynamic handling
        'range': (1, 70),
        'count': 20
    },
    'vikinglotto': {
        'file': 'statistieken-vikinglotto-10-25.xlsx',
        'sheet': 'Resultaten',
        'header_row': 8,
        'cols': {'Datum': 'Date', '1': 'B1', '2': 'B2', '3': 'B3', '4': 'B4', '5': 'B5', '6': 'B6', 'Viking': 'Viking'},
        'range': (1, 48),
        'viking_range': (1, 5),
        'count': 6,
        'viking_count': 1
    },
    'extralotto': {
        'file': 'statistieken-extra-lotto-10-25.xlsx',
        'sheet': 'Resultaten',
        'header_row': 0,
        'cols': {'Datum': 'Date', '1': 'B1', '2': 'B2', '3': 'B3', '4': 'B4', '5': 'B5', '6': 'B6', 'Bonus': 'Bonus'},
        'range': (1, 45),
        'count': 6
    },
    'jokerplus': {
        'file': 'statistieken-joker-plus-10-25.xlsx',
        'sheet': 'Resultaten',
        'header_row': 0, # Will be detected
        'cols': {'Datum': 'Date', 'Constellatie': 'Constellation', 'Nummers': 'Numbers'},
        'range': (0, 9),
        'count': 6,
        'has_constellation': True
    },
    'pick3': {
        'file': 'statistieken-pick3-10-25.xlsx',
        'sheet': 'Resultaten',
        'header_row': 0,
        'cols': {'Datum': 'Date', '1': 'B1', '2': 'B2', '3': 'B3'},
        'range': (0, 9),
        'count': 3
    }
}

def load_data(game_type='lotto'):
    """
    Loads data for a specific game type.
    """
    if game_type not in GAME_CONFIG:
        raise ValueError(f"Unknown game type: {game_type}")
    
    config = GAME_CONFIG[game_type]
    file_path = config['file']
    
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Data file not found at {file_path}")

    # Read the file
    try:
        df = pd.read_excel(file_path, sheet_name=config.get('sheet', 0), header=None)
    except Exception as e:
        # Try first sheet if specific sheet fails
        df = pd.read_excel(file_path, header=None)

    # Find header row containing 'Datum' or 'Date'
    header_idx = -1
    # Read a chunk to find header
    temp_df = pd.read_excel(file_path, sheet_name=config.get('sheet', 0), header=None, nrows=20)
    
    for i, row in temp_df.iterrows():
        row_str = [str(x).lower() for x in row if pd.notna(x)]
        # Check for 'datum' or 'date'
        if any('datum' in str(x).lower() for x in row if pd.notna(x)) or \
           any('date' in str(x).lower() for x in row if pd.notna(x)):
            header_idx = i
            break
            
    if header_idx == -1:
        # Fallback: For Joker+ or Pick3, sometimes header is row 0 but 'Datum' might be named differently or missing?
        # Let's check specific games
        if game_type == 'jokerplus':
             # Joker+ might have 'Trekking' or something
             header_idx = 0
        elif game_type == 'pick3':
             header_idx = 0
        else:
             print(f"Warning: Could not find 'Datum' header in {game_type}. Using row 0.")
             header_idx = 0
        
    # Reload with correct header
    df = pd.read_excel(file_path, sheet_name=config.get('sheet', 0), header=header_idx)
    
    # print(f"DEBUG [{game_type}] Raw Columns: {df.columns.tolist()}")

    # Clean column names
    df.columns = [str(c).strip() for c in df.columns]
    
    # Rename columns
    # Find column that looks like a date
    date_col = None
    for col in df.columns:
        if 'datum' in col.lower() or 'date' in col.lower():
            date_col = col
            break
            
    if date_col:
        df = df.rename(columns={date_col: 'Date'})
        df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
        df = df.dropna(subset=['Date'])
        df = df.sort_values('Date')
    
    # Map numbers
    # Standardize to B1, B2... and S1, S2...
    # Helper to find column by list of possible names
    new_cols = {}
    def find_col(candidates):
        for col in df.columns:
            clean_col = str(col).strip()
            # Handle float headers (e.g. 1.0 -> 1)
            if clean_col.endswith('.0'):
                clean_col = clean_col[:-2]
            # Check exact match
            if clean_col in candidates:
                return col
            # Check N° prefix
            for cand in candidates:
                if clean_col == f"N°{cand}" or clean_col == f"N° {cand}":
                    return col
                if clean_col == cand:
                    return col
        return None

    if game_type == 'lotto' or game_type == 'extralotto':
        # 1-6, Bonus
        for i in range(1, 7):
            c = find_col([str(i)])
            if c: new_cols[c] = f'B{i}'
        c = find_col(['Bonus', 'Reserve', 'Res', 'Bonusnr.', 'Bonusnr'])
        if c: new_cols[c] = 'Bonus'
        
    elif game_type == 'euromillions':
        # 1-5, S1-S2
        for i in range(1, 6):
            c = find_col([str(i)])
            if c: new_cols[c] = f'B{i}'
        for i in range(1, 3):
            c = find_col([f'S{i}', f'Ster{i}', f'Star {i}'])
            if c: new_cols[c] = f'S{i}'

    elif game_type == 'vikinglotto':
        # 1-6, Viking
        for i in range(1, 7):
            c = find_col([str(i)])
            if c: new_cols[c] = f'B{i}'
        c = find_col(['Viking', 'Vikingnummer'])
        if c: new_cols[c] = 'Viking'
        
    elif game_type == 'keno':
        # 1-20
        for i in range(1, 21):
            c = find_col([str(i)])
            if c: new_cols[c] = f'B{i}'

    elif game_type == 'pick3':
        # Pick3 has 'Combinatie' column
        c = find_col(['Combinatie', 'Combination'])
        if c: new_cols[c] = 'Numbers'

    elif game_type == 'jokerplus':
        # Joker+ has 'Nummers' column
        num_col = find_col(['Nummers', 'Numbers', 'Getallen'])
        if num_col: new_cols[num_col] = 'Numbers'
        c = find_col(['Constellatie', 'Constellation', 'Dierenriem', 'Sterrenbeeld'])
        if c: new_cols[c] = 'Constellation'

    df = df.rename(columns=new_cols)
    
    # Special handling for Joker+ splitting
    if game_type == 'jokerplus' and 'Numbers' in df.columns:
        df['Numbers'] = df['Numbers'].astype(str).str.strip().apply(lambda x: x.zfill(6) if x.isdigit() else x)
        for i in range(6):
            df[f'B{i+1}'] = df['Numbers'].apply(lambda x: int(x[i]) if len(x) >= 6 and x[i].isdigit() else 0)

    # Special handling for Pick3 splitting
    if game_type == 'pick3' and 'Numbers' in df.columns:
        # Pad with zeros to ensure 3 digits (e.g. 65 -> 065)
        df['Numbers'] = df['Numbers'].astype(str).str.strip().apply(lambda x: x.zfill(3) if x.isdigit() else x)
        for i in range(3):
            df[f'B{i+1}'] = df['Numbers'].apply(lambda x: int(x[i]) if len(x) >= 3 and x[i].isdigit() else 0)
            
    # Keep only mapped columns + Date
    cols_to_keep = ['Date'] + list(new_cols.values())
    if game_type == 'jokerplus':
        cols_to_keep.extend([f'B{i+1}' for i in range(6)])
    if game_type == 'pick3':
        cols_to_keep.extend([f'B{i+1}' for i in range(3)])
        
    # Filter to only existing columns
    cols_to_keep = [c for c in cols_to_keep if c in df.columns]
    df = df[cols_to_keep]
    
    # Ensure numbers are ints, but skip non-numeric columns like Constellation
    for c in df.columns:
        if c != 'Date' and c != 'Constellation' and c != 'Numbers':
            df[c] = pd.to_numeric(df[c], errors='coerce').fillna(0).astype(int)

    # Filter data based on game rules history
    if game_type == 'lotto':
        # Lotto changed to 45 numbers on 2011-10-01. Prior to that it was 42.
        # To ensure accurate stats for 43-45, we filter from this date.
        df = df[df['Date'] >= '2011-10-01']
        
    elif game_type == 'keno':
        # Keno changed from 80 to 70 numbers in 2008.
        # Filter to include only the 70-number game era.
        df = df[df['Date'] >= '2008-01-01']

    return df

if __name__ == "__main__":
    # Test loading different games
    for game in ['lotto', 'euromillions', 'vikinglotto', 'keno']:
        print(f"\n--- Loading {game} ---")
        try:
            df = load_data(game)
            print(df.head().to_string())
            print("Columns:", df.columns.tolist())
        except Exception as e:
            print(f"Failed: {e}")
