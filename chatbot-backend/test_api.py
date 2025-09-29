#!/usr/bin/env python3
"""
Test script for AI Chatbot API
"""

import asyncio
import httpx
import json


async def test_api():
    """Test the chatbot API endpoints"""
    base_url = "http://localhost:8000"
    
    async with httpx.AsyncClient() as client:
        print("🧪 Testing AI Chatbot API...")
        
        # Test root endpoint
        print("\n1. Testing root endpoint...")
        try:
            response = await client.get(f"{base_url}/")
            print(f"✅ Status: {response.status_code}")
            print(f"📄 Response: {response.json()}")
        except Exception as e:
            print(f"❌ Error: {e}")
            return
        
        # Test health endpoint
        print("\n2. Testing health endpoint...")
        try:
            response = await client.get(f"{base_url}/health")
            print(f"✅ Status: {response.status_code}")
            print(f"🏥 Health: {response.json()}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test agent info endpoint
        print("\n3. Testing agent info endpoint...")
        try:
            response = await client.get(f"{base_url}/agent-info")
            print(f"✅ Status: {response.status_code}")
            print(f"🤖 Agent Info: {response.json()}")
        except Exception as e:
            print(f"❌ Error: {e}")
        
        # Test chat endpoint
        print("\n4. Testing chat endpoint...")
        try:
            chat_data = {
                "message": "Hello! What is your name?",
                "agent_type": "basic"
            }
            
            response = await client.post(
                f"{base_url}/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"✅ Status: {response.status_code}")
            result = response.json()
            print(f"💬 Chat Response: {result.get('response', 'No response')}")
            print(f"🏷️  Agent: {result.get('agent_name', 'Unknown')}")
            print(f"🧠 Model: {result.get('model', 'Unknown')}")
            
        except Exception as e:
            print(f"❌ Chat Error: {e}")
        
        # Test another chat message
        print("\n5. Testing follow-up chat...")
        try:
            chat_data = {
                "message": "Can you remember what I just asked you?",
                "agent_type": "basic"
            }
            
            response = await client.post(
                f"{base_url}/chat",
                json=chat_data,
                headers={"Content-Type": "application/json"}
            )
            
            print(f"✅ Status: {response.status_code}")
            result = response.json()
            print(f"💬 Follow-up Response: {result.get('response', 'No response')}")
            
        except Exception as e:
            print(f"❌ Follow-up Error: {e}")
        
        print("\n🎉 API testing completed!")


if __name__ == "__main__":
    asyncio.run(test_api())