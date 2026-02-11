from fastapi import FastAPI, Form, Request
from fastapi.responses import Response
from twilio.twiml.voice_response import VoiceResponse, Gather
import os
from dotenv import load_dotenv
from openai import OpenAI
import logging

# Load environment variables
load_dotenv()

# Initialize FastAPI app
app = FastAPI()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def get_openai_client():
    """Get OpenAI client, initializing it lazily"""
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")
    return OpenAI(api_key=api_key)


@app.post("/voice")
async def voice_webhook(request: Request):
    """
    Webhook endpoint for incoming calls.
    Greets the caller and listens for their input.
    """
    response = VoiceResponse()
    
    # Greet the caller
    response.say(
        "Hi, this is your personal AI assistant. How may I help you?",
        voice="Polly.Joey",
        language="en-US"
    )
    
    # Gather user's speech input
    gather = Gather(
        input="speech",
        language="en-US",
        speech_timeout="auto",
        action="/process",
        method="POST"
    )
    response.append(gather)
    
    # If no input, say goodbye
    response.say(
        "I didn't hear anything. Please call back when you're ready.",
        voice="Polly.Joey",
        language="en-US"
    )
    
    return Response(content=str(response), media_type="application/xml")


@app.post("/process")
async def process_speech(
    request: Request,
    SpeechResult: str = Form(None)
):
    """
    Process the user's speech input, send to LLM, and respond.
    """
    response = VoiceResponse()
    
    if not SpeechResult:
        response.say(
            "I'm sorry, I didn't catch that. Could you please repeat?",
            voice="Polly.Joey",
            language="en-US"
        )
        gather = Gather(
            input="speech",
            language="en-US",
            speech_timeout="auto",
            action="/process",
            method="POST"
        )
        response.append(gather)
        return Response(content=str(response), media_type="application/xml")
    
    logger.info(f"User said: {SpeechResult}")
    
    try:
        # Get OpenAI client
        openai_client = get_openai_client()
        
        # Send user query to OpenAI
        completion = openai_client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful AI assistant. Keep your responses concise and conversational, suitable for phone calls."},
                {"role": "user", "content": SpeechResult}
            ],
            max_tokens=150,
            temperature=0.7
        )
        
        llm_response = completion.choices[0].message.content
        logger.info(f"LLM response: {llm_response}")
        
        # Speak the LLM's response
        response.say(
            llm_response,
            voice="Polly.Joey",
            language="en-US"
        )
        
        # Ask if they need anything else
        response.say(
            "Is there anything else I can help you with?",
            voice="Polly.Joey",
            language="en-US"
        )
        
        # Continue listening for more input
        gather = Gather(
            input="speech",
            language="en-US",
            speech_timeout="auto",
            action="/process",
            method="POST"
        )
        response.append(gather)
        
        # If no response, end the call
        response.say(
            "Thank you for calling. Have a great day!",
            voice="Polly.Joey",
            language="en-US"
        )
        response.hangup()
        
    except Exception as e:
        logger.error(f"Error processing with LLM: {str(e)}")
        response.say(
            "I'm sorry, I encountered an error. Please try again later.",
            voice="Polly.Joey",
            language="en-US"
        )
        response.hangup()
    
    return Response(content=str(response), media_type="application/xml")


@app.get("/")
async def root():
    """Health check endpoint"""
    return {"status": "ok", "message": "Twilio AI Assistant Server is running"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
