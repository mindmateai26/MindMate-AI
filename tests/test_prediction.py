import sys
import os

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8")

# Add backend directory to sys.path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from backend.services.prediction_service import prediction_service

def test_model_loading():
    assert prediction_service.model is not None, "Model failed to load."
    print("[PASS] Model successfully loaded.")

def test_low_risk_prediction():
    low_input = {
        "mood_rating": 1,
        "stress_level": 1,
        "sleep_quality": 1,
        "concentration_difficulty": 1,
        "academic_work_pressure": 1,
        "social_withdrawal": 1,
        "energy_level": 1,
        "anxiety_frequency": 1,
        "daily_functioning_impact": 1
    }
    res = prediction_service.predict(low_input)
    assert res["riskCategory"] == "Low", f"Expected Low, got {res['riskCategory']}"
    assert res["score"] == 0.0, f"Expected 0.0 score, got {res['score']}"
    assert len(res["suggestions"]) > 0, "Expected suggestions list."
    assert "preliminary wellness screening" in res["disclaimer"].lower()
    print("[PASS] Low risk prediction validated.")

def test_high_risk_prediction():
    high_input = {
        "mood_rating": 5,
        "stress_level": 5,
        "sleep_quality": 5,
        "concentration_difficulty": 5,
        "academic_work_pressure": 5,
        "social_withdrawal": 5,
        "energy_level": 5,
        "anxiety_frequency": 5,
        "daily_functioning_impact": 5
    }
    res = prediction_service.predict(high_input)
    assert res["riskCategory"] == "High", f"Expected High, got {res['riskCategory']}"
    assert res["score"] == 100.0, f"Expected 100.0 score, got {res['score']}"
    assert len(res["contributingFactors"]) == 9
    print("[PASS] High risk prediction validated.")

def test_moderate_factors():
    moderate_input = {
        "mood_rating": 3,
        "stress_level": 4,
        "sleep_quality": 4,
        "concentration_difficulty": 3,
        "academic_work_pressure": 5,
        "social_withdrawal": 2,
        "energy_level": 3,
        "anxiety_frequency": 4,
        "daily_functioning_impact": 3
    }
    res = prediction_service.predict(moderate_input)
    assert res["riskCategory"] in ["Moderate", "Mild", "High"]
    # Check that highest ratings appear at top of contributing factors
    top_factor = res["contributingFactors"][0]
    assert top_factor["rating"] >= 4
    print("[PASS] Contributing factors ranking validated.")

if __name__ == "__main__":
    test_model_loading()
    test_low_risk_prediction()
    test_high_risk_prediction()
    test_moderate_factors()
    print("\nAll ML prediction tests PASSED!")
