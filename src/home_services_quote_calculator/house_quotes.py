"""
house_quotes.py

House cleaning quote domain model.
"""

from dataclasses import dataclass

from .pricing import PriceRules


@dataclass
class HouseCleaningQuote:
    """
    Represents a house cleaning service quote.

    This class models all inputs required for a residential cleaning
    service and provides methods to compute subtotals, service fees,
    discounts, tax, and final totals.
    """

    house_sqft: int
    """Total square footage of the house."""

    carpet_rooms: int
    """Number of carpeted rooms."""

    bathrooms: int
    """Number of bathrooms to be cleaned."""

    dust_rooms: int
    """Number of rooms requiring dusting."""

    thorough: bool
    """Whether a thorough (deep) cleaning is requested."""

    is_senior: bool
    """Whether the customer qualifies for a senior discount."""

    def __post_init__(self) -> None:
        """Validate house cleaning quote inputs."""
        if self.house_sqft <= 0:
            raise ValueError("House square footage must be greater than 0.")

        if self.carpet_rooms < 0:
            raise ValueError("Carpet rooms cannot be negative.")

        if self.bathrooms < 0:
            raise ValueError("Bathrooms cannot be negative.")

        if self.dust_rooms < 0:
            raise ValueError("Dust rooms cannot be negative.")

    def tier(self) -> str:
        """
        Determine the pricing tier based on house size.

        Returns:
            str: Pricing tier identifier as defined by PriceRules.
        """
        return PriceRules.house_tier(self.house_sqft)

    def subtotal(self) -> float:
        """
        Calculate the base service cost before fees, discounts, and tax.

        Returns:
            float: Subtotal cost for cleaning services.
        """
        t = self.tier()
        return (
            self.carpet_rooms * PriceRules.carpet_rate(t)
            + self.bathrooms * PriceRules.bathroom_rate(t)
            + self.dust_rooms * PriceRules.dust_rate(t)
            + PriceRules.house_sqft_surcharge(self.house_sqft)
        )

    def service_fee(self) -> float:
        """
        Calculate the additional fee for thorough cleaning.

        Returns:
            float: Additional service fee, or 0.0 if not applicable.
        """
        return PriceRules.THOROUGH_FEE * self.subtotal() if self.thorough else 0.0

    def discount(self) -> float:
        """
        Calculate the senior discount amount.

        Returns:
            float: Discount amount, or 0.0 if not eligible.
        """
        if not self.is_senior:
            return 0.0
        return PriceRules.SENIOR_DISCOUNT * (self.subtotal() + self.service_fee())

    def tax(self) -> float:
        """
        Calculate sales tax on the taxable portion of the quote.

        Returns:
            float: Calculated tax amount.
        """
        taxable = (self.subtotal() + self.service_fee()) - self.discount()
        return taxable * PriceRules.TAX_RATE

    def total(self) -> float:
        """
        Calculate the final quote total.

        Returns:
            float: Final price including fees, discounts, and tax.
        """
        return (self.subtotal() + self.service_fee()) - self.discount() + self.tax()

    def items(self) -> list[tuple[str, str, float]]:
        """
        Return an itemized cost breakdown for the house cleaning quote.

        Returns:
            list[tuple[str, str, float]]: Service, calculation detail, and cost.
        """
        tier = self.tier()

        carpet_rate = PriceRules.carpet_rate(tier)
        bathroom_rate = PriceRules.bathroom_rate(tier)
        dust_rate = PriceRules.dust_rate(tier)

        items: list[tuple[str, str, float]] = [
            (
                "Carpet Cleaning",
                f"{self.carpet_rooms} rooms × ${carpet_rate:,.2f}",
                self.carpet_rooms * carpet_rate,
            ),
            (
                "Bathroom Cleaning",
                f"{self.bathrooms} {'bathroom' if self.bathrooms == 1 else 'bathrooms'} × ${bathroom_rate:,.2f}",
                self.bathrooms * bathroom_rate,
            ),
            (
                "Dusting",
                f"{self.dust_rooms} rooms × ${dust_rate:,.2f}",
                self.dust_rooms * dust_rate,
            ),
        ]

        sqft_surcharge = PriceRules.house_sqft_surcharge(self.house_sqft)
        if sqft_surcharge > 0:
            excess_sqft = self.house_sqft - 3000
            items.append(
                (
                    "Large House Surcharge",
                    f"{excess_sqft:,} sq ft × $2.50",
                    sqft_surcharge,
                )
            )

        if self.thorough:
            items.append(
                (
                    "Thorough Cleaning Fee",
                    f"{PriceRules.THOROUGH_FEE:.0%} of ${self.subtotal():,.2f}",
                    self.service_fee(),
                )
            )

        if self.is_senior:
            discount_base = self.subtotal() + self.service_fee()
            items.append(
                (
                    "Senior Discount",
                    f"{PriceRules.SENIOR_DISCOUNT:.0%} of ${discount_base:,.2f}",
                    -self.discount(),
                )
            )

        taxable = (self.subtotal() + self.service_fee()) - self.discount()
        items.append(
            (
                "Tax",
                f"{PriceRules.TAX_RATE:.0%} of ${taxable:,.2f}",
                self.tax(),
            )
        )

        return items