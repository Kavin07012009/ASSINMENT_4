"""Attendance processing package."""
from .reader import load
from .stats import compute, percentage
from .report import write
__all__ = ["load", "compute", "percentage", "write"]
