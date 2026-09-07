"""Record serialization / deserialization.

Placeholder used by the frozen contracts. The concrete layout is defined
together with the storage milestone.
"""

from dataclasses import dataclass


@dataclass
class Record:
    """Minimal record placeholder referenced by the frozen contracts."""

    data: bytes
