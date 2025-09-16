from pydantic import BaseModel, Field
from typing import Optional
import hashlib

class ChunkIn(BaseModel):
    path: str
    language: str
    symbol: str
    kind: str
    content: str
    summary: Optional[str] = None

    def hash(self) -> str:
        h = hashlib.sha256()
        h.update(self.path.encode())
        h.update(self.symbol.encode())
        h.update(self.content.encode())
        return h.hexdigest()[:16]

class ChunkStored(ChunkIn):
    id: str = Field(description="Deterministic chunk id")

__all__ = ["ChunkIn", "ChunkStored"]