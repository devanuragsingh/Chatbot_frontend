from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.services.llm_service import generate_response

router = APIRouter()


# ✅ Request schema (clean + safe)
class ChatRequest(BaseModel):
    message: str
    session_id: str = "default"


@router.post("/chat")
def chat(request: ChatRequest):
    try:
        print("📩 Incoming message:", request.message)

        reply = generate_response(request.message, request.session_id)

        print("🤖 Bot reply:", reply)

        return {
            "session_id": request.session_id,
            "user": request.message,
            "bot": reply
        }

    except Exception as e:
        print("❌ ROUTE ERROR:", str(e))
        raise HTTPException(status_code=500, detail="Server error")