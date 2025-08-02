from fastapi import APIRouter, HTTPException, Body, Request
from uuid import uuid4
from datetime import datetime, timedelta
import random
from app.jwt_utils import create_token
from app.services.otp_service import store_otp, verify_stored_otp
from app.db_conn import conn

# Create router instance with /auth prefix
router = APIRouter(prefix="/auth")

@router.post("/signup")
def signup(body: dict = Body(...)):
    """
    Handle user signup by mobile number.
    Creates a new user if mobile number doesn't exist.
    """
    mobile_number = body.get("mobile_number")
    if not mobile_number:
        return {"error": "mobile_number is required"}

    cursor = conn.cursor()
    
    # Check if user already exists in database
    cursor.execute("SELECT id FROM Users WHERE mobile_number = %s", (mobile_number,))
    existing_user = cursor.fetchone()

    if existing_user:
        return {"user_id": existing_user[0], "mobile_number": mobile_number, "message": "User already registered"}

    # Create new user with UUID and mobile number
    user_id = str(uuid4())
    cursor.execute(
        "INSERT INTO Users (id, mobile_number) VALUES (%s, %s)",
        (user_id, mobile_number)
    )
    conn.commit()
    return {"user_id": user_id, "mobile_number": mobile_number, "message": "User registered"}

@router.post("/send-otp")
def send_otp(body: dict = Body(...)):
    """
    Generate and store a 4-digit OTP for the given mobile number.
    """
    mobile_number = body.get("mobile_number")
    if not mobile_number:
        raise HTTPException(status_code=400, detail="mobile_number is required")

    # Generate random 4-digit OTP and store it
    otp = str(random.randint(1000, 9999))
    store_otp(mobile_number, otp)
    return {"otp": otp}

@router.post("/verify-otp")
def verify_otp(body: dict = Body(...)):
    """
    Verify OTP for mobile number and generate JWT token upon success.
    """
    mobile_number = body.get("mobile_number")
    otp = body.get("otp")

    if not mobile_number or not otp:
        raise HTTPException(status_code=400, detail="mobile_number and otp are required")

    # Verify OTP and generate token if valid
    if verify_stored_otp(mobile_number, otp):
        cursor = conn.cursor()
        cursor.execute("SELECT id FROM Users WHERE mobile_number = %s", (mobile_number,))
        user = cursor.fetchone()
        if not user:
            raise HTTPException(status_code=404, detail="User not found")
        token = create_token({"sub": user[0]})
        return {"token": token}
    
    raise HTTPException(status_code=401, detail="Invalid OTP")

@router.post("/forgot-password")
def forgot_password(body: dict = Body(...)):
    """
    Handle forgot password request by generating new OTP.
    """
    mobile_number = body.get("mobile_number")
    if not mobile_number:
        raise HTTPException(status_code=400, detail="mobile_number is required")

    # Generate and store new OTP for password reset
    otp = str(random.randint(1000, 9999))
    store_otp(mobile_number, otp)
    return {"otp": otp, "message": "Use this OTP to reset password."}
