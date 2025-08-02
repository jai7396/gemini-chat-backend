# Import required libraries
from celery import Celery
from app.db_conn import conn  
import uuid

# Initialize Celery instance with Redis as message broker
celery = Celery(__name__, broker='redis://127.0.0.1:6379/0')

@celery.task
def gemini_reply(chatroom_id: str, prompt: str):
    """
    Asynchronous task to generate and store Gemini's reply
    Args:
        chatroom_id (str): ID of the chatroom
        prompt (str): User's input message
    """
    
    # Generate mock response by reversing the prompt
    reply = f"[Gemini Response]: {prompt[::-1]}"

    try:
        # Create database cursor
        cursor = conn.cursor()
        
        # Insert message into database with UUID as message ID
        cursor.execute(
            "INSERT INTO Messages (id, chatroom_id, sender_type, content) VALUES (%s, %s, %s, %s)",
            (str(uuid.uuid4()), chatroom_id, 'gemini', reply)
        )
        # Commit the transaction
        conn.commit()

    except Exception as e:
        # Rollback transaction on error
        conn.rollback()
        print(f"[Gemini Worker Error] {str(e)}")

    finally:
        # Always close cursor
        cursor.close()
