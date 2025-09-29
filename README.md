# AI Chatbot Backend

A professional AI agent chatbot using OpenAI SDK with Gemini API endpoint.

## Features

- **Professional AI Agent Framework**: Built using the `agents` library with proper structure
- **Gemini Integration**: Uses Gemini 2.5 Flash model via OpenAI SDK compatibility
- **FastAPI REST API**: Ready for frontend integration
- **Multiple Agent Types**: Basic, Creative, Technical, and Customer Support specialists
- **Async Architecture**: Full async/await support for optimal performance
- **Environment Configuration**: Secure API key management
- **CORS Support**: Ready for web frontend integration

## Installation

1. Install Python dependencies:
```bash
pip install -r requirements.txt
```

2. Set up environment variables in `.env` file (already configured):
```
GEMINI_API_KEY=AIzaSyCVw0fs416KvQ7WDd-LpbKQs0tPz29g5S4
GEMINI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
GEMINI_MODEL=gemini-2.5-flash
PORT=8000
HOST=0.0.0.0
```

## Usage

### Test the Chatbot Core
```bash
python chatbot_core.py
```

### Start the API Server
```bash
python api_server.py
```

### Or use uvicorn directly
```bash
uvicorn api_server:app --host 0.0.0.0 --port 8000 --reload
```

## API Endpoints

- `GET /` - API information and available endpoints
- `GET /health` - Health check
- `GET /agent-info` - Get current agent information
- `POST /chat` - Send message to chatbot
- `POST /chat/stream` - Streaming chat (future feature)

### Example Chat Request
```json
POST /chat
{
  "message": "Hello! How are you today?",
  "agent_type": "basic"
}
```

### Example Response
```json
{
  "response": "Hello! I'm doing well, thank you for asking. How can I assist you today?",
  "agent_name": "AI Chatbot Assistant", 
  "model": "gemini-2.5-flash",
  "success": true,
  "error": null
}
```

## Agent Types

- **basic**: General conversational AI assistant
- **creative**: Creative writing and brainstorming specialist
- **technical**: Programming and technical support expert
- **customer_support**: Customer service focused agent

## Architecture

```
chatbot_core.py     # Core agent logic and business logic
api_server.py       # FastAPI REST API server
requirements.txt    # Python dependencies
.env               # Environment configuration
```

## Frontend Integration

The API is configured with CORS to accept requests from:
- `http://localhost:3000` 
- `http://127.0.0.1:3000`

Ready to connect with React, Next.js, or any web frontend.