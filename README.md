# Twilio AI Assistant

A FastAPI-based voice assistant that receives calls via Twilio, processes speech with OpenAI, and responds naturally.

## Setup

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Environment Variables

Create a `.env` file in the project root:

```
TWILIO_ACCOUNT_SID=your_twilio_account_sid
TWILIO_AUTH_TOKEN=your_twilio_auth_token
OPENAI_API_KEY=your_openai_api_key
```

### 3. Run the Server

For local development:
```bash
python app.py
```

Or using uvicorn directly:
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

### 4. Expose Your Local Server (for testing)

Since Twilio needs a public URL, use ngrok or similar:

```bash
ngrok http 8000
```

Copy the HTTPS URL (e.g., `https://abc123.ngrok.io`)

### 5. Update call.py

Update the `url` in `call.py` with your ngrok URL:
```python
call = client.calls.create(
    url="https://abc123.ngrok.io/voice",  # Your ngrok URL
    to="+917447425465",
    from_="+12059645992",
)
```

### 6. Make a Test Call

Run:
```bash
python call.py
```

## How It Works

1. **Incoming Call** (`/voice` endpoint):
   - Greets caller: "Hi, this is your personal AI assistant. How may I help you?"
   - Listens for user's speech input

2. **Process Speech** (`/process` endpoint):
   - Receives transcribed speech from Twilio
   - Sends query to OpenAI GPT-3.5-turbo
   - Speaks the AI's response back to caller
   - Continues conversation loop

## Endpoints

- `GET /` - Health check
- `POST /voice` - Twilio webhook for incoming calls
- `POST /process` - Processes user speech and responds with LLM

## Production Deployment

For production, deploy to:
- Heroku
- AWS
- Google Cloud
- DigitalOcean
- Any platform that supports FastAPI

Update the webhook URL in your Twilio console to point to your production server.
