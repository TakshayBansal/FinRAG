"""
Test script to verify the filtered parser works correctly.
"""
import sys
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent.parent / "src"))

from finrag.utils.filtered_parser import FilteredDocumentParser

def test_filtered_parser():
    """Test the filtered parser with sample data."""
    
    print("="*60)
    print("Testing FilteredDocumentParser")
    print("="*60)
    
    # Initialize parser
    parser = FilteredDocumentParser()
    
    # Test 1: Generate system prompt
    print("\n1. Testing system prompt generation...")
    prompt = parser.generate_system_prompt()
    print(f"✓ Generated prompt ({len(prompt)} chars)")
    print("\nPrompt preview:")
    print(prompt[:200] + "...")
    
    # Test 2: Consolidate sections (with sample data)
    print("\n2. Testing section consolidation...")
    
    sample_text = """
1. **Board of Directors Changes**
- New director appointed: John Doe
- Jane Smith resigned from the board

2. **Projects and Major Initiatives**
- Launched new AI platform
- Not found in the page

3. **AI and Digital Initiatives**
- Implemented machine learning models
- Cloud infrastructure upgraded

4. **Government Programs**
Not found in the page

5. **Investments and Capital Expenditure**
- $500M invested in R&D
- New data center construction started

6. **Corporate Actions**
- Not found in the page

7. **Employee Information**
- Total employees: 50,000
- Employee growth: 15% YoY

8. **Operational Metrics**
- Revenue: $10B
- Operating margin: 25%

9. **Corporate Governance**
- New compliance policies implemented
"""
    
    consolidated = parser.consolidate_sections(sample_text)
    
    print(f"✓ Consolidated {len(consolidated)} sections with data")
    print("\nSections found:")
    for section, items in consolidated.items():
        print(f"  • {section}: {len(items)} items")
    
    # Test 3: Convert to different formats
    print("\n3. Testing format conversions...")
    
    text_output = parser.convert_to_text(consolidated)
    print(f"✓ Text format: {len(text_output)} chars")
    
    md_output = parser.convert_to_markdown(consolidated)
    print(f"✓ Markdown format: {len(md_output)} chars")
    
    json_output = parser.convert_to_json(consolidated)
    print(f"✓ JSON format: {len(json_output)} chars")
    
    # Test 4: Get statistics
    print("\n4. Testing statistics...")
    stats = parser.get_statistics(consolidated)
    print(f"✓ Statistics generated")
    print(f"  • Total sections: {stats['total_sections']}")
    print(f"  • Sections with data: {stats['sections_with_data']}")
    print(f"  • Total items: {stats['total_items']}")
    print(f"  • Coverage: {stats['coverage']:.1f}%")
    
    print("\n" + "="*60)
    print("✅ All tests passed!")
    print("="*60)
    
    # Show sample output
    print("\nSample text output:")
    print("-"*60)
    print(text_output[:500] + "...")

if __name__ == "__main__":
    test_filtered_parser()
