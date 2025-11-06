"""
Quick test to verify OpenAI API key is valid.
"""
import os
import sys
from pathlib import Path
from dotenv import load_dotenv
from openai import OpenAI

# Load environment variables from parent directory
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

api_key = os.getenv("OPENAI_API_KEY")

print(f"Testing OpenAI API key: {api_key[:20]}...{api_key[-4:]}")
print()

try:
    client = OpenAI(api_key=api_key)
    
    # Test 1: Embeddings
    print("Test 1: Testing embeddings...")
    response = client.embeddings.create(
        input="Hello, world!",
        model="text-embedding-3-small"
    )
    print(f"✓ Embeddings work! Dimension: {len(response.data[0].embedding)}")
    print()
    
    # Test 2: Chat completions
    print("Test 2: Testing chat completions...")
    response = client.chat.completions.create(
        model="gpt-4-turbo-preview",
        messages=[
            {"role": "user", "content": "Say 'Hello!'"}
        ],
        max_tokens=10
    )
    print(f"✓ Chat completions work! Response: {response.choices[0].message.content}")
    print()
    
    print("=" * 60)
    print("✅ All tests passed! Your OpenAI API key is valid.")
    print("=" * 60)
    
except Exception as e:
    print(f"❌ Error: {e}")
    print()
    print("Your API key may be:")
    print("  1. Invalid or expired")
    print("  2. Not have sufficient credits")
    print("  3. Not have access to the required models")
    print()
    print("Please check:")
    print("  - https://platform.openai.com/api-keys")
    print("  - https://platform.openai.com/usage")
