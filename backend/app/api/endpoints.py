from fastapi import APIRouter, HTTPException
from app.models import DebateRequest, DebateResult
from app.workflow import DebateWorkflow
from typing import List, Optional

router = APIRouter()

@router.post("/debate", response_model=DebateResult)
async def start_debate(request: DebateRequest):
    try:
        workflow = DebateWorkflow()
        result = await workflow.run(request.question)
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
