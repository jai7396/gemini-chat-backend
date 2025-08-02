from starlette.middleware.base import BaseHTTPMiddleware
from fastapi.responses import JSONResponse
from app.jwt_utils import decode_token
import logging

class AuthMiddleware(BaseHTTPMiddleware):
    """Middleware for handling authentication using JWT tokens.
    Validates tokens and adds user info to request state."""
    
    async def dispatch(self, request, call_next):
        """Process each request to validate authentication.
        
        Args:
            request: The incoming request
            call_next: The next middleware/handler in the chain
            
        Returns:
            Response object
        """
        try:
            # Allow unauthenticated access to auth, signup, and webhook routes
            if request.url.path.startswith("/auth") or request.url.path.startswith("/signup") or request.url.path.startswith("/webhook"):
                return await call_next(request)
            
            auth = request.headers.get("Authorization")
            
            if not auth or not auth.startswith("Bearer "):
                return JSONResponse({"detail": "Unauthorized"}, status_code=401)
            
            token = auth.split(" ")[1]
            payload = decode_token(token)
            
            if not payload or "sub" not in payload:
                return JSONResponse({"detail": "Invalid or expired token"}, status_code=401)
            
            request.state.user = payload["sub"]
            return await call_next(request)
            
        except Exception as e:
            return JSONResponse({"detail": f"Middleware error: {str(e)}"}, status_code=500)