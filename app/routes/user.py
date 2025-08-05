from fastapi import APIRouter, Request, HTTPException, Body
from fastapi.responses import JSONResponse
from app.db_conn import conn  
import psycopg2

router = APIRouter(prefix='/user')

@router.get("/me")
def get_me(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = request.state.user

    try:
        cursor = conn.cursor()
        cursor.execute("SELECT mobile_number FROM Users WHERE id = %s", (user_id,))
        row = cursor.fetchone()
        if not row:
            raise HTTPException(status_code=404, detail="User not found")

        return JSONResponse(content={"id": user_id, "mobile_number": row[0]}, status_code=200)

    except Exception:
        raise HTTPException(status_code=500, detail="Database error")

@router.post("/change-password")
async def change_password(request: Request):
    if not hasattr(request.state, "user"):
        raise HTTPException(status_code=401, detail="Unauthorized")

    user_id = request.state.user

    try:
        data = await request.json()
        new_password = data.get("new_password")
        if not new_password:
            raise HTTPException(status_code=400, detail="Missing new_password")

        cursor = conn.cursor()
        cursor.execute("UPDATE Users SET password = %s WHERE id = %s", (new_password, user_id))
        conn.commit()

        return JSONResponse(content={"message": "Password updated"}, status_code=200)

    except psycopg2.Error:
        raise HTTPException(status_code=500, detail="Database error")
