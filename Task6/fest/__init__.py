"""Robust college fest registration processing package."""
from .reader import read_department, InvalidRegistration
from .merge import merge_registrations
from .reports import write_outputs
__all__ = ["read_department", "InvalidRegistration", "merge_registrations", "write_outputs"]
