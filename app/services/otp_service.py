import redis
from app.config import REDIS_URL, OTP_EXPIRY_SECONDS

# Initialize Redis client with the configured URL
r = redis.from_url(REDIS_URL)

def store_otp(mobile, otp):
    """
    Store OTP in Redis with expiration time
    Args:
        mobile: User's mobile number
        otp: One-time password to store
    """
    r.setex(f"otp:{mobile}", OTP_EXPIRY_SECONDS, otp)

def verify_stored_otp(mobile, otp):
    """
    Verify if provided OTP matches stored OTP
    Args:
        mobile: User's mobile number
        otp: One-time password to verify
    Returns:
        bool: True if OTP matches, False otherwise
    """
    stored = r.get(f"otp:{mobile}")
    return stored and stored.decode() == otp
