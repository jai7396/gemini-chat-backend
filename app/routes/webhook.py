from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import stripe
import json
from app.db_conn import conn  
from app.config import STRIPE_WEBHOOK_SECRET  

router = APIRouter(prefix="/webhook")

# Check this is in postman

@router.post("/webhook/stripe")  
async def stripe_webhook(request: Request):
    payload = await request.body()
    
    # Check if this is a test request
    is_test_request = request.headers.get("user-agent", "").lower().startswith("postman") or \
                     request.headers.get("x-test-webhook") == "true"
    
    if is_test_request:
        try:
            event = json.loads(payload.decode("utf-8"))

        except json.JSONDecodeError as e:
            raise HTTPException(status_code=400, detail=f"Invalid JSON: {str(e)}")
    else:
        # Production: Verify signature
        signature = (
            request.headers.get("stripe-signature") or 
            request.headers.get("Stripe-Signature") or
            request.headers.get("HTTP_STRIPE_SIGNATURE")
        )
        
        if not signature:
            print("Available headers:", dict(request.headers))
            raise HTTPException(status_code=400, detail="Missing Stripe signature")
        
        try:
            event = stripe.Webhook.construct_event(
                payload,
                signature,
                STRIPE_WEBHOOK_SECRET
            )
        except stripe.error.SignatureVerificationError as e:
            print(f"Signature verification failed: {e}")
            raise HTTPException(status_code=400, detail="Invalid signature")
        except Exception as e:
            print(f"Webhook error: {e}")
            raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")
    
    # Handle the event
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        user_id = session["metadata"].get("user_id")
        
        if user_id:
            try:
                cursor = conn.cursor()
                cursor.execute("UPDATE Users SET subscription_tier = 'Pro' WHERE id = %s", (user_id,))
                conn.commit()
                cursor.close()
            except Exception as db_error:
                conn.rollback()
        else:
            print("No user_id found in session metadata")  
    return JSONResponse(status_code=200, content={"received": True})


# Check this api in stripe 

from fastapi import APIRouter, Request, HTTPException
from fastapi.responses import JSONResponse
import stripe
from app.config import STRIPE_WEBHOOK_SECRET  
from app.db_conn import conn  

router = APIRouter(prefix="/webhook")

@router.post("/stripe")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")

    try:
        event = stripe.Webhook.construct_event(
            payload=payload,
            sig_header=sig_header,
            secret=STRIPE_WEBHOOK_SECRET
        )
    except stripe.error.SignatureVerificationError:
        raise HTTPException(status_code=400, detail="Invalid Stripe signature")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Webhook error: {str(e)}")

    # Handle different event types
    event_type = event["type"]
    data = event["data"]["object"]

    if event_type == "checkout.session.completed":
        user_id = data.get("metadata", {}).get("user_id")

        if not user_id:
            print(" No user_id found in metadata")
        else:
            with conn.cursor() as cur:
                cur.execute(
                    "UPDATE Users SET subscription_tier = 'Pro', WHERE id = %s",
                    ( user_id,)
                )
                conn.commit()

    elif event_type == "payment_intent.succeeded":
        print(" Payment succeeded:", data["id"])

    elif event_type == "payment_intent.payment_failed":
        print(" Payment failed:", data["id"])

    return JSONResponse(status_code=200, content={"status": "success"})

