"""
pricing.py

Centralized pricing rules and constants.

This module defines all pricing-related business rules used by the
application, including tax rates, discounts, service fees, and
calculation logic for both house cleaning and yard services.

Keeping pricing logic here ensures consistency and prevents duplication
across quote types.
"""

import math


class PriceRules:
    """
    Static pricing rules for house cleaning and yard services.

    This class contains only constants and pure functions. It maintains
    no internal state and should not be instantiated.
    """

    # ---- Global rates ----
    TAX_RATE = 0.08
    """Sales tax rate applied to taxable service totals."""

    SENIOR_DISCOUNT = 0.15
    """Discount percentage applied for senior customers."""

    THOROUGH_FEE = 0.10
    """Additional percentage fee for thorough (deep) house cleaning."""

    # ---- House pricing ----
    @staticmethod
    def house_tier(house_sqft: int) -> str:
        """
        Determine the pricing tier based on house square footage.

        Args:
            house_sqft (int): Total square footage of the house.

        Returns:
            str: One of "small", "medium", or "large".
        """
        if house_sqft <= 1200:
            return "small"
        if house_sqft <= 2000:
            return "medium"
        return "large"

    @staticmethod
    def carpet_rate(tier: str) -> float:
        """
        Return the carpet cleaning rate per room for a given tier.

        Args:
            tier (str): House size tier.

        Returns:
            float: Price per carpeted room.
        """
        return {"small": 100.0, "medium": 200.0, "large": 300.0}[tier]

    @staticmethod
    def bathroom_rate(tier: str) -> float:
        """
        Return the bathroom cleaning rate per bathroom for a given tier.

        Args:
            tier (str): House size tier.

        Returns:
            float: Price per bathroom.
        """
        return {"small": 80.0, "medium": 100.0, "large": 120.0}[tier]

    @staticmethod
    def dust_rate(tier: str) -> float:
        """
        Return the dusting rate per room for a given tier.

        Args:
            tier (str): House size tier.

        Returns:
            float: Price per dusted room.
        """
        return {"small": 60.0, "medium": 80.0, "large": 100.0}[tier]

    @staticmethod
    def house_sqft_surcharge(house_sqft: int) -> float:
        """
        Calculate a square-footage surcharge for large houses.

        Houses over 3,000 square feet incur a per-square-foot surcharge.

        Args:
            house_sqft (int): Total square footage of the house.

        Returns:
            float: Additional surcharge amount.
        """
        return (house_sqft - 3000) * 2.5 if house_sqft > 3000 else 0.0

    # ---- Yard pricing ----
    @staticmethod
    def mowing_cost(yard_sqft: int) -> float:
        """
        Calculate the mowing cost based on yard size.

        Args:
            yard_sqft (int): Total square footage of the yard.

        Returns:
            float: Total mowing cost.
        """
        return yard_sqft * 6.0

    @staticmethod
    def edging_cost(yard_sqft: int) -> float:
        """
        Calculate edging cost based on an estimated yard perimeter.

        The yard is assumed to be approximately square. The perimeter
        is estimated using the square root of the area.

        Args:
            yard_sqft (int): Total square footage of the yard.

        Returns:
            float: Total edging cost.
        """
        perimeter = math.sqrt(yard_sqft) * 4
        return perimeter * 4.0

    @staticmethod
    def shrub_cost(shrubs: int) -> float:
        """
        Calculate shrub pruning cost.

        Args:
            shrubs (int): Number of shrubs to be trimmed.

        Returns:
            float: Total shrub pruning cost.
        """
        return shrubs * 25.0

    @staticmethod
    def yard_hourly_surcharge(yard_sqft: int) -> float:
        """
        Calculate the hourly labor surcharge for large yards.

        Yards over 5,000 square feet incur an additional hourly surcharge,
        charged in 2,000 square foot increments.

        Args:
            yard_sqft (int): Total square footage of the yard.

        Returns:
            float: Hourly surcharge amount.
        """
        if yard_sqft <= 5000:
            return 0.0
        increments = math.ceil((yard_sqft - 5000) / 2000)
        return increments * 35.0

    @staticmethod
    def labor_rate_base() -> float:
        """
        Return the base hourly labor rate for yard services.

        Returns:
            float: Base hourly labor rate.
        """
        return 80.0
