"""Common contract for writing evaluated test evidence to files."""

from __future__ import annotations

from abc import ABC, abstractmethod
from pathlib import Path

from ..models import EvaluatedRecord, RunSummary, TestPack


class ReportWriter(ABC):
    """Contract implemented by every evidence report writer."""

    @property
    @abstractmethod
    def format_name(self) -> str:
        """Return a stable report-format name."""

    @abstractmethod
    def write(
        self,
        destination: Path,
        test_pack: TestPack,
        records: list[EvaluatedRecord],
        summary: RunSummary,
    ) -> Path:
        """Write one report artifact and return its final path."""
