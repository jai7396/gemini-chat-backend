from fastapi import FastAPI
from app.routes import auth, user, chatroom, subscription, webhook, chat
# from app.middleware.auth_middleware import auth_middleware
from app.middleware.error_handler import add_error_handlers
from app.middleware.auth_middleware import AuthMiddleware

app = FastAPI()

# app.middleware('http')(auth_middleware)
add_error_handlers(app)

# app = FastAPI()
app.add_middleware(AuthMiddleware)

app.include_router(auth.router)
app.include_router(user.router)
app.include_router(chatroom.router)
app.include_router(subscription.router)
app.include_router(webhook.router)
app.include_router(chat.router)
