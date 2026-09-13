import os
import json
from datetime import datetime
from typing import Dict, Any, List, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..services.prediction_service import prediction_service

router = APIRouter(prefix="/api/assessment", tags=["Assessment"])

DATA_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "data", "assessments.json")

class AssessmentInput(BaseModel):
    mood_rating: int = Field(1, ge=1, le=5, description="1=Positive, 5=Severely Depressed")
    stress_level: int = Field(1, ge=1, le=5, description="1=Very Low, 5=Extreme Stress")
    sleep_quality: int = Field(1, ge=1, le=5, description="1=Excellent, 5=Severe Insomnia")
    concentration_difficulty: int = Field(1, ge=1, le=5, description="1=None, 5=Severe Inability to Focus")
    academic_work_pressure: int = Field(1, ge=1, le=5, description="1=Minimal, 5=Overwhelming")
    social_withdrawal: int = Field(1, ge=1, le=5, description="1=Connected, 5=Completely Isolated")
    energy_level: int = Field(1, ge=1, le=5, description="1=High Vitality, 5=Severe Fatigue")
    anxiety_frequency: int = Field(1, ge=1, le=5, description="1=Rarely, 5=Constant Panic")
    daily_functioning_impact: int = Field(1, ge=1, le=5, description="1=No Impact, 5=Cannot Perform Routine Tasks")

def _load_history() -> List[Dict[str, Any]]:
    if not os.path.exists(DATA_FILE):
        return []
    try:
        with open(DATA_FILE, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception:
        return []

def _save_history(record: Dict[str, Any]):
    os.makedirs(os.path.dirname(DATA_FILE), exist_ok=True)
    history = _load_history()
    history.insert(0, record)
    # Keep last 50 assessments
    history = history[:50]
    try:
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(history, f, indent=2, ensure_ascii=False)
    except Exception as e:
        print(f"[AssessmentRoute] Warning saving history: {e}")

@router.post("/predict")
def predict_assessment(data: AssessmentInput):
    try:
        input_dict = data.model_dump()
        result = prediction_service.predict(input_dict)
        
        # Save record for dashboard tracking
        record = {
            "id": f"rec_{datetime.now().strftime('%Y%m%d_%H%M%S')}",
            "timestamp": datetime.now().isoformat(),
            "dateFormatted": datetime.now().strftime("%b %d, %Y, %I:%M %p"),
            "score": result["score"],
            "rawScore": result["rawScore"],
            "riskCategory": result["riskCategory"],
            "contributingFactors": result["contributingFactors"][:3],
            "inputs": input_dict
        }
        _save_history(record)
        
        return {
            "success": True,
            "data": result,
            "recordId": record["id"],
            "timestamp": record["timestamp"]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Prediction evaluation failed: {str(e)}")

@router.get("/history")
def get_assessment_history():
    history = _load_history()
    return {
        "success": True,
        "total": len(history),
        "history": history
    }
