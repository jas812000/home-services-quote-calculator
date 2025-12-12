"""
models.py

Simple data models used throughout the application.
These represent structured data, not behavior-heavy logic.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeHM:
    """
    Represents a time using hour and minute.
    Immutable so values cannot be modified after creation.
    """
    hour: int
    minute: int

    def as_hours(self) -> float:
        """Convert time to decimal hours."""
        return self.hour + self.minute / 60.0
