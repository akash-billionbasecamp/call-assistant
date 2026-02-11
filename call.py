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
# Replace 'https://yourdomain.com' with your actual server URL (use ngrok for local testing)
call = client.calls.create(
    url="https://yourdomain.com/voice",  # Replace with your server URL + /voice endpoint
    to="+917447425465",
    from_="+12059645992",
)

print(call.sid)
