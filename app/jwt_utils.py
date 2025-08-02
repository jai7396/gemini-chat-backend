import jwt
import json
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
from datetime import datetime, timedelta
from app.config import JWT_SECRET, JWT_ALGORITHM

def create_token(data: dict, expires_in: int = 3600):
    """
    Create a JWT token with expiration using the 'jwt' library.
    
    Args:
        data (dict): The payload data to encode
        expires_in (int): Token expiration time in seconds (default: 1 hour)
    
    Returns:
        str: Encoded JWT token
    """
    payload = data.copy()
    payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_in)
    return jwt.encode(payload, JWT_SECRET, JWT_ALGORITHM)

def decode_token(token: str):
    """
    Decode and validate a JWT token using the 'jwt' library.
    
    Args:
        token (str): The JWT token to decode
    
    Returns:
        dict or None: Decoded payload if valid, None if invalid or expired
    """
    try:
        decoded = jwt.decode(token, JWT_SECRET, JWT_ALGORITHM)
        
        # Manual expiration check since 'jwt' library doesn't handle it automatically
        if 'exp' in decoded:
            exp_timestamp = decoded['exp']
            if isinstance(exp_timestamp, datetime):
                exp_time = exp_timestamp
            else:
                exp_time = datetime.utcfromtimestamp(exp_timestamp)
            
            if datetime.utcnow() > exp_time:
                return None
        
        return decoded
    except Exception:
        # The 'jwt' library raises generic exceptions
        return None
    
# import jwt
# from jwt.exceptions import ExpiredSignatureError, InvalidTokenError
# from datetime import datetime, timedelta
# from app.config import JWT_SECRET, JWT_ALGORITHM

# def create_token(data: dict, expires_in: int = 3600):
#     payload = data.copy()
#     payload["exp"] = datetime.utcnow() + timedelta(seconds=expires_in)
#     return jwt.encode(payload, JWT_SECRET, algorithm=JWT_ALGORITHM)

# def decode_token(token: str):
#     try:
#         return jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
#     except ExpiredSignatureError:
#         return None
#     except InvalidTokenError:
#         return None
