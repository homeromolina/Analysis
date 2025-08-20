"""
Agno AI Agents Example for Learning
A simplified version using Agno framework that demonstrates the core concepts
"""

from phi.assistant import Assistant
from phi.llm.google import Gemini
from config import Config
from typing import Dict, Any
import json
import os

class AgnoAgentsExample:
    """
    Agno AI Agents learning example
    
    This example demonstrates:
    1. How to create agents with different roles using Agno
    2. How to define tasks for each agent
    3. How agents work together in a workflow
    4. Basic agent coordination
    """
    
    def __init__(self):
        """Initialize the Agno agents example"""
        
        if not Config.USE_GOOGLE_CLI_AUTH:
            if not Config.GEMINI_API_KEY:
                raise ValueError("GEMINI_API_KEY is required when not using CLI authentication")
        
        # Create the Gemini model instance
        self.model = Gemini(
            api_key=Config.GEMINI_API_KEY,
            model="gemini-1.5-flash"
        )
        
        # Create the agents
        self._create_agents()
    
    def _create_agents(self):
        """Create the Agno agents with their roles and goals"""
        
        # Web Content Analyzer Agent
        self.analyzer_agent = Assistant(
            name="Web Content Analyzer",
            role="Analyze web content and provide insights about websites",
            llm=self.model,
            instructions=[
                "You are an expert web analyst who can understand website content.",
                "Identify key information and provide valuable insights about web pages.",
                "You're excellent at summarizing content and identifying important details.",
                "Focus on understanding the type of website, its purpose, and main content."
            ],
            show_tool_calls=Config.AGENT_VERBOSE,
            markdown=True
        )
        
        # Content Insights Specialist Agent
        self.insights_agent = Assistant(
            name="Content Insights Specialist", 
            role="Extract meaningful insights and categorize web content",
            llm=self.model,
            instructions=[
                "You are a content analysis expert who can quickly understand web content.",
                "Identify key themes and provide meaningful insights.", 
                "You excel at categorization and finding patterns in information.",
                "Build upon previous analysis to provide deeper insights."
            ],
            show_tool_calls=Config.AGENT_VERBOSE,
            markdown=True
        )
        
        # Report Writer Agent
        self.reporter_agent = Assistant(
            name="Report Writer",
            role="Create clear, informative reports based on analyzed content",
            llm=self.model,
            instructions=[
                "You are a skilled report writer who takes complex information and presents it clearly.",
                "You understand how to structure reports and highlight key findings.",
                "Make information accessible to different audiences.",
                "Create comprehensive, well-organized reports."
            ],
            show_tool_calls=Config.AGENT_VERBOSE,
            markdown=True
        )
        
        # Workflow Manager Agent
        self.manager_agent = Assistant(
            name="Workflow Manager",
            role="Coordinate the entire content analysis workflow efficiently", 
            llm=self.model,
            instructions=[
                "You are a senior project manager who excels at coordinating workflows.",
                "You understand how to break down tasks and ensure quality standards.",
                "You're excellent at communication and keeping everyone on track.",
                "Provide final summaries and highlight key learnings from workflows."
            ],
            show_tool_calls=Config.AGENT_VERBOSE,
            markdown=True
        )
    
    def analyze_url(self, url: str) -> Dict[str, Any]:
        """
        Main method to analyze a URL using the agent workflow
        
        Args:
            url: The URL to analyze
            
        Returns:
            Complete analysis results
        """
        print(f"🚀 Starting Agno AI Agents workflow for URL: {url}")
        print("=" * 60)
        
        try:
            # Step 1: Initial content analysis
            print("🔍 Step 1: Web Content Analysis...")
            analysis_prompt = f"""
            Analyze the following URL and provide insights about its content:
            URL: {url}
            
            Your goal is to:
            1. Understand what type of website this is
            2. Identify the main purpose and content
            3. Note any key features or important information
            4. Provide a summary of what you found
            
            Think about what kind of website this is (news, company, blog, etc.)
            and what the main content seems to be about.
            """
            
            analysis_response = self.analyzer_agent.run(analysis_prompt)
            analysis_content = "".join([chunk for chunk in analysis_response])
            print(f"✅ Analysis completed: {len(analysis_content)} characters")
            
            # Step 2: Extract deeper insights
            print("📊 Step 2: Content Insights Extraction...")
            insights_prompt = f"""
            Take the following analysis and extract deeper insights:
            URL: {url}
            
            Previous Analysis:
            {analysis_content}
            
            Your goal is to:
            1. Categorize the content type (news, blog, e-commerce, etc.)
            2. Identify key themes and topics
            3. Suggest what users might be looking for on this site
            4. Provide recommendations or observations
            
            Build upon the previous analysis to provide deeper insights.
            """
            
            insights_response = self.insights_agent.run(insights_prompt)
            insights_content = "".join([chunk for chunk in insights_response])
            print(f"✅ Insights completed: {len(insights_content)} characters")
            
            # Step 3: Create comprehensive report
            print("📝 Step 3: Report Generation...")
            report_prompt = f"""
            Create a comprehensive report based on the analysis and insights:
            URL: {url}
            
            Initial Analysis:
            {analysis_content}
            
            Deeper Insights:
            {insights_content}
            
            Your goal is to:
            1. Summarize the key findings from both previous analyses
            2. Present the information in an organized, readable format
            3. Highlight the most important insights
            4. Make the report professional and informative
            
            Combine the analysis and insights into a clear, comprehensive report.
            """
            
            report_response = self.reporter_agent.run(report_prompt)
            report_content = "".join([chunk for chunk in report_response])
            print(f"✅ Report completed: {len(report_content)} characters")
            
            # Step 4: Final coordination and summary
            print("🎯 Step 4: Workflow Coordination...")
            coordination_prompt = f"""
            Coordinate and summarize the entire workflow for analyzing: {url}
            
            Web Content Analysis:
            {analysis_content}
            
            Content Insights:
            {insights_content}
            
            Final Report:
            {report_content}
            
            Your responsibilities:
            1. Review all previous work for completeness
            2. Provide a final summary of the entire process
            3. Highlight the key learnings from this workflow
            4. Ensure the output meets quality standards
            
            Provide a final coordination summary and overall workflow results.
            """
            
            coordination_response = self.manager_agent.run(coordination_prompt)
            coordination_content = "".join([chunk for chunk in coordination_response])
            print(f"✅ Coordination completed: {len(coordination_content)} characters")
            
            print("=" * 60)
            print("✅ Agno AI Agents workflow completed!")
            
            return {
                'url': url,
                'analysis': analysis_content,
                'insights': insights_content, 
                'report': report_content,
                'coordination': coordination_content,
                'workflow_completed': True,
                'agents_used': [
                    'Web Content Analyzer',
                    'Content Insights Specialist',
                    'Report Writer', 
                    'Workflow Manager'
                ],
                'framework': 'Agno (phidata)'
            }
            
        except Exception as e:
            print(f"❌ Error in Agno workflow: {str(e)}")
            return {
                'url': url,
                'error': str(e),
                'workflow_completed': False,
                'framework': 'Agno (phidata)'
            }
    
    def get_agent_info(self) -> Dict[str, Any]:
        """Get information about the agents for educational purposes"""
        return {
            'framework': 'Agno (phidata)',
            'model': 'Gemini 1.5 Flash',
            'agents': {
                'analyzer_agent': {
                    'name': 'Web Content Analyzer',
                    'role': 'Analyze web content and provide insights',
                    'capabilities': [
                        'Website content analysis',
                        'Purpose identification', 
                        'Content summarization',
                        'Key information extraction'
                    ]
                },
                'insights_agent': {
                    'name': 'Content Insights Specialist',
                    'role': 'Extract deeper insights from content',
                    'capabilities': [
                        'Content categorization',
                        'Theme identification',
                        'User intent analysis',
                        'Recommendation generation'
                    ]
                },
                'reporter_agent': {
                    'name': 'Report Writer', 
                    'role': 'Create clear, informative reports',
                    'capabilities': [
                        'Information synthesis',
                        'Report structuring',
                        'Key finding identification',
                        'Professional presentation'
                    ]
                },
                'manager_agent': {
                    'name': 'Workflow Manager',
                    'role': 'Coordinate the entire workflow',
                    'capabilities': [
                        'Task coordination',
                        'Quality assurance',
                        'Workflow management',
                        'Final summary creation'
                    ]
                }
            },
            'workflow_steps': [
                '1. Content Analysis (Web Content Analyzer Agent)',
                '2. Insights Generation (Content Insights Specialist Agent)',
                '3. Report Creation (Report Writer Agent)',
                '4. Workflow Coordination (Workflow Manager Agent)'
            ],
            'advantages': [
                'Direct Gemini API integration',
                'Simple agent configuration',
                'Clear workflow coordination',
                'No complex LLM provider setup'
            ]
        }
