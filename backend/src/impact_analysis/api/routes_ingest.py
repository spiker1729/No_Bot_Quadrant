from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from ..services.repo_cloner import clone_or_update_public_repo

router = APIRouter(prefix="/api", tags=["ingest"])

class IngestRequest(BaseModel):
    repo_url: str
    token: str | None = None  # Token ignored (public only). Left for future.

class IngestResponse(BaseModel):
    job_id: str
    repo_path: str
    status: str

@router.post("/ingest_repo", response_model=IngestResponse)
def ingest_repo(body: IngestRequest):
    # Reject token usage for now: public repos only.
    if body.token:
        raise HTTPException(status_code=400, detail="Private repos not supported in this build. Omit token.")
    
    # Clean and validate the repository URL
    repo_url = body.repo_url.strip()
    
    # Remove @ prefix if present
    if repo_url.startswith('@'):
        repo_url = repo_url[1:]
    
    # Ensure it's a proper GitHub URL
    if not repo_url.startswith('https://github.com/'):
        if repo_url.startswith('github.com/'):
            repo_url = f"https://{repo_url}"
        elif '/' in repo_url and not repo_url.startswith('http'):
            repo_url = f"https://github.com/{repo_url}"
        else:
            raise HTTPException(status_code=400, detail="Invalid repository URL. Please use format: https://github.com/owner/repo")
    
    # Ensure it ends with .git for proper cloning
    if not repo_url.endswith('.git'):
        repo_url += '.git'
    
    try:
        path = clone_or_update_public_repo(repo_url)
        # TODO: enqueue background job for deeper processing (chunking, embedding)
        job_id = path.name
        return IngestResponse(job_id=job_id, repo_path=str(path), status="cloned")
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Failed to clone repository: {str(e)}")

__all__ = ["router"]