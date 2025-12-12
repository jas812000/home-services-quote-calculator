"""
pricing.py

Centralized pricing rules and constants.
All dollar amounts, rates, and tier logic live here so they are not
duplicated across the application.
"""

import math


class PriceRules:
    """
    Static pricing rules for house cleaning and yard services.
    No state is stored here—this class only defines business rules.
    """

    # ---- Global rates ----
    TAX_RATE = 0.08
    SENIOR_DISCOUNT = 0.15
    THOROUGH_FEE = 0.10

    # ---- House pricing ----
    @staticmethod
    def house_tier(house_sqft: int) -> str:
        """Return house size tier based on square footage."""
        if house_sqft <= 1200:
            return "small"
        if house_sqft <= 2000:
            return "medium"
        return "large"

    @staticmethod
    def carpet_rate(tier: str) -> float:
        """Return carpet cleaning price per room."""
        return {"small": 100.0, "medium": 200.0, "large": 300.0}[tier]

    @staticmethod
    def bathroom_rate(tier: str) -> float:
        """Return bathroom cleaning price per room."""
        return {"small": 80.0, "medium": 100.0, "large": 120.0}[tier]

    @staticmethod
    def dust_rate(tier: str) -> float:
        """Return dusting price per room."""
        return {"small": 60.0, "medium": 80.0, "large": 100.0}[tier]

    @staticmethod
    def house_sqft_surcharge(house_sqft: int) -> float:
        """Calculate surcharge for houses over 3,000 square feet."""
        return (house_sqft - 3000) * 2.5 if house_sqft > 3000 else 0.0

    # ---- Yard pricing ----
    @staticmethod
    def mowing_cost(yard_sqft: int) -> float:
        """Calculate mowing cost based on yard size."""
        return yard_sqft * 6.0

    @staticmethod
    def edging_cost(yard_sqft: int) -> float:
        """
        Calculate edging cost.
        Yard perimeter is approximated using square root of area.
        """
        perimeter = math.sqrt(yard_sqft) * 4
        return perimeter * 4.0

    @staticmethod
    def shrub_cost(shrubs: int) -> float:
        """Calculate shrub pruning cost."""
        return shrubs * 25.0

    @staticmethod
    def yard_hourly_surcharge(yard_sqft: int) -> float:
        """
        Calculate hourly surcharge for yards over 5,000 square feet.
        Charged in 2,000 sq ft increments.
        """
        if yard_sqft <= 5000:
            return 0.0
        increments = math.ceil((yard_sqft - 5000) / 2000)
        return increments * 35.0

    @staticmethod
    def labor_rate_base() -> float:
        """Base hourly labor rate for yard services."""
        return 80.0
