"""
FastAPI server for the AI agent.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from agent import Agent

app = FastAPI(title="Social Media Market Sentiment Agent API", version="1.0.0")

# Initialize the agent
# agent = Agent()


class MessageRequest(BaseModel):
    """Request model for agent messages."""

    message: str
    system_prompt: str | None = None


class MessageResponse(BaseModel):
    """Response model for agent messages."""

    response: str
    status: str = "success"


@app.get("/")
async def root():
    """Health check endpoint."""
    return {"status": "ok", "message": "AI Agent API is running"}


@app.get("/health")
async def health():
    """Health check endpoint."""
    return {"status": "healthy"}


@app.post("/chat", response_model=MessageResponse)
async def chat(request: MessageRequest):
    """
    Process a chat message and return the agent's response.

    Args:
        request: MessageRequest containing the user's message and optional system prompt

    Returns:
        MessageResponse with the agent's response
    """
    try:
        # response_text = agent.call(
        #     message=request.message, system_prompt=request.system_prompt
        # )
        response_text = "Hello, how are you?"

        return MessageResponse(response=response_text, status="success")
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing request: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="localhost", port=8000)
