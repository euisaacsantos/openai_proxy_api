
from fastapi import FastAPI
from pydantic import BaseModel
import openai
import os
import time

# Get the API key from environment variables
api_key = os.environ.get("OPENAI_API_KEY")
if not api_key:
    raise ValueError("A variável de ambiente OPENAI_API_KEY não foi definida.")

client = openai.OpenAI(api_key=api_key)
app = FastAPI()

class ChatRequest(BaseModel):
    session_id: str | None = None  # session_id is optional
    assistant_id: str
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
            assistant_id=request.assistant_id,
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

            # Replace double quotes with single quotes to prevent JSON breaking
            assistant_message = assistant_message.replace('"', "'")

            return {
                "response": assistant_message,
                "session_id": thread_id # Return session_id for subsequent requests
            }
        else:
            return {"error": f"Run failed with status: {run.status}"}

    except Exception as e:
        return {"error": str(e)}

