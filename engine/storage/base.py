"""Frozen contract for every file organization.

All file organizations return RIDs. Every implementation of
:class:`FileOrganization` must pass the conformance suite.
"""

from abc import ABC, abstractmethod
from collections.abc import Iterator

from engine.common.record import Record
from engine.common.rid import RID


class FileOrganization(ABC):
    """Base interface for all file organizations."""

    @abstractmethod
    def insert(self, record: Record) -> RID:
        """Insert a record and return its RID."""

    @abstractmethod
    def fetch(self, rid: RID) -> Record | None:
        """Fetch the record at a RID, or None if it does not exist."""

    @abstractmethod
    def remove(self, rid: RID) -> bool:
        """Remove the record at a RID; returns whether it was removed."""

    @abstractmethod
    def scan(self) -> Iterator[tuple[RID, Record]]:
        """Yield every (RID, record) pair currently stored."""
