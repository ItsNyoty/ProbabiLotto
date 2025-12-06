from fastapi import FastAPI, HTTPException
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import uvicorn
from data_loader import load_data, GAME_CONFIG
from predictor import LotteryPredictor

app = FastAPI(title="Lottery AI API")

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cache predictors
predictors = {}

def get_predictor(game_type: str):
    if game_type not in predictors:
        try:
            df = load_data(game_type)
            predictors[game_type] = LotteryPredictor(df, game_type)
            print(f"Initialized predictor for {game_type}")
        except Exception as e:
            print(f"Failed to initialize {game_type}: {e}")
            return None
    return predictors.get(game_type)

class PredictionResponse(BaseModel):
    algorithm: str
    numbers: List[int]
    special_numbers: List[int]
    special_label: str
    constellation: Optional[str] = None
    explanation: str

@app.get("/api/predict/{game}/{algorithm}", response_model=PredictionResponse)
async def get_prediction(game: str, algorithm: str):
    if game not in GAME_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid game type")
        
    predictor = get_predictor(game)
    if predictor is None:
        raise HTTPException(status_code=500, detail=f"Could not load data for {game}")
    
    if algorithm not in ["hot", "cold", "hybrid"]:
        raise HTTPException(status_code=400, detail="Invalid algorithm. Choose 'hot', 'cold', or 'hybrid'.")
    
    try:
        result = predictor.generate_prediction(algorithm)
        return {
            "algorithm": algorithm,
            "numbers": result['numbers'],
            "special_numbers": result['special_numbers'],
            "special_label": result['special_label'],
            "constellation": result.get('constellation'),
            "explanation": result['explanation']
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/stats/{game}")
async def get_stats(game: str):
    if game not in GAME_CONFIG:
        raise HTTPException(status_code=400, detail="Invalid game type")

    predictor = get_predictor(game)
    if predictor is None:
        raise HTTPException(status_code=500, detail=f"Could not load data for {game}")
    
    freq = predictor.get_frequency_stats(predictor.all_main)
    # Convert keys/values to int for JSON serialization
    freq = {int(k): int(v) for k, v in freq.items()}
    
    return {"frequency": freq}

@app.get("/api/games")
async def get_games():
    return list(GAME_CONFIG.keys())

# Serve static files (Frontend)
app.mount("/", StaticFiles(directory="static", html=True), name="static")

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
