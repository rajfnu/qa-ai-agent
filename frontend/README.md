# QA AI Agent - Frontend

React-based control center for the Multi-Agent QA Automation System.

## Quick Start

```bash
# Install dependencies
npm install

# Start development server
npm start
```

The app will open at `http://localhost:3000`

## Features

- **Agent Control Panel**: Configure and monitor all 3 AI agents
- **Real-time Status**: Live updates on agent execution
- **Event Logs**: Detailed trace of all agent activities
- **Configuration**: Customize test scope, models, and frameworks
- **Responsive Design**: Works on desktop and mobile

## Environment Setup

The frontend expects the backend API to be running at `http://localhost:8000`.

This is configured via the `proxy` setting in `package.json`.

## Available Scripts

- `npm start` - Run development server
- `npm build` - Build for production
- `npm test` - Run tests
- `npm eject` - Eject from Create React App (irreversible)

## Key Components

### App.js
Main application component containing:
- Agent workflow orchestration
- State management
- API integration
- UI rendering

### Agent Workflow
The UI manages 5 agents in sequence:
1. Perception Agent (local simulation)
2. Planner Agent (API: `/api/planner`)
3. Generator Agent (API: `/api/generator`)
4. Execution Agent (local simulation)
5. Healer Agent (API: `/api/healer`)

## Dependencies

- `react` - UI framework
- `react-dom` - React DOM rendering
- `lucide-react` - Icon library
- `axios` - HTTP client for API calls
- `tailwindcss` - CSS framework (via CDN in development)

## API Integration

All API calls are made to the FastAPI backend using axios:

```javascript
axios.post('/api/planner', requestData)
axios.post('/api/generator', requestData)
axios.post('/api/healer', requestData)
```

The proxy setting in package.json automatically routes these to `http://localhost:8000`.
