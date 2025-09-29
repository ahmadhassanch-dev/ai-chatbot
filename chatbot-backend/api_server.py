#!/usr/bin/env python3
"""
FastAPI Server for AI Chatbot
This provides REST API endpoints for the chatbot to connect with frontend
"""

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from pydantic import BaseModel
from typing import Optional, List, Dict, Any
import asyncio
import logging
from chatbot_core import create_basic_chatbot_agent, ChatbotService, create_specialized_agent, RunConfig

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global chatbot service instance
chatbot_service: Optional[ChatbotService] = None


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup and shutdown events"""
    global chatbot_service
    try:
        logger.info("Initializing chatbot service...")
        agent = create_basic_chatbot_agent()
        chatbot_service = ChatbotService(agent)
        logger.info("✅ Chatbot service initialized successfully")
        yield
    except Exception as e:
        logger.error(f"❌ Failed to initialize chatbot service: {e}")
        raise
    finally:
        logger.info("Shutting down chatbot service...")


# Initialize FastAPI app with lifespan
app = FastAPI(
    title="AI Chatbot API",
    description="REST API for AI Chatbot using Gemini with OpenAI SDK",
    version="1.0.0",
    lifespan=lifespan
)

# Configure CORS for frontend connection
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],  # Frontend URLs
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# Pydantic models for request/response
class ChatRequest(BaseModel):
    message: str
    agent_type: Optional[str] = "basic"  # basic, creative, technical, etc.


class ChatResponse(BaseModel):
    response: str
    agent_name: str
    model: str
    success: bool = True
    error: Optional[str] = None


class AgentInfo(BaseModel):
    name: str
    model: str
    instructions: str
    available_types: List[str]


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": "AI Chatbot API is running",
        "version": "1.0.0",
        "status": "active",
        "endpoints": {
            "/chat": "POST - Send message to chatbot",
            "/agent-info": "GET - Get current agent information",
            "/health": "GET - Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    global chatbot_service
    return {
        "status": "healthy" if chatbot_service is not None else "initializing",
        "service": "AI Chatbot API",
        "model": "gemini-2.5-flash"
    }


@app.get("/agent-info", response_model=AgentInfo)
async def get_agent_info():
    """Get information about the current agent"""
    global chatbot_service
    
    if chatbot_service is None:
        raise HTTPException(status_code=503, detail="Chatbot service not initialized")
    
    try:
        info = chatbot_service.get_agent_info()
        return AgentInfo(
            name=info["name"],
            model=info["model"],
            instructions=info["instructions"],
            available_types=["basic", "creative", "technical", "customer_support"]
        )
    except Exception as e:
        logger.error(f"Error getting agent info: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to get agent info: {str(e)}")


@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    """
    Main chat endpoint for sending messages to the AI agent
    """
    global chatbot_service
    
    if chatbot_service is None:
        raise HTTPException(status_code=503, detail="Chatbot service not initialized")
    
    if not request.message.strip():
        raise HTTPException(status_code=400, detail="Message cannot be empty")
    
    try:
        # Handle different agent types
        if request.agent_type != "basic":
            agent = get_specialized_agent(request.agent_type)
            temp_service = ChatbotService(agent)
            response = await temp_service.chat(request.message)
            agent_info = temp_service.get_agent_info()
        else:
            response = await chatbot_service.chat(request.message)
            agent_info = chatbot_service.get_agent_info()
        
        return ChatResponse(
            response=response,
            agent_name=agent_info["name"],
            model=agent_info["model"],
            success=True
        )
        
    except Exception as e:
        logger.error(f"Error in chat endpoint: {e}")
        return ChatResponse(
            response="I apologize, but I encountered an error processing your request.",
            agent_name="Error Handler",
            model="gemini-2.5-flash",
            success=False,
            error=str(e)
        )


def get_specialized_agent(agent_type: str):
    """Create specialized agents based on type"""
    
    agent_configs = {
        "creative": {
            "specialty": "Creative Assistant",
            "instructions": """You are a creative AI assistant specializing in:
            - Creative writing and storytelling
            - Brainstorming and ideation
            - Art and design concepts
            - Marketing and content creation
            - Problem-solving with creative approaches
            
            Be imaginative, inspiring, and help users think outside the box."""
        },
        "technical": {
            "specialty": "Technical Expert",
            "instructions": """You are a technical AI assistant specializing in:
            - Programming and software development
            - Technical troubleshooting
            - Code reviews and optimization
            - System architecture and design
            - Technology explanations and tutorials
            
            Be precise, detailed, and provide practical solutions."""
        },
        "customer_support": {
            "specialty": "Customer Support",
            "instructions": """You are a customer support AI assistant specializing in:
            - Helping users with product questions
            - Troubleshooting common issues
            - Providing clear, step-by-step guidance
            - Escalating complex issues appropriately
            - Maintaining a helpful and empathetic tone
            
            Always be patient, understanding, and solution-focused."""
        }
    }
    
    config = agent_configs.get(agent_type, agent_configs["creative"])
    return create_specialized_agent(config["specialty"], config["instructions"])


@app.post("/chat/stream")
async def chat_stream_endpoint(request: ChatRequest):
    """
    Streaming chat endpoint (for future real-time features)
    """
    # This would implement Server-Sent Events for streaming responses
    # For now, we'll return a regular response
    return await chat_endpoint(request)


if __name__ == "__main__":
    import uvicorn
    
    # Get configuration from environment
    import os
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    
    print(f"🚀 Starting AI Chatbot API server on {host}:{port}")
    print("📡 Ready to connect with frontend!")
    
    uvicorn.run(
        "api_server:app",
        host=host,
        port=port,
        reload=True,
        log_level="info"
    )