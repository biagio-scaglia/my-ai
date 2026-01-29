import sys
import os
import uvicorn
from contextlib import asynccontextmanager
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Dict, Optional
from fastapi.responses import StreamingResponse
import json

# Ensure we can import modules from current directory
sys.path.append(os.getcwd())

# Global engine variables
engine = None
rag = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    global engine, rag
    print("Booting Neural Core...")
    try:
        from engine_cpp import CoddyEngine2
        from rag_engine import RagEngine

        # Init RAG
        rag = RagEngine()

        # Init Engine
        engine = CoddyEngine2()
        engine.start()
        print("Systems Online.")
    except Exception as e:
        print(f"Error starting engines: {e}")

    yield

    # Shutdown logic
    if engine:
        engine.close()
    if rag:
        try:
            rag.close()
        except:
            pass
    print("Systems Shutdown.")


app = FastAPI(
    title="Coddy AI API",
    description="API for Coddy AI Engine",
    version="2.0",
    lifespan=lifespan,
)

# CORS to allow frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify your frontend URL
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    messages: List[Message]
    use_web: bool = False


def stream_generator(messages, use_web):
    """
    Generator function for streaming response
    """
    # Convert Pydantic models to dicts
    history = [msg.dict() for msg in messages]

    user_query = history[-1]["content"]

    # 1. RAG Search
    rag_results = rag.search(user_query)
    context_parts = []

    if rag_results:
        context_parts.append("=== KNOWLEDGE BASE ===")
        for r in rag_results:
            context_parts.append(f"{r['text']}")

    # 2. Web Search (Optional - strictly if requested)
    if use_web:
        try:
            from coddy import web_search

            web_results = web_search(user_query)
            if web_results:
                context_parts.append("=== WEB RESULTS ===")
                context_parts.extend(web_results)
        except Exception as e:
            print(f"Web search error: {e}")

    # Build full input
    full_input = user_query
    if context_parts:
        full_input += "\n\n" + "\n".join(context_parts)

    generation_history = history[:-1] + [{"role": "user", "content": full_input}]

    # Stream
    for chunk in engine.stream_chat(generation_history, model_type="auto"):
        yield chunk


@app.post("/chat")
async def chat_endpoint(request: ChatRequest):
    if not engine:
        raise HTTPException(status_code=503, detail="Engine not ready")

    return StreamingResponse(
        stream_generator(request.messages, request.use_web), media_type="text/plain"
    )


@app.get("/health")
def health_check():
    return {"status": "online", "engine": "CoddyEngine2"}


if __name__ == "__main__":
    uvicorn.run("api:app", host="0.0.0.0", port=8000, reload=True)
