from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..services.emotion_detector import detect_emotion
from ..services.language_detector import detect_language

router = APIRouter(prefix="/api/emotion", tags=["Emotion & Language"])

class EmotionRequest(BaseModel):
    text: str = Field(..., min_length=1, description="Text to analyze for emotional tone")
    language: str = Field("auto", description="Optional language override")

class EmotionResponse(BaseModel):
    emotion: str
    moodTag: str
    language: str
    isEmergency: bool

@router.post("", response_model=EmotionResponse)
def analyze_emotion(payload: EmotionRequest):
    try:
        text = payload.text.strip()
        emotion_data = detect_emotion(text)
        detected_lang = detect_language(text, payload.language)

        return EmotionResponse(
            emotion=emotion_data["emotion"],
            moodTag=emotion_data["moodTag"],
            language=detected_lang,
            isEmergency=emotion_data["isEmergency"]
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Emotion analysis failed: {str(e)}")
