"""Sole gateway to the filesystem, tracks reads and writes."""

import os
from pathlib import Path


class DiskManager:
    """Manages a single database file at page granularity."""

    def __init__(self, path: str | Path, page_size: int) -> None:
        self._page_size = page_size
        self.reads = 0
        self.writes = 0

        self._path = Path(path)
        self._path.touch(exist_ok=True)
        self._file = open(self._path, "r+b")

        self._file.seek(0, os.SEEK_END)
        self._next_page_id = self._file.tell() // page_size

    def allocate_page(self) -> int:
        """Physically extend the file by one zero-filled page."""
        page_id = self._next_page_id

        self._file.seek(0, os.SEEK_END)
        self._file.write(bytes(self._page_size))
        self._file.flush()

        self.writes += 1
        self._next_page_id += 1
        return page_id

    def write_page(self, page_id: int, data: bytes) -> None:
        """Overwrite an existing page with exactly page_size bytes."""
        if len(data) != self._page_size:
            raise ValueError(f"data must be exactly {self._page_size} bytes, got {len(data)}")

        self._file.seek(page_id * self._page_size)
        self._file.write(data)
        self._file.flush()

        self.writes += 1

    def read_page(self, page_id: int) -> bytes:
        """Read exactly one page's worth of bytes from disk."""
        self._file.seek(page_id * self._page_size)
        data = self._file.read(self._page_size)

        self.reads += 1
        return data

    def close(self) -> None:
        """Close the managed file. Safe to call more than once."""
        self._file.close()
