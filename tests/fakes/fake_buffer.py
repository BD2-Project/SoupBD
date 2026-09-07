"""In-memory buffer manager: oracle and unblocking fake."""


class FakeBufferManager:
    """In-memory buffer manager with pin/unpin semantics."""

    def __init__(self, capacity: int = 0) -> None:
        self._capacity = capacity
        self._pins: dict[int, int] = {}

    @property
    def capacity(self) -> int:
        return self._capacity

    def pin(self, page_id: int) -> None:
        self._pins[page_id] = self._pins.get(page_id, 0) + 1

    def unpin(self, page_id: int) -> None:
        if page_id not in self._pins:
            raise KeyError(page_id)
        self._pins[page_id] -= 1
        if self._pins[page_id] == 0:
            del self._pins[page_id]

    def is_pinned(self, page_id: int) -> bool:
        return page_id in self._pins
