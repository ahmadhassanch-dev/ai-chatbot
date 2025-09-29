#!/usr/bin/env python3
"""
AI Agent Chatbot using OpenAI SDK with Gemini API
This script creates a professional AI agent chatbot that can interact with users
and be connected to a frontend application.
"""

import asyncio  # For running asynchronous event loops
import os       # For accessing environment variables
from dotenv import load_dotenv  # To load environment variables from a .env file
from typing import List, Optional, Dict, Any
import logging
from dataclasses import dataclass

# Import OpenAI SDK directly
from openai import AsyncOpenAI

# Load .env file so secrets/keys don't live in code
load_dotenv()

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Load Gemini API key (needed to connect to Google Gemini)
gemini_api_key = os.getenv("GEMINI_API_KEY")
if not gemini_api_key:
    raise ValueError("GEMINI_API_KEY is not set in environment variables!")


@dataclass
class RunConfig:
    """Configuration for agent runs"""
    temperature: float = 0.7
    max_tokens: Optional[int] = None
    timeout: float = 30.0


class OpenAIChatCompletionsModel:
    """
    Chat completions model using OpenAI SDK with Gemini API endpoint
    """
    
    def __init__(
        self,
        model: str = "gemini-2.5-flash",
        openai_client: Optional[AsyncOpenAI] = None,
        temperature: float = 0.7,
        max_tokens: Optional[int] = None
    ):
        self.model = model
        self.temperature = temperature
        self.max_tokens = max_tokens
        
        # Use provided client or create new one
        if openai_client:
            self.client = openai_client
        else:
            # Setup an AsyncOpenAI client that points to Gemini's endpoint
            self.client = AsyncOpenAI(
                api_key=gemini_api_key,
                base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
            )
        
        logger.info(f"Initialized OpenAIChatCompletionsModel with model: {self.model}")
    
    async def generate_response(
        self,
        messages: List[Dict[str, str]],
        temperature: Optional[float] = None,
        max_tokens: Optional[int] = None
    ) -> str:
        """
        Generate a chat completion response
        
        Args:
            messages: List of message dictionaries with 'role' and 'content'
            temperature: Override default temperature
            max_tokens: Override default max_tokens
            
        Returns:
            Response string
        """
        try:
            completion = await self.client.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=temperature or self.temperature,
                max_tokens=max_tokens or self.max_tokens
            )
            
            response_message = completion.choices[0].message.content
            return response_message
                
        except Exception as e:
            logger.error(f"Error generating response: {str(e)}")
            raise Exception(f"Failed to generate response: {str(e)}")


class Agent:
    """
    AI Agent class that manages chat interactions and context
    """
    
    def __init__(
        self,
        model: OpenAIChatCompletionsModel,
        name: str = "AI Assistant",
        instructions: Optional[str] = None
    ):
        self.model = model
        self.name = name
        self.instructions = instructions or "You are a helpful AI assistant."
        self.conversation_history: List[Dict[str, str]] = []
        
        # Add system message if provided
        if self.instructions:
            self.conversation_history.append({
                "role": "system",
                "content": self.instructions
            })
            
        logger.info(f"Initialized Agent: {self.name}")
    
    def add_message(self, role: str, content: str) -> None:
        """Add a message to conversation history"""
        message = {"role": role, "content": content}
        self.conversation_history.append(message)
        logger.debug(f"Added {role} message to conversation")
    
    async def chat(self, user_message: str) -> str:
        """
        Process user message and generate response
        
        Args:
            user_message: The user's input message
            
        Returns:
            Response string
        """
        try:
            # Add user message to history
            self.add_message("user", user_message)
            
            # Generate response using the model
            response = await self.model.generate_response(self.conversation_history)
            
            # Add assistant response to history
            self.add_message("assistant", response)
            
            return response
            
        except Exception as e:
            logger.error(f"Error in chat method: {str(e)}")
            raise Exception(f"Chat processing failed: {str(e)}")
    
    def clear_history(self, keep_system: bool = True) -> None:
        """Clear conversation history"""
        if keep_system and self.conversation_history and self.conversation_history[0]["role"] == "system":
            system_msg = self.conversation_history[0]
            self.conversation_history = [system_msg]
        else:
            self.conversation_history = []
        logger.info("Conversation history cleared")


class Runner:
    """
    Runner class to manage agent execution and provide utility methods
    """
    
    def __init__(self):
        logger.info("Runner initialized")
    
    @staticmethod
    async def run(
        starting_agent: Agent,
        input: str,
        run_config: Optional[RunConfig] = None
    ):
        """
        Execute a single query through the agent
        
        Args:
            starting_agent: The agent to run
            input: User input string
            run_config: Optional run configuration
            
        Returns:
            Result object with final_output
        """
        try:
            response = await starting_agent.chat(input)
            
            # Return a simple result object
            class Result:
                def __init__(self, output):
                    self.final_output = output
            
            return Result(response)
            
        except Exception as e:
            logger.error(f"Error running agent: {str(e)}")
            raise


def set_tracing_disabled(disabled: bool = True):
    """Disable tracing (placeholder function for compatibility)"""
    if disabled:
        logger.info("Tracing disabled")
    else:
        logger.info("Tracing enabled")


# Setup an AsyncOpenAI client that points to Gemini's endpoint
external_client = AsyncOpenAI(
    api_key=gemini_api_key,
    base_url="https://generativelanguage.googleapis.com/v1beta/openai/"
)

# Bind the client into an OpenAI-like Chat Completions model
model = OpenAIChatCompletionsModel(
    model="gemini-2.5-flash",  # Which Gemini model to use
    openai_client=external_client
)

# Disable tracing (useful if you don't want logs or monitoring overhead)
set_tracing_disabled(disabled=True)

def create_basic_chatbot_agent() -> Agent:
    """
    Create a basic chatbot agent with general conversational capabilities.
    
    Returns:
        Agent: Configured AI agent for chatbot functionality
    """
    agent = Agent(
        model=model,
        name="AI Chatbot Assistant",
        instructions="""You are a helpful, friendly, and knowledgeable AI assistant. 
        You can help users with a wide range of tasks including:
        - Answering questions on various topics
        - Providing explanations and tutorials
        - Helping with problem-solving
        - Engaging in casual conversation
        - Offering creative assistance
        
        Always be polite, accurate, and helpful in your responses."""
    )
    
    logger.info("Basic chatbot agent created successfully")
    return agent


def create_specialized_agent(specialty: str, instructions: str) -> Agent:
    """
    Create a specialized agent for specific tasks.
    
    Args:
        specialty: The specialty name for the agent
        instructions: Custom instructions for the specialized agent
        
    Returns:
        Agent: Configured specialized AI agent
    """
    agent = Agent(
        model=model,
        name=f"AI {specialty} Specialist",
        instructions=instructions
    )
    
    logger.info(f"Specialized {specialty} agent created successfully")
    return agent


class ChatbotService:
    """
    Service class to manage chatbot interactions and provide API-ready methods
    """
    
    def __init__(self, agent: Agent):
        self.agent = agent
        self.runner = Runner()
        logger.info("ChatbotService initialized")
    
    async def chat(self, message: str, run_config: Optional[RunConfig] = None) -> str:
        """
        Process a single chat message and return response
        
        Args:
            message: User input message
            run_config: Optional run configuration
            
        Returns:
            str: Agent's response message
        """
        try:
            if run_config is None:
                run_config = RunConfig()
            
            # Run the agent with the user message
            result = await self.runner.run(
                starting_agent=self.agent,
                input=message,
                run_config=run_config
            )
            
            return result.final_output
            
        except Exception as e:
            logger.error(f"Error in chat method: {str(e)}")
            return f"I apologize, but I encountered an error processing your request: {str(e)}"
    
    async def chat_stream(self, message: str, run_config: Optional[RunConfig] = None):
        """
        Process a chat message with streaming response (for real-time UI updates)
        
        Args:
            message: User input message
            run_config: Optional run configuration
            
        Yields:
            str: Chunks of the agent's response
        """
        try:
            if run_config is None:
                run_config = RunConfig()
            
            # This would need to be implemented based on the agents framework streaming capabilities
            # For now, we'll return the full response
            response = await self.chat(message, run_config)
            yield response
            
        except Exception as e:
            logger.error(f"Error in streaming chat: {str(e)}")
            yield f"Error: {str(e)}"
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the current agent"""
        return {
            "name": self.agent.name,
            "model": "gemini-2.5-flash",
            "instructions": self.agent.instructions
        }


async def test_chatbot():
    """
    Test function to verify chatbot functionality
    """
    print("🚀 Initializing AI Chatbot...")
    
    try:
        # Create the chatbot agent
        agent = create_basic_chatbot_agent()
        chatbot_service = ChatbotService(agent)
        
        print("✅ Chatbot initialized successfully!")
        print(f"🤖 Agent Info: {chatbot_service.get_agent_info()}")
        
        # Test with a simple message
        test_message = "Hello! Can you tell me a bit about yourself?"
        print(f"\n🧪 Testing with message: '{test_message}'")
        
        response = await chatbot_service.chat(test_message)
        print(f"🤖 Response: {response}")
        
        return chatbot_service
        
    except Exception as e:
        logger.error(f"Error testing chatbot: {str(e)}")
        print(f"❌ Test failed: {e}")
        raise


async def interactive_chat():
    """
    Interactive chat session for testing the chatbot
    """
    print("🚀 Starting Interactive AI Chatbot...")
    
    try:
        # Initialize chatbot
        agent = create_basic_chatbot_agent()
        chatbot_service = ChatbotService(agent)
        
        print("✅ Chatbot ready!")
        print("💡 Type your messages (type 'quit', 'exit', or 'q' to exit)")
        
        # Interactive loop
        while True:
            user_input = input("\nYou: ").strip()
            
            # Exit conditions
            if user_input.lower() in ["quit", "exit", "q"]:
                print("\n👋 Goodbye!")
                break
            if not user_input:
                continue
            
            print("💭 AI thinking...")
            
            try:
                response = await chatbot_service.chat(user_input)
                print(f"🤖 AI Assistant: {response}")
                
            except Exception as e:
                print(f"❌ Error: {e}")
                
    except Exception as e:
        print(f"❌ Error initializing chatbot: {e}")
        return


# Entry point — run async main loop
if __name__ == "__main__":
    print("Choose mode:")
    print("1. Test chatbot functionality")
    print("2. Interactive chat session")
    
    choice = input("Enter choice (1-2): ").strip()
    
    if choice == "1":
        asyncio.run(test_chatbot())
    elif choice == "2":
        asyncio.run(interactive_chat())
    else:
        print("Invalid choice. Running test mode...")
        asyncio.run(test_chatbot())