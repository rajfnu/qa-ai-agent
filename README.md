# QA AI Agent - Multi-Agent QA Automation System

A sophisticated multi-agent system for automated QA testing, featuring three intelligent agents (Planner, Generator, and Healer) that work together to create, execute, and maintain test automation.

## Architecture Overview

This system implements three core AI agents (shown in blue boxes in the architecture diagram):

1. **Planner Agent (TestPlanerAgent)** - ReAct Agent that creates structured test plans based on BRD documents and requirements
2. **Generator Agent (TestGeneratorAgent)** - Code Agent that generates executable test scripts in Playwright/Selenium/Cypress
3. **Healer Agent (TestHealerAgent)** - Learning Agent that performs RCA and fixes test scripts when application changes occur

## Project Structure

```
qa-ai-agent/
├── frontend/              # React UI for agent control center
│   ├── public/
│   ├── src/
│   │   ├── App.js        # Main application component with agent orchestration
│   │   ├── index.js
│   │   └── index.css
│   └── package.json
├── backend/              # FastAPI backend with agent APIs
│   ├── app/
│   │   ├── routers/
│   │   │   ├── planner.py     # Planner Agent API
│   │   │   ├── generator.py   # Generator Agent API
│   │   │   └── healer.py      # Healer Agent API
│   │   ├── models.py          # Pydantic models
│   │   └── main.py            # FastAPI application
│   └── requirements.txt
└── README.md
```

## Prerequisites

### Frontend
- Node.js 16+ and npm
- Modern web browser

### Backend
- Python 3.9+
- pip

## Installation & Setup

### 1. Backend Setup

```bash
# Navigate to backend directory
cd backend

# Create virtual environment (recommended)
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
uvicorn app.main:app --reload --port 8000
```

The backend API will be available at `http://localhost:8000`
- API Documentation: `http://localhost:8000/docs`
- Health Check: `http://localhost:8000/health`

### 2. Frontend Setup

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies
npm install

# Install Tailwind CSS
npm install -D tailwindcss postcss autoprefixer
npx tailwindcss init

# Start the development server
npm start
```

The frontend UI will be available at `http://localhost:3000`

## Usage

1. **Start Backend**: Run the FastAPI server (port 8000)
2. **Start Frontend**: Run the React development server (port 3000)
3. **Open Browser**: Navigate to `http://localhost:3000`
4. **Configure Test Run**:
   - Enter application details (name, type, URL)
   - Upload/connect BRD documents
   - Define test scope
   - Select test types
   - Choose LLM models for agents
   - Select automation framework
5. **Execute**: Click "Start Agent Run" to launch the workflow
6. **Monitor**: Watch the cognitive pipeline status and event logs in real-time

## Agent Workflow

```
┌─────────────────┐
│ Perception      │ → Analyzes BRD documents and requirements
└────────┬────────┘
         ↓
┌─────────────────┐
│ Planner Agent   │ → Creates structured test plan with priorities
└────────┬────────┘
         ↓
┌─────────────────┐
│ Generator Agent │ → Generates executable test scripts
└────────┬────────┘
         ↓
┌─────────────────┐
│ Execution       │ → Runs tests in isolated environment
└────────┬────────┘
         ↓
┌─────────────────┐
│ Healer Agent    │ → Analyzes failures and self-heals scripts
└─────────────────┘
```

## API Endpoints

### Planner Agent
**POST** `/api/planner`
- Creates structured test plan from requirements
- Input: Application context, scope, test types
- Output: Detailed test plan with risk analysis

### Generator Agent
**POST** `/api/generator`
- Generates executable test scripts
- Input: Test plan, automation framework
- Output: Framework-specific test code

### Healer Agent
**POST** `/api/healer`
- Analyzes test failures and applies fixes
- Input: Test script, execution results
- Output: Fixed script or JIRA ticket for manual review

## Features

- **Multi-Agent Architecture**: Specialized agents for planning, generation, and healing
- **Framework Agnostic**: Supports Playwright, Selenium, and Cypress
- **Self-Healing**: Automatically fixes test scripts when UI changes
- **Risk Analysis**: Prioritizes test cases based on risk assessment
- **Real-time Monitoring**: Live event logs and agent status tracking
- **Model Selection**: Choose different LLMs for reasoning and code generation

## Technology Stack

### Frontend
- React 18
- Lucide React (icons)
- Axios (HTTP client)
- Tailwind CSS (styling)

### Backend
- FastAPI (Python web framework)
- Pydantic (data validation)
- Uvicorn (ASGI server)

## Development

### Backend Development
```bash
cd backend
source venv/bin/activate
uvicorn app.main:app --reload --port 8000
```

### Frontend Development
```bash
cd frontend
npm start
```

### API Documentation
Visit `http://localhost:8000/docs` for interactive Swagger documentation

## Next Steps

To integrate with real AI models and tools:

1. **Planner Agent**: Integrate LangChain/LangGraph for reasoning
2. **Generator Agent**: Connect to GPT-4/Claude for code generation
3. **Healer Agent**: Add Computer Vision for UI change detection
4. **MCP Integration**: Connect to Playwright MCP Server
5. **Database**: Add persistence for test plans and results
6. **Git Integration**: Auto-commit healed scripts
7. **JIRA Integration**: Create tickets for manual review
8. **CI/CD Integration**: Connect to build pipelines

## License

MIT

## Contributing

Contributions are welcome! Please feel free to submit a Pull Request.
