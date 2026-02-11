# Download the helper library from https://www.twilio.com/docs/python/install
import os
from dotenv import load_dotenv
from twilio.rest import Client

# Load environment variables from .env file
load_dotenv()

# Find your Account SID and Auth Token at twilio.com/console
# and set the environment variables. See http://twil.io/secure
account_sid = os.getenv("TWILIO_ACCOUNT_SID")
auth_token = os.getenv("TWILIO_AUTH_TOKEN")
client = Client(account_sid, auth_token)

# Make a call that will be handled by the webhook server
# IMPORTANT: Twilio REQUIRES HTTPS for webhooks. Options:
# 1. Use ngrok: "https://abc123.ngrok.io/voice" (recommended for testing)
# 2. Set up SSL certificate on your server
# 3. For testing only, try HTTP (may not work): "http://65.0.173.124:8006/voice"
# The endpoint MUST be /voice (as defined in app.py)
call = client.calls.create(
    url="http://65.0.173.124:8006/voice",  # Change to HTTPS when SSL is set up
    to="+917447425465",
    from_="+12059645992",
)

print(call.sid)
