from __future__ import annotations
from typing import Iterable

__all__ = ["estimate_tokens", "estimate_tokens_batch"]

# Simple heuristic: ~1 token per 4 chars (English-ish) fallback min 1 token per word.
# This avoids bringing heavy tokenizer dependencies into the lightweight prototype.
_CHARS_PER_TOKEN = 4

def estimate_tokens(text: str) -> int:
    if not text:
        return 0
    approx = max(len(text) // _CHARS_PER_TOKEN, len(text.split()))
    return approx

def estimate_tokens_batch(texts: Iterable[str]) -> int:
    return sum(estimate_tokens(t) for t in texts)
