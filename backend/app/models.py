from pydantic import BaseModel
from typing import List, Optional

class DebateRequest(BaseModel):
    question: str

class DebateTurn(BaseModel):
    speaker: str
    content: str

class DebateResult(BaseModel):
    transcript: List[DebateTurn]
    winner: str
    confidence: int
    reason: str
