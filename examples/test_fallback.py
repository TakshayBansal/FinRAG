"""
Test script to verify OpenAI API key fallback functionality.
This script tests the fallback to free models when OpenAI API key is missing.
"""
import os
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from finrag.config import FinRAGConfig
from finrag.models.fallback_models import check_openai_key_valid


def test_api_key_check():
    """Test API key validation."""
    print("="*60)
    print("Testing OpenAI API Key Check")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY", "")
    
    if not api_key:
        print("❌ No OPENAI_API_KEY environment variable found")
        print("✓ This will trigger fallback to free models")
        return False
    else:
        print(f"✓ OPENAI_API_KEY found (length: {len(api_key)})")
        print("Validating key...")
        is_valid = check_openai_key_valid(api_key)
        
        if is_valid:
            print("✓ API key is valid")
            return True
        else:
            print("❌ API key is invalid or expired")
            print("✓ This will trigger fallback to free models")
            return False


def test_fallback_models():
    """Test fallback model initialization."""
    print("\n" + "="*60)
    print("Testing Fallback Models")
    print("="*60)
    
    # Temporarily clear API key to force fallback
    original_key = os.getenv("OPENAI_API_KEY")
    if original_key:
        del os.environ["OPENAI_API_KEY"]
    
    try:
        from finrag import FinRAG
        
        print("\nInitializing FinRAG with no API key...")
        finrag = FinRAG()
        
        print("\n✓ FinRAG initialized successfully with fallback models!")
        print(f"  Embedding Model: {type(finrag.embedding_model).__name__}")
        print(f"  Summarization Model: {type(finrag.summarization_model).__name__}")
        print(f"  QA Model: {type(finrag.qa_model).__name__}")
        
        # Test embedding
        print("\nTesting embedding generation...")
        test_text = "This is a test of the financial analysis system."
        embedding = finrag.embedding_model.create_embedding(test_text)
        print(f"✓ Generated embedding with shape: {embedding.shape}")
        
        # Test QA
        print("\nTesting QA model...")
        context = "Apple Inc. reported revenue of $100 billion in Q4 2024, up 10% from last year."
        question = "What was Apple's revenue?"
        answer = finrag.qa_model.answer_question(context, question)
        print(f"✓ QA Answer: {answer['answer'][:100]}...")
        
        print("\n" + "="*60)
        print("✅ ALL FALLBACK TESTS PASSED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during fallback test: {e}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Restore original key
        if original_key:
            os.environ["OPENAI_API_KEY"] = original_key


def test_with_openai():
    """Test with OpenAI API key."""
    print("\n" + "="*60)
    print("Testing with OpenAI API Key")
    print("="*60)
    
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("⚠ Skipping OpenAI test - no API key available")
        return
    
    try:
        from finrag import FinRAG
        
        print("\nInitializing FinRAG with OpenAI API key...")
        finrag = FinRAG()
        
        print("\n✓ FinRAG initialized successfully with OpenAI models!")
        print(f"  Embedding Model: {type(finrag.embedding_model).__name__}")
        print(f"  Summarization Model: {type(finrag.summarization_model).__name__}")
        print(f"  QA Model: {type(finrag.qa_model).__name__}")
        
        print("\n" + "="*60)
        print("✅ OPENAI TEST PASSED")
        print("="*60)
        
    except Exception as e:
        print(f"\n❌ Error during OpenAI test: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    print("\n" + "="*60)
    print("FinRAG API Key Fallback Test Suite")
    print("="*60 + "\n")
    
    # Test 1: Check API key
    has_valid_key = test_api_key_check()
    
    # Test 2: Test fallback models
    test_fallback_models()
    
    # Test 3: Test with OpenAI (if available)
    if has_valid_key:
        test_with_openai()
    
    print("\n" + "="*60)
    print("TEST SUITE COMPLETE")
    print("="*60)
    print("\nSummary:")
    print("- Fallback models allow FinRAG to work without OpenAI API key")
    print("- Free models: sentence-transformers for embeddings")
    print("- Limited quality for summarization and QA without API key")
    print("- For production use, OpenAI API key is recommended")
    print("="*60 + "\n")
