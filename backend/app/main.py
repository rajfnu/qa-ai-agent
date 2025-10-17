from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import planner, generator, healer

app = FastAPI(
    title="QA AI Agent API",
    description="Backend API for Multi-Agent QA Automation System",
    version="1.0.0"
)

# Enable CORS for frontend communication
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],  # React default port
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers for the 3 main agents
app.include_router(planner.router, prefix="/api", tags=["Planner Agent"])
app.include_router(generator.router, prefix="/api", tags=["Generator Agent"])
app.include_router(healer.router, prefix="/api", tags=["Healer Agent"])

@app.get("/")
async def root():
    return {
        "message": "QA AI Agent API is running",
        "agents": ["Planner", "Generator", "Healer"],
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "qa-ai-agent-api"}
