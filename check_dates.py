import sys
from data_loader import load_data, GAME_CONFIG

sys.stdout = open('dates_log.txt', 'w')

print("Checking data ranges...")
for game in GAME_CONFIG.keys():
    try:
        df = load_data(game)
        if 'Date' in df.columns:
            min_date = df['Date'].min()
            max_date = df['Date'].max()
            print(f"{game}: {min_date.date()} to {max_date.date()} (Total: {len(df)} draws)")
        else:
            print(f"{game}: No Date column found")
    except Exception as e:
        print(f"{game}: Error - {e}")

sys.stdout.close()
