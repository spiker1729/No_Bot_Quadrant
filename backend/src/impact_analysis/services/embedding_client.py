from __future__ import annotations
import os
import hashlib
import numpy as np
from typing import List

_EMBED_DIM = 64  # small demo dimension

class SimpleEmbeddingClient:
    def __init__(self):
        pass

    def embed(self, text: str) -> List[float]:
        # Deterministic hash -> vector (demo only)
        h = hashlib.sha256(text.encode()).digest()
        nums = [b for b in h]
        # pad / repeat to dimension
        vec = (nums * ((_EMBED_DIM // len(nums)) + 1))[:_EMBED_DIM]
        # normalize
        arr = np.array(vec, dtype=float)
        arr = arr / (arr.max() or 1)
        return arr.tolist()

_client: SimpleEmbeddingClient | None = None

def get_embedding_client() -> SimpleEmbeddingClient:
    global _client
    if _client is None:
        _client = SimpleEmbeddingClient()
    return _client

__all__ = ["get_embedding_client", "SimpleEmbeddingClient", "_EMBED_DIM"]