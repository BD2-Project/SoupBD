"""Frozen contract for every index structure.

All indexes point to RIDs. Every implementation of :class:`Index` must pass
the conformance suite in ``tests/unit/indexes/test_index_contract.py``.
"""

from abc import ABC, abstractmethod
from typing import Any

from engine.common.rid import RID

#: Key type supported by indexes (int, str and composite keys).
Key = Any


class Index(ABC):
    """Base interface for all index structures."""

    @abstractmethod
    def insert(self, key: Key, rid: RID) -> None:
        """Insert a RID under a key."""

    @abstractmethod
    def search(self, key: Key) -> list[RID]:
        """Return all RIDs matching the key."""

    @abstractmethod
    def range_search(self, lo: Key, hi: Key) -> list[RID]:
        """Return RIDs whose key is in the inclusive range [lo, hi].

        Raises UnsupportedOperation on indexes that do not support ranges.
        """

    @abstractmethod
    def remove(self, key: Key, rid: RID | None = None) -> int:
        """Remove a RID (or all RIDs) under a key; returns the count removed."""

    @property
    @abstractmethod
    def supports_range(self) -> bool:
        """Whether the index supports range searches."""

    @abstractmethod
    def close(self) -> None:
        """Flush and release resources."""
