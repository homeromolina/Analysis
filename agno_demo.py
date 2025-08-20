#!/usr/bin/env python3
"""
Simple demo script for Agno AI Agents
Run this to see the agents in action
"""

from agno_agents_example import AgnoAgentsExample
import sys

def main():
    print("🚀 Agno AI Agents Demo")
    print("=" * 40)
    
    # Example URL to analyze
    example_url = "https://www.apple.com"
    
    print(f"📱 Analyzing: {example_url}")
    print("🤖 Starting AI agent workflow...")
    print()
    
    try:
        # Create and run the Agno agents
        agno_example = AgnoAgentsExample()
        
        # Run the analysis
        result = agno_example.analyze_url(example_url)
        
        if result.get('workflow_completed', False):
            print("\n🎉 Workflow completed successfully!")
            print("\n📊 Results Summary:")
            print(f"   URL: {result['url']}")
            print(f"   Agents used: {len(result['agents_used'])}")
            print(f"   Framework: {result['framework']}")
            
            print("\n🔍 Analysis Preview:")
            analysis = result.get('analysis', '')
            if analysis:
                print(f"   {analysis[:200]}...")
            
            print("\n📝 Report Preview:")
            report = result.get('report', '')
            if report:
                print(f"   {report[:200]}...")
                
        else:
            print(f"\n❌ Workflow failed: {result.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
        print("\n💡 Make sure you have:")
        print("   1. Set GEMINI_API_KEY in your .env file")
        print("   2. Installed all dependencies: pip install -r requirements.txt")
        print("   3. Run the test: python test_agno_setup.py")
        sys.exit(1)
    
    print("\n" + "=" * 40)
    print("🎓 This demonstrates how AI agents work together!")
    print("   Try running: streamlit run agno_streamlit_app.py")
    print("   For an interactive web interface")

if __name__ == "__main__":
    main()
