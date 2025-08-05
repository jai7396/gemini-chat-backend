from fastapi import Request, FastAPI
from fastapi.responses import JSONResponse


def add_error_handlers(app: FastAPI):
    """
    Adds global exception handler to the FastAPI application.
    Args:
        app (FastAPI): The FastAPI application instance
    """
    
    @app.exception_handler(Exception)
    async def global_exception_handler(request: Request, exc: Exception):
        """
        Global exception handler that catches all unhandled exceptions.
        Args:
            request (Request): The incoming HTTP request
            exc (Exception): The exception that was raised
            
        Returns:
            JSONResponse: A JSON response with 500 status code and error details
        """
        return JSONResponse(status_code=500, content={"detail": str(exc)})
