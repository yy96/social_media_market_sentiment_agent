# Social Media Market Sentiment Agent

A toy project for learning production AI agent systems. This project implements a basic AI agent with a FastAPI backend and CLI interface.

## Features

- Basic AI agent call/response functionality using OpenAI
- FastAPI server for handling agent requests
- Command-line interface for interacting with the agent
- Support for system prompts to guide agent behavior

## Setup

1. **Activate the virtual environment:**
   ```bash
   source venv/bin/activate
   ```
   (The virtual environment has already been created for you)

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   Create a `.env` file in the project root:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```
   You can get your API key from [OpenAI Platform](https://platform.openai.com/api-keys)

## Usage

### Starting the FastAPI Server

Run the server:
```bash
python api.py
```

Or using uvicorn directly:
```bash
uvicorn api:app --reload
```

The server will start on `http://localhost:8000`

### Using the CLI

**Interactive mode:**
```bash
python cli.py
```

**Single message mode:**
```bash
python cli.py -m "Hello, how are you?"
```

**With system prompt:**
```bash
python cli.py -m "What is the weather?" -s "You are a helpful assistant."
```

### API Endpoints

- `GET /` - Health check
- `GET /health` - Health check endpoint
- `POST /chat` - Send a message to the agent
  ```json
  {
    "message": "Your message here",
    "system_prompt": "Optional system prompt"
  }
  ```

## Project Structure

```
.
├── agent.py          # Core AI agent module
├── api.py            # FastAPI server
├── cli.py            # Command-line interface
├── requirements.txt  # Python dependencies
└── README.md         # This file
```

## Next Steps

This is the basic foundation. Future enhancements could include:
- Conversation history/memory
- Tool calling and function execution
- Multi-agent systems
- Streaming responses
- Error handling and retries
- Logging and monitoring