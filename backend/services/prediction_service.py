import os
import joblib
import pandas as pd
from typing import Dict, Any, List

FEATURE_LABELS = {
    "mood_rating": "Mood & Emotional Balance",
    "stress_level": "Stress Level",
    "sleep_quality": "Sleep Quality & Restfulness",
    "concentration_difficulty": "Focus & Concentration",
    "academic_work_pressure": "Academic & Work Pressure",
    "social_withdrawal": "Social Connectedness",
    "energy_level": "Vitality & Energy Levels",
    "anxiety_frequency": "Anxiety & Nervous Tension",
    "daily_functioning_impact": "Daily Functioning & Routine"
}

SUGGESTIONS = {
    "Low": [
        "Continue maintaining your healthy daily sleep and study balance.",
        "Practice mindful reflection or journaling a few times each week.",
        "Stay socially connected with supportive peers and mentors."
    ],
    "Mild": [
        "Incorporate 10-15 minute structured relaxation or deep-breathing intervals daily.",
        "Break large academic or work tasks into smaller, time-boxed milestones.",
        "Aim for consistent sleep schedules and limit late-night screen time.",
        "Chat with our MindMate AI companion whenever you feel tension building."
    ],
    "Moderate": [
        "Consider discussing your workload and stress with a college counselor or mentor.",
        "Establish firm boundaries between study hours and personal rest time.",
        "Engage in gentle physical movement, hydration, and progressive muscle relaxation.",
        "Keep open communication with family or close friends about how you are feeling."
    ],
    "High": [
        "We strongly encourage connecting with a qualified mental health professional or counselor.",
        "Reach out immediately to someone you trust—you do not have to navigate this alone.",
        "Utilize free, confidential student helpline resources available on our Crisis Support page.",
        "Focus on fundamental self-care: adequate rest, nutrition, and reducing acute pressure."
    ]
}

class PredictionService:
    def __init__(self):
        self.model_data = None
        self.model = None
        self.feature_names = list(FEATURE_LABELS.keys())
        self._load_model()

    def _load_model(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        model_path = os.path.join(current_dir, "..", "models", "prediction_model.joblib")
        if os.path.exists(model_path):
            try:
                self.model_data = joblib.load(model_path)
                self.model = self.model_data.get("model")
                if "feature_names" in self.model_data:
                    self.feature_names = self.model_data["feature_names"]
                print(f"[PredictionService] Successfully loaded model from {model_path}")
            except Exception as e:
                print(f"[PredictionService] Warning: Could not load model: {e}")
        else:
            print(f"[PredictionService] Warning: Model file not found at {model_path}")

    def predict(self, responses: Dict[str, int]) -> Dict[str, Any]:
        """
        Takes dictionary with 9 ratings (1 to 5).
        Returns risk category, scores, top contributing factors, and suggestions.
        """
        # Ensure all features exist and are integers 1-5
        clean_features = {}
        for feature in self.feature_names:
            val = responses.get(feature, 1)
            try:
                val = int(val)
            except (ValueError, TypeError):
                val = 1
            clean_features[feature] = max(1, min(5, val))

        # Calculate composite score (Min: 9, Max: 45) -> Normalize to 0-100%
        raw_sum = sum(clean_features.values())
        normalized_score = round(((raw_sum - 9) / (45 - 9)) * 100, 1)

        # ML model prediction
        predicted_category = "Low"
        probabilities: Dict[str, float] = {}

        if self.model is not None:
            try:
                df_input = pd.DataFrame([clean_features])[self.feature_names]
                pred = self.model.predict(df_input)[0]
                predicted_category = str(pred)
                
                if hasattr(self.model, "predict_proba"):
                    probs = self.model.predict_proba(df_input)[0]
                    classes = self.model.classes_
                    for cls, prob in zip(classes, probs):
                        probabilities[str(cls)] = round(float(prob) * 100, 1)
            except Exception as err:
                print(f"[PredictionService] Fallback to heuristic calculation: {err}")
                predicted_category = self._heuristic_category(normalized_score)
        else:
            predicted_category = self._heuristic_category(normalized_score)

        # Identify contributing factors (highest rating relative to scale)
        # Factor contribution score = rating * feature_importance
        importances = (
            self.model_data.get("feature_importances", {})
            if self.model_data else {}
        )
        contributing_factors: List[Dict[str, Any]] = []
        for feat, score in clean_features.items():
            imp = importances.get(feat, 0.1)
            severity_weight = (score / 5.0) * imp * 100
            contributing_factors.append({
                "feature": feat,
                "label": FEATURE_LABELS.get(feat, feat),
                "rating": score,
                "severity_score": round(severity_weight, 2),
                "status": "High Impact" if score >= 4 else ("Moderate Impact" if score == 3 else "Low Impact")
            })

        # Sort by rating and severity
        contributing_factors.sort(key=lambda x: (x["rating"], x["severity_score"]), reverse=True)

        suggestions = SUGGESTIONS.get(predicted_category, SUGGESTIONS["Low"])

        return {
            "score": normalized_score,
            "rawScore": raw_sum,
            "riskCategory": predicted_category,
            "probabilities": probabilities,
            "contributingFactors": contributing_factors,
            "suggestions": suggestions,
            "disclaimer": "This is a preliminary wellness screening and not a medical diagnosis."
        }

    def _heuristic_category(self, normalized_score: float) -> str:
        if normalized_score <= 25.0:
            return "Low"
        elif normalized_score <= 50.0:
            return "Mild"
        elif normalized_score <= 75.0:
            return "Moderate"
        else:
            return "High"

prediction_service = PredictionService()
