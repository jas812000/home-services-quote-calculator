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
