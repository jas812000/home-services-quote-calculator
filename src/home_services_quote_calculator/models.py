"""
models.py

Simple data models used throughout the application.

These classes represent structured, immutable data objects that are shared
across the application. They intentionally contain minimal logic.
"""

from dataclasses import dataclass


@dataclass(frozen=True)
class TimeHM:
    """
    Represents a time using hour and minute components.

    This model is immutable to ensure time values cannot be modified after
    creation. It is primarily used for calculating elapsed labor time.
    """

    hour: int
    """Hour component of the time (0–23)."""

    minute: int
    """Minute component of the time (0–59)."""

    def __post_init__(self) -> None:
        """Validate hour and minute values."""
        if not 0 <= self.hour <= 23:
            raise ValueError("Hour must be between 0 and 23.")

        if not 0 <= self.minute <= 59:
            raise ValueError("Minute must be between 0 and 59.")

    def as_hours(self) -> float:
        """
        Convert the time to decimal hours.

        Assumes:
            - hour is in the range 0–23
            - minute is in the range 0–59

        Returns:
            float: Time represented as fractional hours.
        """
        return self.hour + self.minute / 60.0
