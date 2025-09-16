from __future__ import annotations
import os
from typing import List, Tuple
from qdrant_client import QdrantClient
from qdrant_client.http.models import VectorParams, Distance, PointStruct
from ..models.chunk import ChunkIn

_QDRANT_URL = os.getenv("QDRANT_URL", "http://localhost:6333")
_COLLECTION = os.getenv("QDRANT_COLLECTION", "impact_chunks")

class QdrantVectorStore:
    def __init__(self):
        self.client = QdrantClient(url=_QDRANT_URL)
        self.collection_name = _COLLECTION
        self._ensure()

    def _ensure(self):
        existing = [c.name for c in self.client.get_collections().collections]
        if self.collection_name not in existing:
            self.client.recreate_collection(
                collection_name=self.collection_name,
                vectors_config=VectorParams(size=64, distance=Distance.COSINE),
            )

    def upsert_chunks(self, vectors: List[Tuple[ChunkIn, list]]):
        points = []
        for c, vec in vectors:
            cid = c.hash()
            points.append(
                PointStruct(id=cid, vector=vec, payload={
                    "path": c.path,
                    "language": c.language,
                    "symbol": c.symbol,
                    "kind": c.kind,
                    "summary": c.summary or "",
                })
            )
        if points:
            self.client.upsert(collection_name=self.collection_name, points=points)

__all__ = ["QdrantVectorStore"]