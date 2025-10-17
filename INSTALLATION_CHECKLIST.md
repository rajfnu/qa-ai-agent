# Installation Checklist

Use this checklist to ensure everything is set up correctly.

## Prerequisites Check

### System Requirements
- [ ] Python 3.9+ installed (`python3 --version`)
- [ ] Node.js 16+ installed (`node --version`)
- [ ] npm installed (`npm --version`)
- [ ] pip installed (`pip --version`)
- [ ] Git installed (optional) (`git --version`)

### Verify Installation
```bash
# Check Python
python3 --version
# Expected: Python 3.9.x or higher

# Check Node
node --version
# Expected: v16.x.x or higher

# Check npm
npm --version
# Expected: 8.x.x or higher
```

## Backend Setup Checklist

### 1. Navigate to Backend
- [ ] `cd backend`
- [ ] Confirm you're in the right directory (`ls` should show `app/` and `requirements.txt`)

### 2. Virtual Environment
- [ ] Create venv: `python3 -m venv venv`
- [ ] Activate venv:
  - macOS/Linux: `source venv/bin/activate`
  - Windows: `venv\Scripts\activate`
- [ ] Verify activation (should see `(venv)` in terminal)

### 3. Install Dependencies
- [ ] Install packages: `pip install -r requirements.txt`
- [ ] Wait for installation to complete
- [ ] Verify: `pip list` should show fastapi, uvicorn, pydantic

### 4. Start Backend Server
- [ ] Run: `uvicorn app.main:app --reload --port 8000`
- [ ] Wait for startup message
- [ ] Verify: Terminal shows "Application startup complete"
- [ ] Test: Open http://localhost:8000 in browser
- [ ] Expected: JSON message about QA AI Agent API

### 5. Test API Documentation
- [ ] Open http://localhost:8000/docs
- [ ] Expected: Swagger UI with 3 endpoints
  - POST /api/planner
  - POST /api/generator
  - POST /api/healer
- [ ] Open http://localhost:8000/health
- [ ] Expected: `{"status":"healthy","service":"qa-ai-agent-api"}`

### Backend Troubleshooting
If backend fails:
- [ ] Check Python version is 3.9+
- [ ] Ensure venv is activated (see `(venv)` in prompt)
- [ ] Try: `pip install --upgrade pip`
- [ ] Check port 8000 is free: `lsof -i :8000` (kill if needed)
- [ ] Check for error messages in terminal

## Frontend Setup Checklist

### 1. Navigate to Frontend
- [ ] Open **NEW terminal** (keep backend running)
- [ ] `cd frontend`
- [ ] Confirm you're in the right directory (`ls` should show `src/` and `package.json`)

### 2. Install Dependencies
- [ ] Run: `npm install`
- [ ] Wait 1-3 minutes for installation
- [ ] Ignore peer dependency warnings (normal)
- [ ] Verify: `node_modules/` folder created

### 3. Install Tailwind CSS
- [ ] Run: `npm install -D tailwindcss postcss autoprefixer`
- [ ] Verify: Check package.json for tailwindcss in devDependencies

### 4. Start Frontend Server
- [ ] Run: `npm start`
- [ ] Wait for compilation (15-30 seconds)
- [ ] Browser should auto-open to http://localhost:3000
- [ ] If not, manually open http://localhost:3000

### 5. Verify UI
- [ ] Page loads without errors
- [ ] See "Multi-Agent QA Control Center" header
- [ ] See configuration panels on left
- [ ] See "Start Agent Run" button (green/amber)
- [ ] No console errors in browser DevTools (F12)

### Frontend Troubleshooting
If frontend fails:
- [ ] Check Node version is 16+
- [ ] Delete node_modules: `rm -rf node_modules`
- [ ] Delete package-lock.json: `rm package-lock.json`
- [ ] Reinstall: `npm install`
- [ ] Check port 3000 is free: `lsof -i :3000`
- [ ] Check backend is running at localhost:8000
- [ ] Clear browser cache (Cmd+Shift+R / Ctrl+Shift+R)

## Integration Test Checklist

### 1. Both Services Running
- [ ] Terminal 1: Backend running on port 8000
- [ ] Terminal 2: Frontend running on port 3000
- [ ] No error messages in either terminal

### 2. UI Configuration
- [ ] Change "Application Name" field → text updates
- [ ] Select different "Application Type" → dropdown works
- [ ] Modify "Test URL" → text updates
- [ ] Click test type buttons → they toggle on/off
- [ ] Modify "Functionality Scope" → textarea updates

### 3. Full Workflow Test
- [ ] Click "Start Agent Run" button
- [ ] Button changes to "Running..." with spinner
- [ ] "Ready to Execute" changes to "RUNNING" (amber)
- [ ] Perception Agent card turns amber, then green
- [ ] Planner Agent card turns amber, then green
- [ ] Generator Agent card turns amber, then green
- [ ] Execution Agent card turns amber, then green
- [ ] Healer Agent card turns amber, then green
- [ ] Status changes to "COMPLETE" (green)
- [ ] "Final Report" appears (green box)
- [ ] Event logs show detailed messages

### 4. API Communication Test
- [ ] Open browser DevTools (F12) → Network tab
- [ ] Click "Start Agent Run"
- [ ] See POST requests to:
  - `/api/planner` (status 200)
  - `/api/generator` (status 200)
  - `/api/healer` (status 200)
- [ ] All requests return success responses

### Integration Troubleshooting
If workflow fails:
- [ ] Check browser console (F12) for errors
- [ ] Check backend terminal for request logs
- [ ] Verify backend health: http://localhost:8000/health
- [ ] Test API directly: http://localhost:8000/docs
- [ ] Check CORS settings in backend/app/main.py
- [ ] Reload browser page (Cmd+R / Ctrl+R)

## File Structure Verification

### Backend Files
- [ ] `backend/app/main.py` exists
- [ ] `backend/app/models.py` exists
- [ ] `backend/app/routers/planner.py` exists
- [ ] `backend/app/routers/generator.py` exists
- [ ] `backend/app/routers/healer.py` exists
- [ ] `backend/requirements.txt` exists

### Frontend Files
- [ ] `frontend/src/App.js` exists
- [ ] `frontend/src/index.js` exists
- [ ] `frontend/src/index.css` exists
- [ ] `frontend/public/index.html` exists
- [ ] `frontend/package.json` exists
- [ ] `frontend/tailwind.config.js` exists
- [ ] `frontend/postcss.config.js` exists

### Documentation Files
- [ ] `README.md` (main)
- [ ] `QUICKSTART.md`
- [ ] `PROJECT_SUMMARY.md`
- [ ] `backend/README.md`
- [ ] `frontend/README.md`

## Success Criteria

You have successfully installed the system when:

✅ Backend server running without errors
✅ Frontend UI loads in browser
✅ Can click "Start Agent Run"
✅ All 5 agents complete successfully
✅ Event logs show detailed trace
✅ Final report appears
✅ No console errors in browser
✅ No errors in backend terminal
✅ API docs accessible at /docs

## Post-Installation

### Next Steps
1. [ ] Read `QUICKSTART.md` for usage guide
2. [ ] Read `PROJECT_SUMMARY.md` for architecture details
3. [ ] Explore API at http://localhost:8000/docs
4. [ ] Review agent code in `backend/app/routers/`
5. [ ] Customize UI in `frontend/src/App.js`

### Optional Enhancements
- [ ] Set up Git repository: `git init`
- [ ] Create `.gitignore` (already exists)
- [ ] Install code editor extensions (Python, React)
- [ ] Set up Docker (for deployment)
- [ ] Configure environment variables

## Common Issues & Solutions

### "Port already in use"
```bash
# Find process on port
lsof -i :8000  # or :3000

# Kill process
kill -9 <PID>
```

### "Module not found"
```bash
# Backend
cd backend
source venv/bin/activate
pip install -r requirements.txt

# Frontend
cd frontend
rm -rf node_modules
npm install
```

### "CORS error"
- Check backend/app/main.py has `allow_origins=["http://localhost:3000"]`
- Restart backend server
- Clear browser cache

### "Agents not executing"
- Verify backend is running (check terminal)
- Check http://localhost:8000/health returns healthy
- Open browser DevTools → Console for errors
- Check Network tab for failed requests

## Getting Help

If you're stuck:
1. Check terminal output for error messages
2. Check browser console (F12) for JavaScript errors
3. Review the README files
4. Test API endpoints directly at /docs
5. Verify all prerequisites are met

## Clean Slate Reset

To start fresh:

```bash
# Stop all servers (Ctrl+C in terminals)

# Backend clean
cd backend
deactivate  # exit venv
rm -rf venv
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# Frontend clean
cd frontend
rm -rf node_modules
rm package-lock.json
npm install

# Restart both servers
# Terminal 1: cd backend && uvicorn app.main:app --reload --port 8000
# Terminal 2: cd frontend && npm start
```

---

Good luck! 🚀
