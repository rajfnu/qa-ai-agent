from fastapi import APIRouter, HTTPException
from app.models import PlannerRequest, AgentResponse
import time
import random

router = APIRouter()

@router.post("/planner", response_model=AgentResponse)
async def planner_agent(request: PlannerRequest):
    """
    Planner Agent (TestPlanerAgent / Reasoning Agent)

    This agent creates a structured Test Plan based on:
    - Application context (name, type, URL)
    - Requirements/scope from BRD documents
    - Test types to be performed

    Uses ReAct Agent with context from MCP and LLM reasoning.

    Based on the architecture diagram:
    - Takes NLP Instructions as input
    - Uses Context from MCP
    - Communicates with LLM (reasoning model)
    - Creates Test Plan document
    """

    try:
        # Simulate processing time (AI reasoning takes time)
        time.sleep(random.uniform(1.5, 2.5))

        # Dummy AI logic - In real implementation, this would:
        # 1. Query MCP for context about the application
        # 2. Use LangGraph/LangChain to create structured reasoning
        # 3. Generate test plan with priorities and risk assessment

        test_cases = []
        num_cases = len(request.testTypes) * random.randint(3, 5)

        for i in range(num_cases):
            test_cases.append({
                "id": f"TC_{i+1:03d}",
                "name": f"Test case for {request.scope.split(',')[0] if ',' in request.scope else request.scope}",
                "type": random.choice(request.testTypes),
                "priority": random.choice(["High", "Medium", "Low"]),
                "risk": random.choice(["High", "Medium", "Low"]),
                "steps": [
                    "Navigate to application",
                    "Perform test action",
                    "Verify expected result",
                    "Capture evidence"
                ]
            })

        test_plan = {
            "appName": request.appName,
            "appType": request.appType,
            "testUrl": request.testUrl,
            "scope": request.scope,
            "totalTestCases": num_cases,
            "testCases": test_cases,
            "coverage": {
                "functional": "Functional Testing" in request.testTypes,
                "regression": "Regression Testing" in request.testTypes,
                "performance": "Performance Testing" in request.testTypes,
                "security": "Security/Pen Testing" in request.testTypes
            },
            "riskAnalysis": {
                "highRisk": sum(1 for tc in test_cases if tc["risk"] == "High"),
                "mediumRisk": sum(1 for tc in test_cases if tc["risk"] == "Medium"),
                "lowRisk": sum(1 for tc in test_cases if tc["risk"] == "Low")
            },
            "estimatedDuration": f"{num_cases * 2} minutes",
            "reasoning": f"Using {request.reasoningModel} to analyze scope and generate {num_cases} high-priority test cases"
        }

        return AgentResponse(
            status="success",
            message=f"Structured Test Plan generated. {num_cases} test cases identified with risk analysis complete.",
            data={"testPlan": test_plan}
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=AgentResponse(
                status="error",
                message="Planner Agent encountered an error",
                error_details=str(e)
            ).dict()
        )
