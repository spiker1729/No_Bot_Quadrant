from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List
from ..models.chunk import ChunkIn
from ..services.embedding_client import get_embedding_client
from ..services.qdrant_client import QdrantVectorStore

router = APIRouter(prefix="/api", tags=["chunks"])

class ChunkBatchRequest(BaseModel):
    chunks: List[ChunkIn]

class ChunkBatchResponse(BaseModel):
    stored: int
    collection: str

@router.post("/ingest_chunk_batch", response_model=ChunkBatchResponse)
def ingest_chunk_batch(body: ChunkBatchRequest):
    if not body.chunks:
        raise HTTPException(status_code=400, detail="No chunks provided")
    emb_client = get_embedding_client()
    store = QdrantVectorStore()
    vectors = []
    for c in body.chunks:
        vec = emb_client.embed(c.content)
        vectors.append((c, vec))
    store.upsert_chunks(vectors)
    return ChunkBatchResponse(stored=len(vectors), collection=store.collection_name)

__all__ = ["router"]