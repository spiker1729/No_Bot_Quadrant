from __future__ import annotations
from pathlib import Path
from typing import List
from .repo_cloner import clone_or_update_public_repo
from .embedding_client import get_embedding_client
from .qdrant_client import QdrantVectorStore
from .neo4j_client import Neo4jDriver
from ..models.chunk import ChunkIn

# Placeholder file scanning & chunking (to be replaced with real AST logic)

def naive_collect_chunks(repo_path: Path) -> List[ChunkIn]:
    chunks: List[ChunkIn] = []
    for p in repo_path.rglob("*.py"):
        try:
            content = p.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if not content.strip():
            continue
        symbol = p.stem
        chunks.append(ChunkIn(path=str(p.relative_to(repo_path)), language="python", symbol=symbol, kind="file", content=content[:4000]))
    return chunks

class IngestionOrchestrator:
    def __init__(self):
        self.emb = get_embedding_client()
        self.store = QdrantVectorStore()
        self.graph = Neo4jDriver()

    def ingest_repo(self, repo_url: str) -> dict:
        path = clone_or_update_public_repo(repo_url)
        chunks = naive_collect_chunks(path)
        vecs = []
        for c in chunks:
            vecs.append((c, self.emb.embed(c.content)))
            self.graph.upsert_code_node(c.hash(), c.path, c.symbol, c.kind)
        self.store.upsert_chunks(vecs)
        return {"repo": repo_url, "chunks": len(chunks)}

__all__ = ["IngestionOrchestrator"]