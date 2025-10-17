# Quick Start Guide

Get the QA AI Agent system up and running in 5 minutes!

## Step 1: Start Backend (Terminal 1)

```bash
cd backend

# Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Start FastAPI server
uvicorn app.main:app --reload --port 8000
```

**Expected Output**:
```
INFO:     Uvicorn running on http://127.0.0.1:8000
INFO:     Application startup complete.
```

**Verify**: Open http://localhost:8000/docs in browser

## Step 2: Start Frontend (Terminal 2)

```bash
cd frontend

# Install dependencies (first time only)
npm install

# Start React development server
npm start
```

**Expected Output**:
```
Compiled successfully!
You can now view qa-ai-agent-frontend in the browser.
Local: http://localhost:3000
```

**Auto-opens**: Browser should open to http://localhost:3000

## Step 3: Run Your First Test

1. **Configure Application** (left panel):
   - Application Name: "My Test App"
   - Application Type: Web App
   - Test URL: https://example.com

2. **Set Scope** (left panel):
   - Scope: "Test login and navigation"
   - Select test types: Functional Testing, Regression Testing

3. **Configure Agents** (bottom panel):
   - Keep default settings for now

4. **Execute**:
   - Click the green "Start Agent Run" button
   - Watch the agents work in sequence
   - Monitor real-time logs in the Event Log panel

5. **Results**:
   - Each agent will complete with a green status
   - Final report will appear at the bottom
   - Check event logs for detailed trace

## What's Happening?

The system runs 5 agents in sequence:

1. **Perception Agent** → Analyzes your requirements (simulated)
2. **Planner Agent** → Creates structured test plan via `/api/planner`
3. **Generator Agent** → Generates test scripts via `/api/generator`
4. **Execution Agent** → Runs tests (simulated)
5. **Healer Agent** → Analyzes results and fixes issues via `/api/healer`

## Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (needs 3.9+)
- Try: `pip install --upgrade pip`
- Check port 8000 is free: `lsof -i :8000`

### Frontend won't start
- Check Node version: `node --version` (needs 16+)
- Delete node_modules and reinstall: `rm -rf node_modules && npm install`
- Check port 3000 is free: `lsof -i :3000`

### Agents fail to execute
- Verify backend is running: http://localhost:8000/health
- Check browser console for errors (F12)
- Verify CORS is enabled in backend/app/main.py

### Connection errors
- Ensure both frontend AND backend are running
- Frontend proxy is configured for http://localhost:8000
- Check firewall settings

## Next Steps

- Review the main [README.md](./README.md) for architecture details
- Explore API documentation at http://localhost:8000/docs
- Check [backend/README.md](./backend/README.md) for agent implementation details
- Modify agent logic in `backend/app/routers/` to integrate real AI models

## Tips

- Keep both terminals open while working
- Backend auto-reloads on file changes (--reload flag)
- Frontend auto-reloads on file changes
- Use browser DevTools (F12) to inspect API calls
- Check backend terminal for API request logs

Enjoy building with the QA AI Agent system!
