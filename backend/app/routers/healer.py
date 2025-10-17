from fastapi import APIRouter, HTTPException
from app.models import HealerRequest, AgentResponse
import time
import random

router = APIRouter()

@router.post("/healer", response_model=AgentResponse)
async def healer_agent(request: HealerRequest):
    """
    Healer Agent (TestHealerAgent / Learning Agent)

    This agent fixes Test Scripts if there are any changes in the web application or test failures.

    Based on the architecture diagram:
    - Analyzes execution results
    - Uses Code Agent to fix test scripts
    - Uses Tools for Playwright
    - Communicates with LLM for root cause analysis
    - Updates Test Scripts based on application changes
    - Provides feedback for CICD pipeline
    """

    try:
        # Simulate processing time (analysis and healing takes time)
        time.sleep(random.uniform(1.5, 2.5))

        # Dummy AI logic - In real implementation, this would:
        # 1. Perform Root Cause Analysis (RCA) on failures
        # 2. Use Computer Vision to detect UI changes
        # 3. Use LLM to fix code based on detected issues
        # 4. Update scripts and commit to Git
        # 5. Create JIRA tickets for non-auto-fixable issues

        execution_result = request.executionResult.lower()
        test_script = request.testScript

        # Analyze execution result
        if "css selector change" in execution_result or "selector" in execution_result:
            # Self-healing scenario: Fix selector issues
            healing_action = "SELF_HEALED"
            root_cause = "UI element locator changed (CSS selector mismatch)"

            # Simulate fixing selectors
            fixed_script = test_script.replace("#old-login-btn", "#new-submit-btn")
            fixed_script = fixed_script.replace("button.submit", "button[type='submit']")

            healing_details = {
                "rcaComplete": True,
                "rootCause": root_cause,
                "action": healing_action,
                "fixesApplied": [
                    "Updated CSS selector: #old-login-btn → #new-submit-btn",
                    "Improved selector reliability: button.submit → button[type='submit']"
                ],
                "updatedScript": fixed_script,
                "gitCommit": f"auto-heal-{random.randint(1000, 9999)}",
                "confidence": 0.92,
                "needsManualReview": False
            }

            summary = "RCA complete. Root cause: UI element locator change. Script successfully self-healed and committed to Git."

        elif "environment issue" in execution_result or "failed" in execution_result:
            # Environment/infrastructure issue - create JIRA ticket
            healing_action = "JIRA_TICKET_CREATED"
            root_cause = "Environment connection failure or infrastructure issue"

            healing_details = {
                "rcaComplete": True,
                "rootCause": root_cause,
                "action": healing_action,
                "jiraTicket": f"QA-{random.randint(100, 999)}",
                "jiraDetails": {
                    "title": "Test Execution Failed - Environment Issue",
                    "priority": "High",
                    "assignee": "DevOps Team",
                    "description": f"Automated tests failed due to: {root_cause}"
                },
                "needsManualReview": True,
                "updatedScript": test_script  # No changes needed
            }

            summary = f"RCA complete. Root cause: {root_cause}. JIRA ticket {healing_details['jiraTicket']} created for DevOps team."

        else:
            # Tests passed - update confidence model
            healing_action = "CONFIDENCE_UPDATED"

            healing_details = {
                "rcaComplete": True,
                "rootCause": "No issues detected",
                "action": healing_action,
                "testsPassed": True,
                "confidenceScore": 0.98,
                "learningUpdates": [
                    "Updated baseline for test stability",
                    "Reinforced successful test patterns"
                ],
                "updatedScript": test_script  # No changes needed
            }

            summary = "Tests passed successfully. Confidence model updated with successful test patterns."

        return AgentResponse(
            status="success",
            message=summary,
            data={
                "summary": summary,
                "healingAction": healing_action,
                "details": healing_details
            }
        )

    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=AgentResponse(
                status="error",
                message="Healer Agent encountered an error",
                error_details=str(e)
            ).dict()
        )
