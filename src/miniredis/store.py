"""In-memory store.

Naive by design: plain dict + linear scans. Real Redis uses hash tables,
expire heaps, SDS strings, and specialized encodings — we call those out
in class when we upgrade a feature.
"""

from __future__ import annotations

import time
from typing import Any


class Store:
    """Key → value map with optional TTL (checked lazily on access)."""

    def __init__(self) -> None:
        self._data: dict[str, Any] = {}
        # key → unix timestamp when the key should die (naive lazy expire)
        self._expires: dict[str, float] = {}

    def _purge_if_expired(self, key: str) -> bool:
        """Return True if the key was expired and removed."""
        deadline = self._expires.get(key)
        if deadline is None:
            return False
        if time.time() < deadline:
            return False
        self._data.pop(key, None)
        self._expires.pop(key, None)
        return True

    def set(self, key: str, value: str) -> str:
        self._data[key] = value
        self._expires.pop(key, None)
        return "OK"

    def get(self, key: str) -> str | None:
        if self._purge_if_expired(key):
            return None
        value = self._data.get(key)
        if value is None:
            return None
        if not isinstance(value, str):
            raise TypeError("WRONGTYPE Operation against a key holding the wrong kind of value")
        return value

    def delete(self, *keys: str) -> int:
        removed = 0
        for key in keys:
            self._purge_if_expired(key)
            if key in self._data:
                del self._data[key]
                self._expires.pop(key, None)
                removed += 1
        return removed

    def exists(self, *keys: str) -> int:
        count = 0
        for key in keys:
            if self._purge_if_expired(key):
                continue
            if key in self._data:
                count += 1
        return count

    def keys(self, pattern: str = "*") -> list[str]:
        """Naive KEYS — O(N) scan. Real Redis also warns: don't use KEYS in prod."""
        alive = []
        for key in list(self._data.keys()):
            if self._purge_if_expired(key):
                continue
            if _match(pattern, key):
                alive.append(key)
        return alive

    def expire(self, key: str, seconds: int) -> int:
        if self._purge_if_expired(key):
            return 0
        if key not in self._data:
            return 0
        self._expires[key] = time.time() + seconds
        return 1

    def ttl(self, key: str) -> int:
        if self._purge_if_expired(key):
            return -2
        if key not in self._data:
            return -2
        deadline = self._expires.get(key)
        if deadline is None:
            return -1
        remaining = int(deadline - time.time())
        return remaining if remaining >= 0 else -2

    def flushdb(self) -> str:
        self._data.clear()
        self._expires.clear()
        return "OK"

    def dbsize(self) -> int:
        for key in list(self._data.keys()):
            self._purge_if_expired(key)
        return len(self._data)


def _match(pattern: str, key: str) -> bool:
    """Tiny glob: only `*` (any chars) and `?` (one char). Enough for class demos."""
    if pattern == "*":
        return True
    i = j = 0
    star_p = star_k = -1
    while j < len(key):
        if i < len(pattern) and pattern[i] in (key[j], "?"):
            i += 1
            j += 1
        elif i < len(pattern) and pattern[i] == "*":
            star_p = i
            star_k = j
            i += 1
        elif star_p != -1:
            i = star_p + 1
            star_k += 1
            j = star_k
        else:
            return False
    while i < len(pattern) and pattern[i] == "*":
        i += 1
    return i == len(pattern)
