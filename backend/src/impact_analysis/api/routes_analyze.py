from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["analyze"])

class DiffRequest(BaseModel):
    diff_patch: str

class ImpactResponse(BaseModel):
    impacted: list

@router.post("/analyze_diff", response_model=ImpactResponse)
def analyze_diff(body: DiffRequest):
    # TODO: implement real diff + graph expansion
    return ImpactResponse(impacted=[{"symbol": "demo", "reason": "stub"}])

__all__ = ["router"]