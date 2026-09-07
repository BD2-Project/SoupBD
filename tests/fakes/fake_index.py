"""In-memory index: oracle and unblocking fake."""

from collections import defaultdict

from engine.common.errors import UnsupportedOperation
from engine.common.rid import RID
from engine.indexes.base import Index, Key


class FakeIndex(Index):
    """In-memory :class:`Index` used as test oracle.

    Disk-backed indexes are added to the conformance suite when they exist.
    """

    def __init__(self, *, supports_range: bool = True) -> None:
        self._entries: dict[Key, list[RID]] = defaultdict(list)
        self._supports_range = supports_range

    @property
    def supports_range(self) -> bool:
        return self._supports_range

    def insert(self, key: Key, rid: RID) -> None:
        self._entries[key].append(rid)

    def search(self, key: Key) -> list[RID]:
        return list(self._entries.get(key, []))

    def range_search(self, lo: Key, hi: Key) -> list[RID]:
        if not self._supports_range:
            raise UnsupportedOperation("FakeIndex does not support range searches")
        return [rid for key, rids in self._entries.items() if lo <= key <= hi for rid in rids]

    def remove(self, key: Key, rid: RID | None = None) -> int:
        if key not in self._entries:
            return 0
        if rid is None:
            removed = len(self._entries.pop(key))
            return removed
        rids = self._entries[key]
        try:
            rids.remove(rid)
        except ValueError:
            return 0
        if not rids:
            del self._entries[key]
        return 1

    def close(self) -> None:
        self._entries.clear()
