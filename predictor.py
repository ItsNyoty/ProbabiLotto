import pandas as pd
from collections import Counter
import random
from data_loader import GAME_CONFIG

class LotteryPredictor:
    def __init__(self, df, game_type):
        """
        Initialize with the lottery data DataFrame and game type.
        """
        self.df = df
        self.game_type = game_type
        self.config = GAME_CONFIG[game_type]
        
        # Identify number columns
        self.main_cols = [c for c in df.columns if c.startswith('B')]
        self.star_cols = [c for c in df.columns if c.startswith('S')]
        self.viking_cols = [c for c in df.columns if c.startswith('Viking')]
        
        # Flatten all drawn numbers
        self.all_main = df[self.main_cols].values.flatten()
        
        # Filter out 0s unless it's Pick3 where 0 is valid
        if self.game_type == 'pick3':
            self.all_main = self.all_main[self.all_main >= 0]
        else:
            self.all_main = self.all_main[self.all_main > 0]
        
        import numpy as np
        self.all_stars = df[self.star_cols].values.flatten() if self.star_cols else np.array([])
        if len(self.all_stars) > 0:
            self.all_stars = self.all_stars[self.all_stars > 0]

    def get_frequency_stats(self, numbers):
        """Returns a dictionary of number frequencies."""
        return dict(Counter(numbers))

    def get_overdue_numbers(self, cols, max_val, top_n=10):
        """
        Identifies numbers that haven't been drawn for the longest time.
        """
        last_seen = {}
        # Iterate backwards
        for idx, row in self.df.sort_values('Date', ascending=False).iterrows():
            draw_nums = [row[c] for c in cols]
            for num in draw_nums:
                if num not in last_seen:
                    last_seen[num] = row['Date']
            
            # Stop if we found all numbers
            if len(last_seen) >= max_val:
                break
        
        # Calculate days since last seen
        current_date = pd.Timestamp.now()
        overdue = []
        for num in range(1, max_val + 1):
            if num in last_seen:
                days_since = (current_date - last_seen[num]).days
                overdue.append({'number': num, 'days_overdue': days_since})
            else:
                overdue.append({'number': num, 'days_overdue': 99999})
        
        overdue.sort(key=lambda x: x['days_overdue'], reverse=True)
        return overdue[:top_n]

    def predict_hot_numbers(self, n, source_nums):
        """Predicts based on most frequent numbers, with some randomness."""
        freq = self.get_frequency_stats(source_nums)
        sorted_nums = sorted(freq.items(), key=lambda x: x[1], reverse=True)
        
        # Take top n * 2 (or at least n + 5) to sample from
        pool_size = max(n * 2, n + 5)
        top_candidates = [num for num, count in sorted_nums[:pool_size]]
        
        # Sample n from the top candidates
        if len(top_candidates) >= n:
            return random.sample(top_candidates, n)
        return top_candidates

    def predict_cold_numbers(self, n, cols, max_val):
        """Predicts based on overdue numbers, with some randomness."""
        overdue = self.get_overdue_numbers(cols, max_val, top_n=max(n * 2, n + 5))
        candidates = [item['number'] for item in overdue]
        
        if len(candidates) >= n:
            return random.sample(candidates, n)
        return candidates

    def predict_hybrid(self, n, source_nums, cols, max_val):
        """
        Combines hot and cold numbers.
        Strategy: Half hot, half cold.
        """
        n_hot = n // 2
        n_cold = n - n_hot
        
        hot = self.predict_hot_numbers(n_hot, source_nums)
        cold = self.predict_cold_numbers(n_cold, cols, max_val)
        
        prediction = list(set(hot + cold))
        
        while len(prediction) < n:
            new_num = random.randint(1, max_val)
            if new_num not in prediction:
                prediction.append(new_num)
                
        # Shuffle instead of sort
        random.shuffle(prediction)
        return prediction[:n]

    def generate_prediction(self, algorithm):
        """
        Generates a full prediction including main numbers and special numbers (stars, viking).
        Returns a dict with 'numbers', 'special_numbers', and 'explanation'.
        """
        main_count = self.config['count']
        main_range = self.config['range'][1]
        
        special_numbers = []
        special_label = ""
        constellation_name = None
        
        # Main numbers
        if algorithm == "hot":
            main_pred = self.predict_hot_numbers(main_count, self.all_main)
            explanation = "Based on the most frequently drawn numbers historically."
        elif algorithm == "cold":
            main_pred = self.predict_cold_numbers(main_count, self.main_cols, main_range)
            explanation = "Based on numbers that haven't been drawn for the longest time (overdue)."
        else: # hybrid
            main_pred = self.predict_hybrid(main_count, self.all_main, self.main_cols, main_range)
            explanation = "A balanced mix of frequently drawn numbers and overdue numbers."
            
        # Shuffle main numbers (user request)
        random.shuffle(main_pred)

        # Special numbers (Stars, Viking, Constellation, Bonus)
        if self.game_type in ['lotto', 'extralotto']:
            # Handle Bonus number
            # Bonus is in 'Bonus' column
            bonus_col = 'Bonus'
            if bonus_col in self.df.columns:
                bonus_nums = self.df[bonus_col].values.flatten()
                bonus_nums = bonus_nums[bonus_nums > 0]
                
                if algorithm == "hot":
                    special_numbers = self.predict_hot_numbers(1, bonus_nums)
                elif algorithm == "cold":
                    # Bonus range is same as main range usually (1-45)
                    special_numbers = self.predict_cold_numbers(1, [bonus_col], main_range)
                else:
                    special_numbers = self.predict_hybrid(1, bonus_nums, [bonus_col], main_range)
                special_label = "Bonus"

        elif self.game_type == 'euromillions':
            stars_count = self.config['stars_count']
            stars_range = self.config['stars_range'][1]
            special_label = "Stars"
            if algorithm == "hot":
                special_numbers = self.predict_hot_numbers(stars_count, self.all_stars)
            elif algorithm == "cold":
                special_numbers = self.predict_cold_numbers(stars_count, self.star_cols, stars_range)
            else:
                special_numbers = self.predict_hybrid(stars_count, self.all_stars, self.star_cols, stars_range)
                
        elif self.game_type == 'vikinglotto':
            viking_range = self.config['viking_range'][1]
            viking_nums = self.df[self.viking_cols].values.flatten()
            viking_nums = viking_nums[viking_nums > 0]
            
            if algorithm == "hot":
                special_numbers = self.predict_hot_numbers(1, viking_nums)
            elif algorithm == "cold":
                special_numbers = self.predict_cold_numbers(1, self.viking_cols, viking_range)
            else:
                special_numbers = self.predict_hybrid(1, viking_nums, self.viking_cols, viking_range)
            special_label = "Viking"

        elif self.game_type == 'jokerplus':
            # Joker+ has a constellation
            constellation_name = None
            if 'Constellation' in self.df.columns:
                constellations = self.df['Constellation'].dropna().values
                freq = Counter(constellations)
                
                if algorithm == "hot":
                    best = freq.most_common(1)
                    pred_constellation = str(best[0][0]) if best else "Leo"
                elif algorithm == "cold":
                    least = freq.most_common()[:-2:-1]
                    pred_constellation = str(least[0][0]) if least else "Pisces"
                else:
                    top3 = [x[0] for x in freq.most_common(3)]
                    pred_constellation = str(random.choice(top3)) if top3 else "Gemini"
                
                # explanation += f" Predicted Constellation: {pred_constellation}." # Removed as per user request
                special_label = "Constellation"
                special_numbers = [] 
                constellation_name = pred_constellation
            else:
                special_label = "Constellation"
                special_numbers = []

        elif self.game_type == 'pick3':
            # Pick3: 3 numbers from 0-9. Allow duplicates.
            range_max = 9
            main_pred = []
            
            cols = ['B1', 'B2', 'B3']
            for col in cols:
                if col in self.df.columns:
                    col_nums = self.df[col].values.flatten()
                    col_nums = col_nums[col_nums >= 0] # 0 is valid in Pick3
                    
                    if algorithm == "hot":
                        p = self.predict_hot_numbers(1, col_nums)
                    elif algorithm == "cold":
                        p = self.predict_cold_numbers(1, [col], range_max)
                    else:
                        p = self.predict_hybrid(1, col_nums, [col], range_max)
                    
                    if p:
                        main_pred.append(p[0])
                    else:
                        main_pred.append(random.randint(0, 9))
                else:
                    # Fallback if column missing
                    main_pred.append(random.randint(0, 9))

        return {
            "numbers": [int(x) for x in main_pred],
            "special_numbers": [int(x) for x in special_numbers],
            "special_label": special_label,
            "constellation": constellation_name,
            "explanation": explanation
        }

if __name__ == "__main__":
    from data_loader import load_data
    
    for game in ['lotto', 'euromillions']:
        print(f"\n--- Prediction for {game} ---")
        df = load_data(game)
        predictor = LotteryPredictor(df, game)
        pred = predictor.generate_prediction('hybrid')
        print(pred)
