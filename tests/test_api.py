import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

def test_health():
    res = client.get("/api/health")
    assert res.status_code == 200
    data = res.json()
    assert data["status"] == "healthy"
    print("[PASS] GET /api/health passed.")

def test_assessment_predict():
    payload = {
        "mood_rating": 4,
        "stress_level": 4,
        "sleep_quality": 3,
        "concentration_difficulty": 4,
        "academic_work_pressure": 5,
        "social_withdrawal": 3,
        "energy_level": 4,
        "anxiety_frequency": 4,
        "daily_functioning_impact": 3
    }
    res = client.post("/api/assessment/predict", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "riskCategory" in data["data"]
    assert "score" in data["data"]
    assert "contributingFactors" in data["data"]
    print("[PASS] POST /api/assessment/predict passed.")

def test_assessment_history():
    res = client.get("/api/assessment/history")
    assert res.status_code == 200
    data = res.json()
    assert data["success"] is True
    assert "history" in data
    print("[PASS] GET /api/assessment/history passed.")

def test_emotion_endpoint():
    # Test English
    res1 = client.post("/api/emotion", json={"text": "I am feeling so anxious about exams"})
    assert res1.status_code == 200
    assert res1.json()["emotion"] in ["Academic pressure", "Anxiety", "Stress"]

    # Test Thanglish
    res2 = client.post("/api/emotion", json={"text": "enaku romba stress ah iruku"})
    assert res2.status_code == 200
    assert res2.json()["language"] == "thanglish"

    # Test Emergency
    res3 = client.post("/api/emotion", json={"text": "I want to end my life"})
    assert res3.status_code == 200
    assert res3.json()["isEmergency"] is True
    print("[PASS] POST /api/emotion passed.")

def test_chat_endpoint():
    payload = {
        "message": "My name is Priya",
        "history": [],
        "language": "auto"
    }
    res = client.post("/api/chat", json=payload)
    assert res.status_code == 200
    data = res.json()
    assert "text" in data
    assert "moodTag" in data
    assert "followUps" in data
    print("[PASS] POST /api/chat passed.")

if __name__ == "__main__":
    test_health()
    test_assessment_predict()
    test_assessment_history()
    test_emotion_endpoint()
    test_chat_endpoint()
    print("\nAll API Endpoint Tests PASSED!")
