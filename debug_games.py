import pandas as pd
from data_loader import load_data, GAME_CONFIG
from predictor import LotteryPredictor

import sys

# Redirect stdout to file
sys.stdout = open('debug_log.txt', 'w')

print("Available games in config:", list(GAME_CONFIG.keys()))

def test_game(game):
    print(f"\n--- Loading {game} ---")
    try:
        df = load_data(game)
        print(df.head().to_string())
        print("Columns:", df.columns.tolist())
        
        # Test prediction
        predictor = LotteryPredictor(df, game)
        print(f"Testing {game} Hybrid Prediction...")
        pred = predictor.generate_prediction('hybrid')
        print("Prediction:", pred)
        return True
    except Exception as e:
        print(f"Failed {game}: {e}")
        import traceback
        traceback.print_exc()
        return False

# Test specific games
games_to_test = ['pick3']
for game in games_to_test:
    test_game(game)

sys.stdout.close()
