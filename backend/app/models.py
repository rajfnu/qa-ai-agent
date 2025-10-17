from pydantic import BaseModel
from typing import List, Optional, Dict, Any

# === Request Models ===

class PlannerRequest(BaseModel):
    appName: str
    appType: str
    testUrl: str
    scope: str
    testTypes: List[str]
    reasoningModel: str

class GeneratorRequest(BaseModel):
    testPlan: Dict[str, Any]
    automationFramework: str
    generationModel: str

class HealerRequest(BaseModel):
    testScript: str
    executionResult: str
    automationFramework: str

# === Response Models ===

class AgentResponse(BaseModel):
    status: str  # "success" or "error"
    message: str
    data: Optional[Dict[str, Any]] = None
    error_details: Optional[str] = None
