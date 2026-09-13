from typing import List, Dict, Any, Optional
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel, Field
from ..services.gemini_service import gemini_service

router = APIRouter(prefix="/api/chat", tags=["Chat"])

class ChatMessage(BaseModel):
    sender: str
    text: str

class ChatRequest(BaseModel):
    message: str = Field(..., min_length=1, description="The user's current message")
    history: Optional[List[Dict[str, Any]]] = Field(default_factory=list, description="Recent conversation turns")
    language: Optional[str] = Field("auto", description="Language preference: 'auto', 'en', 'ta', 'thanglish'")
    assessmentContext: Optional[Dict[str, Any]] = Field(None, description="Optional score & risk context from screening")
    apiKey: Optional[str] = Field(None, description="Optional user-provided Gemini API key")

class ChatResponse(BaseModel):
    text: str
    moodTag: str
    language: str
    source: str
    isEmergency: bool
    followUps: List[str]

@router.post("", response_model=ChatResponse)
def handle_chat(payload: ChatRequest):
    try:
        user_message = payload.message.strip()
        if not user_message:
            raise HTTPException(status_code=400, detail="Message cannot be empty.")
            
        result = gemini_service.chat(
            message=user_message,
            history=payload.history,
            language_preference=payload.language or "auto",
            assessment_context=payload.assessmentContext,
            api_key=payload.apiKey
        )
        return ChatResponse(**result)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Chat processing failed: {str(e)}")
