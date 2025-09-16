import hashlib
from typing import Union

__all__ = [
    "stable_hash_hex",
    "stable_file_hash",
    "stable_path_symbol_hash",
    "derive_chunk_id",
]

# NOTE: Keep the first 16 hex chars for short IDs (same as existing ChunkIn.hash slice)
_SHORT_LEN = 16

StrOrBytes = Union[str, bytes]

def _to_bytes(data: StrOrBytes) -> bytes:
    if isinstance(data, bytes):
        return data
    return data.encode("utf-8", errors="replace")

def stable_hash_hex(*parts: StrOrBytes, short: bool = False) -> str:
    """Return a SHA256 hex digest of concatenated parts.

    Args:
        *parts: String/bytes parts to concatenate deterministically.
        short: If True, truncate to _SHORT_LEN characters (sufficient for local IDs).
    """
    h = hashlib.sha256()
    for p in parts:
        h.update(_to_bytes(p))
        # delimiter to avoid accidental collisions when concatenating variable length parts
        h.update(b"\x1f")
    digest = h.hexdigest()
    return digest[:_SHORT_LEN] if short else digest

def stable_file_hash(content: StrOrBytes) -> str:
    """Full SHA256 hex for file content."""
    return stable_hash_hex(content, short=False)

def stable_path_symbol_hash(path: str, symbol: str, content_hash: str | None = None, short: bool = True) -> str:
    """Deterministic ID from path + symbol (+ optional content hash).

    Including content hash makes the id change on content modifications (versioned
    chunks). Excluding it yields a stable logical symbol id.
    """
    parts = [path, symbol]
    if content_hash:
        parts.append(content_hash)
    return stable_hash_hex(*parts, short=short)

def derive_chunk_id(path: str, symbol: str, content: StrOrBytes) -> str:
    """Convenience helper mirroring previous inline logic in ChunkIn.hash()."""
    return stable_path_symbol_hash(path, symbol, stable_file_hash(content), short=True)
