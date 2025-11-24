
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import time
from typing import Optional


# Get the API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi definida.")

# Get the Assistant ID from environment variables
default_assistant_id = os.environ.get("ASSISTANT_ID")

client = openai.OpenAI(api_key=api_key)
app = FastAPI()

# Mount static files
from fastapi.staticfiles import StaticFiles
app.mount("/static", StaticFiles(directory="static"), name="static")

class ChatRequest(BaseModel):
    session_id: Optional[str] = None  # session_id is optional
    assistant_id: Optional[str] = None # assistant_id is optional if env var is set
    message: str
    assunto: str
    objetivo: str

@app.get("/")
def read_root():
    return {"Status": "API is running. Use the /chat endpoint to interact."}

@app.post("/chat")
def chat_with_assistant(request: ChatRequest):
    """
    Handles a chat request with the OpenAI assistant.
    1. Creates a thread if session_id is not provided.
    2. Adds a message to the thread.
    3. Runs the assistant.
    4. Waits for the run to complete.
    5. Returns the assistant's latest response.
    """
    try:
        # Determine assistant_id
        assistant_id = request.assistant_id or default_assistant_id
        if not assistant_id:
             return {"error": "Assistant ID not provided and ASSISTANT_ID env var not set."}

        # Step 1: Create a new thread or use the existing one
        thread_id = request.session_id
        if thread_id is None:
            thread = client.beta.threads.create()
            thread_id = thread.id

        # Step 2: Add the user's message to the thread
        client.beta.threads.messages.create(
            thread_id=thread_id,
            role="user",
            content=request.message
        )

        # Step 3: Run the assistant
        run = client.beta.threads.runs.create(
            thread_id=thread_id,
            assistant_id=assistant_id,
            additional_instructions=f"Assunto: {request.assunto}. Objetivo: {request.objetivo}"
        )

        # Step 4: Wait for the run to complete
        while run.status in ['queued', 'in_progress', 'cancelling']:
            time.sleep(1)
            run = client.beta.threads.runs.retrieve(thread_id=thread_id, run_id=run.id)

        if run.status == 'completed':
            # Step 5: Retrieve the latest messages from the thread
            messages = client.beta.threads.messages.list(thread_id=thread_id)
            # The latest message is from the assistant
            assistant_message = messages.data[0].content[0].text.value

            # Replace all types of quotes with single quotes for ManyChat compatibility
            assistant_message = assistant_message.replace('"', "'")  # Straight double quotes
            assistant_message = assistant_message.replace('\u201c', "'")  # Left curly quote "
            assistant_message = assistant_message.replace('\u201d', "'")  # Right curly quote "

            return {
                "version": "v2",
                "content": {
                    "messages": [
                        {
                            "type": "text",
                            "text": assistant_message
                        }
                    ]
                }
            }
        else:
            return {"error": f"Run failed with status: {run.status}"}

    except Exception as e:
        return {"error": str(e)}

