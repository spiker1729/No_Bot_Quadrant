"""Repository cloning utilities.
Currently supports only PUBLIC GitHub repositories via HTTPS.
Private repository (token / SSH) logic is outlined in comments for future enablement.
"""
from __future__ import annotations

import os
import hashlib
from pathlib import Path
from typing import Optional

from git import Repo, GitCommandError  # type: ignore

DATA_REPOS_DIR = Path(os.getenv("DATA_REPOS_DIR", "data/repos"))
DATA_REPOS_DIR.mkdir(parents=True, exist_ok=True)


def _safe_dir_name(url: str) -> str:
    """Create a deterministic folder name for a repo URL."""
    h = hashlib.sha256(url.encode("utf-8")).hexdigest()[:12]
    return h


def clone_or_update_public_repo(repo_url: str) -> Path:
    """Clone (or pull) a PUBLIC GitHub repository via HTTPS.

    NOTE: Only public repos are supported now. For private repos, see commented code below.
    """
    folder = DATA_REPOS_DIR / _safe_dir_name(repo_url)
    if folder.exists():
        try:
            repo = Repo(folder)
            repo.remote().fetch(prune=True)
            repo.git.pull()
        except GitCommandError:
            # If pull fails, reclone fresh
            for child in folder.iterdir():
                if child.is_file() or child.is_symlink():
                    child.unlink()
                else:
                    import shutil
                    shutil.rmtree(child)
            Repo.clone_from(repo_url, folder)
    else:
        Repo.clone_from(repo_url, folder)
    return folder

# --- Future private repo logic (commented) ---
# def clone_or_update_repo(repo_url: str, token: Optional[str] = None) -> Path:
#     """Clone or update a repository (public or private).
#     If token is provided, it will attempt an authenticated clone over HTTPS.
#     Alternatively, SSH clone can be implemented if deploy keys are configured.
#     """
#     if token:
#         # Authenticated HTTPS form: https://<token>@github.com/owner/repo.git
#         from urllib.parse import urlparse
#         parsed = urlparse(repo_url)
#         if parsed.netloc != "github.com":
#             raise ValueError("Only GitHub supported for token auth in this prototype")
#         auth_url = f"https://{token}:x-oauth-basic@{parsed.netloc}{parsed.path}"
#         return _clone_generic(auth_url, repo_url)
#     return clone_or_update_public_repo(repo_url)
#
# def _clone_generic(actual_url: str, identity_url: str) -> Path:
#     folder = DATA_REPOS_DIR / _safe_dir_name(identity_url)
#     if folder.exists():
#         try:
#             repo = Repo(folder)
#             repo.remote().fetch(prune=True)
#             repo.git.pull()
#         except GitCommandError:
#             import shutil
#             shutil.rmtree(folder)
#             Repo.clone_from(actual_url, folder)
#     else:
#         Repo.clone_from(actual_url, folder)
#     return folder
# --------------------------------------------

__all__ = ["clone_or_update_public_repo"]