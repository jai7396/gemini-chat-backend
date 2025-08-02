from fastapi import APIRouter, Request, HTTPException
from app.jwt_utils import decode_token 
from app.rate_limit import check_rate_limit, get_user_subscription_tier
from app.genai import send_to_gemini

router = APIRouter(prefix="/chat")

@router.post("/send")
async def send_message(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = request.state.user

    tier = get_user_subscription_tier(user_id)
    if tier.lower() == "basic":
        check_rate_limit(user_id)

    data = await request.json()
    user_message = data.get("message")
    if not user_message:
        raise HTTPException(status_code=400, detail="Message is required")

    gemini_response = send_to_gemini(user_message)
    return {"reply": gemini_response}
