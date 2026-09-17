"""
yard_quotes.py

Yard service quote domain model.
"""

import math
from dataclasses import dataclass

from .models import TimeHM
from .pricing import PriceRules


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
        """
        return self.end.as_hours() - self.start.as_hours()

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

    def items(self) -> list[tuple[str, str, float]]:
        """
        Return an itemized cost breakdown for the yard service quote.

        Returns:
            list[tuple[str, str, float]]: Service, calculation detail, and cost.
        """
        perimeter = PriceRules.estimated_yard_perimeter(self.yard_sqft)
        labor_hours = self.labor_hours()
        base_labor_rate = PriceRules.labor_rate_base()
        hourly_surcharge = self.hourly_surcharge()

        items: list[tuple[str, str, float]] = [
            (
                "Mowing",
                f"$45 base + {math.ceil(self.yard_sqft / 1000)} × $15 per 1,000 sq ft",
                PriceRules.mowing_cost(self.yard_sqft),
            ),
            (
                "Edging",
                f"{perimeter:,.1f} estimated linear ft × $4.00",
                PriceRules.edging_cost(self.yard_sqft),
            ),
            (
                "Shrub Pruning",
                f"{self.shrubs} shrubs × $25.00",
                PriceRules.shrub_cost(self.shrubs),
            ),
            (
                "Labor",
                f"{labor_hours:.2f} hr × ${base_labor_rate:,.2f}/hr",
                labor_hours * base_labor_rate,
            ),
        ]

        if hourly_surcharge > 0:
            items.append(
                (
                    "Large Yard Surcharge",
                    f"{labor_hours:.2f} hr × ${hourly_surcharge:,.2f}/hr",
                    labor_hours * hourly_surcharge,
                )
            )

        if self.is_senior:
            items.append(
                (
                    "Senior Discount",
                    f"{PriceRules.SENIOR_DISCOUNT:.0%} of ${self.subtotal():,.2f}",
                    -self.discount(),
                )
            )

        taxable = self.subtotal() - self.discount()
        items.append(
            (
                "Tax",
                f"{PriceRules.TAX_RATE:.0%} of ${taxable:,.2f}",
                self.tax(),
            )
        )

        return items

    def __post_init__(self) -> None:
        """Validate yard service quote inputs."""
        if self.yard_sqft <= 0:
            raise ValueError("Yard square footage must be greater than 0.")

        if self.shrubs < 0:
            raise ValueError("Shrub count cannot be negative.")

        if self.end.as_hours() <= self.start.as_hours():
            raise ValueError("End time must be after start time.")
