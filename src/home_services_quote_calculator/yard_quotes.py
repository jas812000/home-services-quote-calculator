"""
yard_quotes.py

Yard service quote domain model.
"""

from dataclasses import dataclass
from .pricing import PriceRules
from .models import TimeHM


@dataclass
class YardServiceQuote:
    """
    Represents a yard maintenance service quote.

    This class handles pricing for lawn mowing, edging, shrub trimming,
    labor costs, yard-size surcharges, discounts, and tax calculations.
    """

    yard_sqft: int
    """Total square footage of the yard."""

    shrubs: int
    """Number of shrubs to be trimmed."""

    start: TimeHM
    """Service start time."""

    end: TimeHM
    """Service end time."""

    is_senior: bool
    """Whether the customer qualifies for a senior discount."""

    def labor_hours(self) -> float:
        """
        Calculate total labor time in hours.

        Returns:
            float: Number of labor hours worked.

        Raises:
            ValueError: If the end time is not after start time.
        """
        hours = self.end.as_hours() - self.start.as_hours()
        if hours <= 0:
            raise ValueError("End time must be after start time.")
        return hours

    def hourly_surcharge(self) -> float:
        """
        Calculate the hourly surcharge based on yard size.

        Returns:
            float: Additional hourly surcharge.
        """
        return PriceRules.yard_hourly_surcharge(self.yard_sqft)

    def labor_cost(self) -> float:
        """
        Calculate total labor cost including surcharges.

        Returns:
            float: Total labor cost.
        """
        hourly = PriceRules.labor_rate_base() + self.hourly_surcharge()
        return hourly * self.labor_hours()

    def subtotal(self) -> float:
        """
        Calculate subtotal before discounts and tax.

        Returns:
            float: Subtotal service cost.
        """
        return (
            PriceRules.mowing_cost(self.yard_sqft)
            + PriceRules.edging_cost(self.yard_sqft)
            + PriceRules.shrub_cost(self.shrubs)
            + self.labor_cost()
        )

    def discount(self) -> float:
        """
        Calculate the senior discount.

        Returns:
            float: Discount amount, or 0.0 if not eligible.
        """
        return PriceRules.SENIOR_DISCOUNT * self.subtotal() if self.is_senior else 0.0

    def tax(self) -> float:
        """
        Calculate sales tax on the taxable portion of the quote.

        Returns:
            float: Calculated tax amount.
        """
        taxable = self.subtotal() - self.discount()
        return taxable * PriceRules.TAX_RATE

    def total(self) -> float:
        """
        Calculate the final quote total.

        Returns:
            float: Final price including discounts and tax.
        """
        return self.subtotal() - self.discount() + self.tax()

    def items(self) -> list[tuple[str, float]]:
        """
        Return an itemized cost breakdown for the yard service quote.

        Returns:
            list[tuple[str, float]]: Line items and their costs.
        """
        items: list[tuple[str, float]] = [
            ("Mowing", PriceRules.mowing_cost(self.yard_sqft)),
            ("Edging", PriceRules.edging_cost(self.yard_sqft)),
            ("Shrub pruning", PriceRules.shrub_cost(self.shrubs)),
            ("Labor", self.labor_cost()),
        ]

        if self.is_senior:
            items.append(("Senior discount", -self.discount()))

        items.append(("Tax", self.tax()))

        return items
    
    def __post_init__(self) -> None:
        start_minutes = self.start.hour * 60 + self.start.minute
        end_minutes = self.end.hour * 60 + self.end.minute
        if end_minutes <= start_minutes:
            raise ValueError("end must be after start")
   

