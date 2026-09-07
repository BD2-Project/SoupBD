"""Volcano operator model.

Frozen contract between query processing and the rest of the engine.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from typing import Any

from engine.common.record import Record


@dataclass
class PlanNode:
    """Serializable execution plan node (contract with the frontend).

    ``op`` is a free string on purpose: future operators
    (InvertedIndexScan, HNSWSearch) appear without touching the renderer.
    """

    op: str
    detail: dict[str, Any]
    rows: int
    elapsed_ms: float
    disk_reads: int
    disk_writes: int
    children: list["PlanNode"] = field(default_factory=list)

    def to_json(self) -> dict[str, Any]:
        """Return the JSON contract shape of the plan node."""
        return {
            "op": self.op,
            "detail": self.detail,
            "rows": self.rows,
            "elapsed_ms": self.elapsed_ms,
            "disk_reads": self.disk_reads,
            "disk_writes": self.disk_writes,
            "children": [child.to_json() for child in self.children],
        }


class Operator(ABC):
    """Base interface for all Volcano query operators."""

    @abstractmethod
    def open(self) -> None:
        """Prepare the operator for execution."""

    @abstractmethod
    def next(self) -> Record | None:
        """Return the next record or None when exhausted."""

    @abstractmethod
    def close(self) -> None:
        """Release resources held by the operator."""

    @abstractmethod
    def explain(self) -> PlanNode:
        """Return the execution plan node for this operator."""
