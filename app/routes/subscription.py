from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
from app.db_conn import conn
from app.config import STRIPE_SECRET_KEY, STRIPE_PRICE_ID, STRIPE_WEBHOOK_SECRET
import stripe


# Create router for subscription-related endpoints
router = APIRouter(prefix="/subscribe")

# Initialize Stripe with API key
stripe.api_key = STRIPE_SECRET_KEY

@router.post("/pro")
def subscribe_pro(request: Request):
    """
    Endpoint to handle Pro subscription purchases.
    Creates a Stripe checkout session for subscription payment.
    """
    # Check if user is authenticated
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = request.state.user

    try:
        # Create Stripe checkout session for subscription
        session = stripe.checkout.Session.create(
            payment_method_types=["card"],
            mode="subscription",
            line_items=[{
                "price": STRIPE_PRICE_ID,
                "quantity": 1
            }],
            success_url="https://gemini.com/success",  # Redirect URL after successful payment
            cancel_url="https://gemini.com/cancel",    # Redirect URL if payment is cancelled
            metadata={"user_id": user_id}              # Attach user_id to track subscription
        )
        return {"url": session.url}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/status")
def subscription_status(request: Request):
    """
    Endpoint to check user's current subscription status.
    Returns either 'Pro' or 'Basic' tier status.
    """
    # Check if user is authenticated
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = request.state.user
    
    # Query database for user's subscription tier
    cursor = conn.cursor()
    cursor.execute("SELECT subscription_tier FROM Users WHERE id = %s", (user_id,))
    row = cursor.fetchone()
    subscription = row[0] if row else "Basic"
    return {"subscription": subscription or "Basic"}
