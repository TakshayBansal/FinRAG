"""
Test script to verify FinRAG installation and basic functionality.
Run this after installation to ensure everything is working.
"""
import sys
import os

def test_imports():
    """Test that all required packages are installed."""
    print("Testing imports...")
    
    required_packages = [
        ("openai", "OpenAI"),
        ("numpy", "NumPy"),
        ("sklearn", "scikit-learn"),
        ("umap", "umap-learn"),
        ("tiktoken", "tiktoken"),
        ("PyPDF2", "PyPDF2"),
        ("pandas", "pandas"),
    ]
    
    optional_packages = [
        ("llama_cloud_services", "LlamaParse (recommended for PDF parsing)"),
    ]
    
    failed = []
    for package, name in required_packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ✗ {name} - NOT FOUND")
            failed.append(name)
    
    if failed:
        print(f"\n❌ Missing packages: {', '.join(failed)}")
        print("Run: pip install -r requirements.txt")
        return False
    
    print("✅ All required packages installed\n")
    
    # Check optional packages
    print("Checking optional packages...")
    for package, name in optional_packages:
        try:
            __import__(package)
            print(f"  ✓ {name}")
        except ImportError:
            print(f"  ○ {name} - NOT FOUND (optional)")
    
    print()
    return True


def test_api_key():
    """Test that API keys are set."""
    print("Testing API keys...")
    
    # Check OpenAI API key (required)
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("  ✗ OPENAI_API_KEY not set (REQUIRED)")
        print("\n❌ Please set your OpenAI API key:")
        print("  Windows PowerShell: $env:OPENAI_API_KEY='your-key'")
        print("  Linux/Mac: export OPENAI_API_KEY='your-key'")
        return False
    
    print(f"  ✓ OPENAI_API_KEY found (length: {len(api_key)})")
    
    # Check LlamaParse API key (optional but recommended)
    llama_key = os.getenv("LLAMA_CLOUD_API_KEY")
    if llama_key:
        print(f"  ✓ LLAMA_CLOUD_API_KEY found (length: {len(llama_key)})")
    else:
        print("  ○ LLAMA_CLOUD_API_KEY not set (optional but recommended)")
        print("    LlamaParse provides better PDF parsing for financial docs")
        print("    Get key at: https://cloud.llamaindex.ai/")
    
    print("✅ Required API keys configured\n")
    return True


def test_basic_functionality():
    """Test basic FinRAG functionality."""
    print("Testing FinRAG components...")
    
    try:
        from config import FinRAGConfig
        print("  ✓ Config import")
        
        from base_models import BaseEmbeddingModel
        print("  ✓ Base models import")
        
        from models import OpenAIEmbeddingModel, FinancialChunker
        print("  ✓ Models import")
        
        from clustering import RAPTORClustering
        print("  ✓ Clustering import")
        
        from tree import RAPTORTree
        print("  ✓ Tree import")
        
        from retrieval import RAPTORRetriever
        print("  ✓ Retrieval import")
        
        from finrag import FinRAG
        print("  ✓ FinRAG import")
        
        print("✅ All components loaded\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n❌ Component loading failed")
        return False


def test_config():
    """Test configuration."""
    print("Testing configuration...")
    
    try:
        from config import FinRAGConfig
        
        # Test with environment variable
        config = FinRAGConfig()
        print(f"  ✓ Default config created")
        print(f"    - Chunk size: {config.chunk_size}")
        print(f"    - Tree depth: {config.tree_depth}")
        print(f"    - Top-k: {config.top_k}")
        
        print("✅ Configuration working\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n❌ Configuration failed")
        return False


def test_chunker():
    """Test the chunker."""
    print("Testing financial chunker...")
    
    try:
        from models import FinancialChunker
        
        chunker = FinancialChunker(chunk_size=100, chunk_overlap=10)
        
        sample_text = """
        Company XYZ reported revenue of $500M in Q4 2024, up 25% year-over-year.
        Net income was $125M, representing a 30% increase.
        The company's operating margin improved to 25%.
        """
        
        chunks = chunker.chunk_text(sample_text)
        print(f"  ✓ Created {len(chunks)} chunks")
        print(f"    - Sample chunk length: {len(chunks[0]['text'])} chars")
        
        print("✅ Chunker working\n")
        return True
        
    except Exception as e:
        print(f"  ✗ Error: {e}")
        print("\n❌ Chunker test failed")
        return False


def run_all_tests():
    """Run all tests."""
    print("="*60)
    print("FinRAG Installation Test")
    print("="*60)
    print()
    
    results = []
    
    # Test imports
    results.append(("Package imports", test_imports()))
    
    # Test API key
    results.append(("API key", test_api_key()))
    
    # Test components
    results.append(("Component loading", test_basic_functionality()))
    
    # Test config
    results.append(("Configuration", test_config()))
    
    # Test chunker
    results.append(("Chunker", test_chunker()))
    
    # Summary
    print("="*60)
    print("Test Summary")
    print("="*60)
    
    passed = sum(1 for _, result in results if result)
    total = len(results)
    
    for name, result in results:
        status = "✅ PASS" if result else "❌ FAIL"
        print(f"{name:20s} {status}")
    
    print()
    print(f"Results: {passed}/{total} tests passed")
    
    if passed == total:
        print("\n🎉 All tests passed! FinRAG is ready to use.")
        print("\nNext steps:")
        print("  1. Run: python example.py")
        print("  2. Or: python cli.py")
        print("  3. Or: python main.py")
    else:
        print("\n⚠️  Some tests failed. Please fix the issues above.")
    
    print()
    return passed == total


if __name__ == "__main__":
    try:
        success = run_all_tests()
        sys.exit(0 if success else 1)
    except KeyboardInterrupt:
        print("\n\nTest interrupted.")
        sys.exit(1)
    except Exception as e:
        print(f"\n\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
