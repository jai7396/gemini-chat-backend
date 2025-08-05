
#. Gemini Chat Backend API - Postman Collection

This Postman collection provides a complete set of requests for interacting with the Gemini Chat Backend built using FastAPI. It covers authentication, chatroom management, chat messages, subscriptions (Stripe), and webhook testing.

---

##  Collection Structure

###  Auth
- **POST** `/auth/send-otp` - Send OTP to mobile number
- **POST** `/auth/verify-otp` - Verify OTP and receive JWT token

###  Users
- **GET** `/user/me` - Get current logged-in user info
- **POST** `/user/change-password` - Change the user's password

###  Chatroom
- **POST** `/chatroom` - Create a new chatroom
- **GET** `/chatroom` - List all chatrooms

###  Chat
- **POST** `/chat/send` - Send a message to Gemini (rate-limited by subscription tier)

###  Subscription
- **POST** `/subscription/start` - Create a Stripe checkout session
- **GET** `/subscription/status` - Check the user's current subscription tier

###  Webhook
- **POST** `/webhook/stripe` - Stripe webhook handler (no auth)

---

##  Setup Instructions

### 1. Import into Postman
- Open Postman
- Click **Import** > **Upload Files**
- Select the file: `Gemini_Backend_API.postman_collection.json`

### 2. Set Environment Variables
Create an environment in Postman with the following variables:

| Variable       | Example Value                        |
|----------------|--------------------------------------|
| `base_url`     | `http://localhost:8000`              |
| `jwt_token`    | `your-jwt-token-from-login`          |

Once the OTP is verified via `/auth/verify-otp`, copy the JWT token and set it in your environment.

### 3. Running Requests
- Use the folder structure to test APIs.
- Secure endpoints require `Authorization: Bearer {{jwt_token}}`.

---

##  Testing Webhook
For local webhook testing, use the Stripe CLI:

```bash
stripe listen --forward-to localhost:8000/webhook/stripe
```

Then trigger events like:

```bash
stripe trigger checkout.session.completed
```

---

##  Feedback
If you need additional routes, environment presets, or tests included, let us know!


---

##  How to Run the Project Locally

### 1. Clone the Repository

```bash
git clone https://github.com/your-username/gemini-chat-backend.git
cd gemini-chat-backend
```

### 2. Create and Activate Virtual Environment

```bash
python -m venv venv
source venv/bin/activate  # On Windows use `venv\Scripts\activate`
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Set Environment Variables

Create a `.env` file in the root directory with the following content:

```
DATABASE_URL=postgresql://postgres:yourpassword@localhost/gemini_backend
JWT_SECRET=your_jwt_secret
REDIS_URL=redis://localhost:6379
STRIPE_SECRET_KEY=your_stripe_secret
STRIPE_WEBHOOK_SECRET=your_stripe_webhook_secret
```

### 5. Start Redis Server

Make sure Redis is running locally:

```bash
redis-server
```

### 6. Run Database Migrations (if needed)

```bash
# You may use raw SQL or a tool like Alembic for migration
```

### 7. Start the FastAPI Server

```bash
uvicorn app.main:app --reload
```

Your API should now be running at: `http://localhost:8000`

---

##  Optional: Run Celery Worker (for background tasks)

```bash
celery -A app.tasks.worker worker --loglevel=info
```

---

##  Optional: Test Stripe Webhook

```bash
stripe listen --forward-to localhost:8000/webhook/stripe
stripe trigger checkout.session.completed
```
