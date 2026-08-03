"""Baseline-versus-candidate comparison engine and artifact workflow."""

from .engine import compare_evaluated_records
from .workflow import generate_comparison_artifacts

__all__ = ["compare_evaluated_records", "generate_comparison_artifacts"]
