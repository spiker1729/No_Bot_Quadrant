from __future__ import annotations
from typing import Iterable, Iterator, TypeVar, Callable, Sequence

T = TypeVar("T")

__all__ = [
    "batch_iter",
    "batch_by_size",
    "batch_fixed",
]

def batch_iter(iterable: Iterable[T], size: int) -> Iterator[list[T]]:
    """Simple fixed-length batching."""
    bucket: list[T] = []
    for item in iterable:
        bucket.append(item)
        if len(bucket) >= size:
            yield bucket
            bucket = []
    if bucket:
        yield bucket

def batch_fixed(seq: Sequence[T], size: int) -> Iterator[Sequence[T]]:
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def batch_by_size(iterable: Iterable[T], get_size: Callable[[T], int], max_total: int, max_items: int | None = None) -> Iterator[list[T]]:
    """Batch items so that cumulative size <= max_total (and optional item cap).

    Args:
        iterable: items
        get_size: returns integer size for each item (e.g. token estimate)
        max_total: soft cap for cumulative size. If single item exceeds, it's yielded alone.
        max_items: optional maximum number of items per batch.
    """
    bucket: list[T] = []
    total = 0
    for item in iterable:
        s = get_size(item)
        if not bucket:
            bucket.append(item)
            total = s
            continue
        if total + s > max_total or (max_items and len(bucket) >= max_items):
            yield bucket
            bucket = [item]
            total = s
        else:
            bucket.append(item)
            total += s
    if bucket:
        yield bucket
