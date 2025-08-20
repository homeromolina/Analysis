"""
Streamlit app for Agno AI Agents learning example
"""

import streamlit as st
import json
from datetime import datetime
from agno_agents_example import AgnoAgentsExample
from config import Config

def main():
    st.set_page_config(
        page_title="Agno AI Agents Learning Example",
        page_icon="🤖",
        layout="wide"
    )
    
    st.title("🤖 Agno AI Agents Learning Example")
    st.subheader("Learn how AI agents work together to accomplish complex tasks")
    
    # About section
    with st.expander("📚 About This Example", expanded=True):
        st.markdown("""
        This example demonstrates how **Agno AI Agents** work together:
        
        - 🔍 **Web Content Analyzer**: Analyzes website content
        - 📊 **Content Insights Specialist**: Extracts deeper insights  
        - 📝 **Report Writer**: Creates comprehensive reports
        - 🎯 **Workflow Manager**: Manages everything
        
        **How it works:**
        1. Enter a URL to analyze
        2. Watch the agents work together
        3. See the final results and insights
        
        **Note:** This version uses the Agno framework with direct Gemini API integration.
        """)
    
    # Configuration display
    with st.expander("⚙️ Configuration"):
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Model", "gemini-1.5-flash")
        with col2:
            st.metric("Temperature", Config.AGENT_TEMPERATURE)
        with col3:
            st.metric("Verbose", Config.AGENT_VERBOSE)
    
    # Main content area
    st.markdown("### 🌐 Content Analysis with Agno AI Agents")
    
    # URL input
    url_input = st.text_input(
        "Enter a URL to analyze:",
        placeholder="https://example.com",
        help="Enter any website URL you want the AI agents to analyze"
    )
    
    # Example URLs
    st.markdown("**Try these example URLs:**")
    example_urls = [
        "https://www.apple.com",
        "https://news.ycombinator.com", 
        "https://github.com",
        "https://www.wikipedia.org"
    ]
    
    cols = st.columns(len(example_urls))
    for i, example_url in enumerate(example_urls):
        with cols[i]:
            if st.button(f"📱 {example_url.split('//')[1].split('.')[1].title()}", key=f"example_{i}"):
                url_input = example_url
                st.rerun()
    
    # Analysis button and results
    if st.button("🚀 Analyze with Agno Agents", type="primary", disabled=not url_input):
        if url_input:
            try:
                # Create progress indicators
                progress_bar = st.progress(0)
                status_text = st.empty()
                
                status_text.text("🚀 Initializing Agno AI Agents...")
                progress_bar.progress(10)
                
                # Initialize the Agno agents
                agno_example = AgnoAgentsExample()
                
                status_text.text("🤖 Running AI agent workflow...")
                progress_bar.progress(30)
                
                # Run the analysis
                result = agno_example.analyze_url(url_input)
                progress_bar.progress(100)
                status_text.text("✅ Analysis completed!")
                
                # Store results in session state
                st.session_state.last_result = result
                st.session_state.last_analysis_time = datetime.now()
                
                # Clear progress indicators
                progress_bar.empty()
                status_text.empty()
                
                st.success("🎉 Agno AI Agents workflow completed successfully!")
                
            except Exception as e:
                st.error(f"❌ Error running Agno workflow: {str(e)}")
                st.session_state.last_result = None
    
    # Display results if available
    if hasattr(st.session_state, 'last_result') and st.session_state.last_result:
        result = st.session_state.last_result
        
        if result.get('workflow_completed', False):
            # Quick stats
            st.markdown("### 📊 Quick Stats")
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("Status", "✅ Complete")
            with col2:
                st.metric("Agents Used", len(result.get('agents_used', [])))
            with col3:
                st.metric("URL", result.get('url', 'N/A')[:20] + "..." if len(result.get('url', '')) > 20 else result.get('url', 'N/A'))
            with col4:
                if hasattr(st.session_state, 'last_analysis_time'):
                    st.metric("Completed", st.session_state.last_analysis_time.strftime("%Y-%m-%d %H:%M:%S"))
            
            # Results tabs
            st.markdown("### 📋 Workflow Results")
            
            tab1, tab2, tab3, tab4 = st.tabs(["🎯 Summary", "📊 Analysis", "🤖 Agent Work", "📝 Full Report"])
            
            with tab1:
                st.markdown("#### Content Analysis")
                if 'coordination' in result:
                    st.markdown(result['coordination'])
                else:
                    st.info("Coordination summary not available")
            
            with tab2:
                st.markdown("#### Initial Analysis")
                if 'analysis' in result:
                    st.markdown(result['analysis'])
                else:
                    st.info("Initial analysis not available")
            
            with tab3:
                st.markdown("#### Agent Insights")
                if 'insights' in result:
                    st.markdown(result['insights'])
                else:
                    st.info("Agent insights not available")
            
            with tab4:
                st.markdown("#### Comprehensive Report")
                if 'report' in result:
                    st.markdown(result['report'])
                else:
                    st.info("Full report not available")
                    
                # Raw data (collapsible)
                with st.expander("🔍 Raw Data"):
                    st.json(result)
        
        else:
            st.error("❌ Workflow failed to complete")
            if 'error' in result:
                st.error(f"Error: {result['error']}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    📊 **Quick Stats**
    - Built with ❤️ using **Agno (phidata)**, **Streamlit**, and **Google Gemini**
    - This is a learning example to understand how AI agents work together
    - **Agno framework** provides simple, direct LLM integration
    """)

if __name__ == "__main__":
    main()
