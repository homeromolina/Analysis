# 🤖 Agno AI Agents Learning Example

A simple, working example of AI agents working together using the **Agno framework** (phidata) with Google Gemini API integration.

## 🎯 What This Example Demonstrates

This project shows how to create AI agents that work together to accomplish complex tasks:

1. **🔍 Web Content Analyzer**: Analyzes website content and purpose
2. **📊 Content Insights Specialist**: Extracts deeper insights and themes  
3. **📝 Report Writer**: Creates comprehensive analysis reports
4. **🎯 Workflow Manager**: Coordinates the entire workflow

## 🚀 Quick Start

### 1. Install Dependencies
```bash
pip install -r requirements.txt
```

### 2. Configure Environment
Copy `env.example` to `.env` and add your Gemini API key:
```bash
cp env.example .env
# Edit .env and add: GEMINI_API_KEY=your_api_key_here
```

### 3. Test Setup
```bash
python test_agno_setup.py
```

### 4. Run the Example
```bash
# Command line demo
python agno_agents_example.py

# Streamlit web interface
streamlit run agno_streamlit_app.py
```

## 🏗️ Architecture

### Why Agno Instead of CrewAI?

- **✅ Direct Gemini API Integration**: No complex LLM provider setup
- **✅ Simple Configuration**: Clean, straightforward agent definitions
- **✅ Reliable**: No internal LLM compatibility issues
- **✅ Fast**: Direct API calls without middleware layers

### Agent Workflow

```
URL Input → Web Content Analyzer → Content Insights Specialist → Report Writer → Workflow Manager → Final Results
```

## 📁 Project Structure

```
crewai_learning_example/
├── agno_agents_example.py      # Main Agno agents implementation
├── agno_streamlit_app.py       # Streamlit web interface
├── test_agno_setup.py          # Setup verification script
├── config.py                   # Configuration management
├── requirements.txt            # Python dependencies
├── .env                        # Environment variables (create from .env.example)
└── README.md                   # This file
```

## 🔧 Configuration

The `.env` file contains:
- `GEMINI_API_KEY`: Your Google Gemini API key
- `AGENT_TEMPERATURE`: AI creativity level (0.0-1.0)
- `AGENT_VERBOSE`: Enable detailed logging
- `SCRAPING_TIMEOUT`: Web request timeout
- `MAX_CONTENT_LENGTH`: Maximum content length to process

## 🎓 Key Concepts

### AI Agents
- **Role-based**: Each agent has a specific role and expertise
- **Goal-oriented**: Clear objectives for each task
- **Collaborative**: Agents work together in a coordinated workflow

### Workflow Management
- **Sequential Processing**: Tasks flow from one agent to the next
- **Context Preservation**: Each agent builds upon previous work
- **Quality Assurance**: Final coordination ensures output quality

## 🚀 Running the Example

### Command Line Demo
```bash
python agno_agents_example.py
```

### Web Interface
```bash
streamlit run agno_streamlit_app.py
```

## 🚀 GitHub Setup

### 1. Initialize Git Repository
```bash
git init
git add .
git commit -m "Initial commit: Agno AI Agents Learning Example"
```

### 2. Create GitHub Repository
- Go to GitHub and create a new repository
- Don't initialize with README, .gitignore, or license (we already have these)

### 3. Push to GitHub
```bash
git remote add origin https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
git branch -M main
git push -u origin main
```

### 4. Verify .gitignore is Working
The `.gitignore` file ensures these sensitive files are NOT uploaded:
- ✅ `.env` (your API keys)
- ✅ `venv/` (virtual environment)
- ✅ `__pycache__/` (Python cache)
- ✅ `memory_db/` (Chroma database)
- ✅ `*.db` (SQLite databases)

### 5. Share with Others
Others can clone and set up your project:
```bash
git clone https://github.com/YOUR_USERNAME/YOUR_REPO_NAME.git
cd YOUR_REPO_NAME
cp env.example .env
# Edit .env with their own API keys
pip install -r requirements.txt
python test_agno_setup.py
```

Then open your browser to the displayed URL (usually http://localhost:8501)

## 🔍 Example Usage

1. **Enter a URL**: Any website you want to analyze
2. **Watch the Workflow**: See each agent process the content
3. **Review Results**: Get comprehensive analysis and insights

### Sample URLs to Try
- https://www.apple.com
- https://news.ycombinator.com
- https://github.com
- https://www.wikipedia.org

## 🛠️ Troubleshooting

### Common Issues

1. **API Key Error**: Ensure `GEMINI_API_KEY` is set in `.env`
2. **Import Errors**: Run `pip install -r requirements.txt`
3. **Port Conflicts**: Use `--server.port 8502` for different port

### Getting Help

- Check the test script: `python test_agno_setup.py`
- Verify configuration: Check `.env` file
- Review logs: Enable verbose mode in configuration

## 📚 Learning Resources

- [Agno Framework Documentation](https://docs.phidata.com/)
- [Google Gemini API](https://ai.google.dev/)
- [Streamlit Documentation](https://docs.streamlit.io/)

## 🤝 Contributing

This is a learning example. Feel free to:
- Modify agent roles and goals
- Add new workflow steps
- Experiment with different prompts
- Share improvements

## 📄 License

This project is for educational purposes. Use responsibly and in accordance with API terms of service.

---

**Built with ❤️ using Agno (phidata), Streamlit, and Google Gemini**
