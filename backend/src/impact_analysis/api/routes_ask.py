from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["ask"])

class AskRequest(BaseModel):
    question: str
    context_ids: list[str] | None = None
    repo_path: str | None = None

class AskResponse(BaseModel):
    answer: str
    used_ids: list[str]

@router.post("/ask", response_model=AskResponse)
def ask(body: AskRequest):
    # Heuristic: if asking about "auth" in a repo, list functions with auth-like names
    if body.repo_path and ("auth" in body.question.lower() or "authentication" in body.question.lower()):
        import os, re
        from pathlib import Path
        repo = Path(body.repo_path)
        if repo.exists():
            impacted: list[str] = []
            func_re = re.compile(r"def\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*\(")
            for root, _dirs, files in os.walk(repo):
                for f in files:
                    if f.endswith('.py'):
                        p = Path(root) / f
                        try:
                            txt = p.read_text(encoding='utf-8', errors='ignore')
                        except Exception:
                            continue
                        if 'auth' in txt or 'authenticate' in txt or 'login' in txt or 'permission' in txt:
                            for m in func_re.finditer(txt):
                                fn = m.group(1)
                                if fn not in impacted:
                                    impacted.append(fn)
                            if len(impacted) > 50:
                                break
                if len(impacted) > 50:
                    break
            if impacted:
                return AskResponse(answer=f"Potentially impacted functions: {', '.join(impacted[:50])}", used_ids=[])
    # Default stub
    return AskResponse(answer=f"Stub answer for: {body.question}", used_ids=body.context_ids or [])

__all__ = ["router"]