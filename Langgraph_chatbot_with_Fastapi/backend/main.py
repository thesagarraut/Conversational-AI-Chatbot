from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from uuid import uuid4

from langchain_core.messages import HumanMessage

from backend.langgraph_backend_with_database import(chatbot, retrieve_all_threads)
import logging

logger = logging.getLogger(__name__)

app = FastAPI(
    title="LangGraph Chatbot API",
    description="API for a persistent AI chatbot",
    version="1.0.0"
)

class ChatRequest(BaseModel):
    thread_id: str
    message: str
    
class CreateThreadResponse(BaseModel):
    thread_id: str
    
@app.get("/")
def home():
    return {"message": "LangGraph Chatbot API is running"}

#  Create a new conversation ID
@app.post("/threads", response_model=CreateThreadResponse)
def create_thread():
    return {"thread_id": str(uuid4())}

# 3. List saved conversations
@app.get("/threads")
def get_threads():
    return {
        "threads": retrieve_all_threads()
    }
    
#  Send a message to the chatbot
@app.post("/chat")
def chat(request: ChatRequest):
    if not request.message.strip():
        raise HTTPException(
            status_code=400,
            detail="Message cannot be empty",
        )

    config = {
        "configurable": {
            "thread_id": request.thread_id
        }
    }

    try:
        result = chatbot.invoke(
            {
                "messages": [
                    HumanMessage(content=request.message)
                ]
            },
            config=config,
        )

        answer = result["messages"][-1].content

        return {
            "thread_id": request.thread_id,
            "user_message": request.message,
            "answer": answer,
        }

    except Exception as exc:
        logger.exception("Chatbot invocation failed")

        raise HTTPException(
            status_code=500,
            detail="Failed to generate chatbot response",
        ) from exc
        
# . Load an existing conversation
@app.get("/threads/{thread_id}")
def get_thread(thread_id: str):
    config = {
        "configurable": {
            "thread_id": thread_id
        }
    }

    try:
        state = chatbot.get_state(config)
        messages = state.values.get("messages", [])

        return {
            "thread_id": thread_id,
            "messages": [
                {
                    "role": (
                        "user"
                        if isinstance(msg, HumanMessage)
                        else "assistant"
                    ),
                    "content": msg.content,
                }
                for msg in messages
            ],
        }

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail="Failed to load conversation",
        ) from exc