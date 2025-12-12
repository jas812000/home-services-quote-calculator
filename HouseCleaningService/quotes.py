"""
quotes.py

Quote calculation classes.
Each class represents one complete service quote and knows how to
calculate its own totals.
"""

from dataclasses import dataclass
from pricing import PriceRules
from models import TimeHM


@dataclass
class HouseCleaningQuote:
    """
    Represents a house cleaning service quote.
    Handles all house-related calculations.
    """
    house_sqft: int
    carpet_rooms: int
    bathrooms: int
    dust_rooms: int
    thorough: bool
    is_senior: bool

    def tier(self) -> str:
        """Determine house size tier."""
        return PriceRules.house_tier(self.house_sqft)

    def subtotal(self) -> float:
        """Calculate subtotal before fees, discounts, and tax."""
        t = self.tier()
        return (
            self.carpet_rooms * PriceRules.carpet_rate(t)
            + self.bathrooms * PriceRules.bathroom_rate(t)
            + self.dust_rooms * PriceRules.dust_rate(t)
            + PriceRules.house_sqft_surcharge(self.house_sqft)
        )

    def service_fee(self) -> float:
        """Calculate additional fee for thorough cleaning."""
        return PriceRules.THOROUGH_FEE * self.subtotal() if self.thorough else 0.0

    def discount(self) -> float:
        """Calculate senior discount."""
        if not self.is_senior:
            return 0.0
        return PriceRules.SENIOR_DISCOUNT * (self.subtotal() + self.service_fee())

    def tax(self) -> float:
        """Calculate sales tax."""
        taxable = (self.subtotal() + self.service_fee()) - self.discount()
        return taxable * PriceRules.TAX_RATE

    def total(self) -> float:
        """Final total including fees, discounts, and tax."""
        return (self.subtotal() + self.service_fee()) - self.discount() + self.tax()


@dataclass
class YardServiceQuote:
    """
    Represents a yard service quote.
    Handles mowing, edging, shrubs, labor, and surcharges.
    """
    yard_sqft: int
    shrubs: int
    start: TimeHM
    end: TimeHM
    is_senior: bool

    def labor_hours(self) -> float:
        """Calculate total labor hours."""
        hours = self.end.as_hours() - self.start.as_hours()
        if hours <= 0:
            raise ValueError("End time must be after start time.")
        return hours

    def hourly_surcharge(self) -> float:
        """Calculate yard size hourly surcharge."""
        return PriceRules.yard_hourly_surcharge(self.yard_sqft)

    def labor_cost(self) -> float:
        """Calculate total labor cost."""
        hourly = PriceRules.labor_rate_base() + self.hourly_surcharge()
        return hourly * self.labor_hours()

    def subtotal(self) -> float:
        """Calculate subtotal before discount and tax."""
        return (
            PriceRules.mowing_cost(self.yard_sqft)
            + PriceRules.edging_cost(self.yard_sqft)
            + PriceRules.shrub_cost(self.shrubs)
            + self.labor_cost()
        )

    def discount(self) -> float:
        """Calculate senior discount."""
        return PriceRules.SENIOR_DISCOUNT * self.subtotal() if self.is_senior else 0.0

    def tax(self) -> float:
        """Calculate sales tax."""
        taxable = self.subtotal() - self.discount()
        return taxable * PriceRules.TAX_RATE

    def total(self) -> float:
        """Final total including discount and tax."""
        return self.subtotal() - self.discount() + self.tax()
