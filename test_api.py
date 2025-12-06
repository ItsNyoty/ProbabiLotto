from fastapi.testclient import TestClient
from main import app
import pytest

client = TestClient(app)

def test_read_main():
    response = client.get("/")
    assert response.status_code == 200
    assert "text/html" in response.headers["content-type"]

def test_get_games():
    response = client.get("/api/games")
    assert response.status_code == 200
    games = response.json()
    assert "lotto" in games
    assert "euromillions" in games

def test_get_stats_lotto():
    response = client.get("/api/stats/lotto")
    assert response.status_code == 200
    data = response.json()
    assert "frequency" in data
    assert len(data["frequency"]) > 0

def test_predict_lotto_hybrid():
    response = client.get("/api/predict/lotto/hybrid")
    assert response.status_code == 200
    data = response.json()
    assert data["algorithm"] == "hybrid"
    assert len(data["numbers"]) == 6
    assert "explanation" in data
    assert len(data["explanation"]) > 0

def test_predict_euromillions_hot():
    response = client.get("/api/predict/euromillions/hot")
    assert response.status_code == 200
    data = response.json()
    assert len(data["numbers"]) == 5
    assert len(data["special_numbers"]) == 2
    assert data["special_label"] == "Stars"

def test_invalid_game():
    response = client.get("/api/predict/invalid_game/hot")
    assert response.status_code == 400
