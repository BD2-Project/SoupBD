"""In-memory file organization: oracle and unblocking fake."""

from collections.abc import Iterator

from engine.common.record import Record
from engine.common.rid import RID
from engine.storage.base import FileOrganization


class FakeFileOrganization(FileOrganization):
    """In-memory :class:`FileOrganization` used as test oracle."""

    def __init__(self) -> None:
        self._records: dict[RID, Record] = {}
        self._next_slot = 0

    def insert(self, record: Record) -> RID:
        rid = RID(page_id=0, slot=self._next_slot)
        self._next_slot += 1
        self._records[rid] = record
        return rid

    def fetch(self, rid: RID) -> Record | None:
        return self._records.get(rid)

    def remove(self, rid: RID) -> bool:
        return self._records.pop(rid, None) is not None

    def scan(self) -> Iterator[tuple[RID, Record]]:
        yield from self._records.items()
