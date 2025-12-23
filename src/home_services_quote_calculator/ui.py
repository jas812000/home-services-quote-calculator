"""
ui.py

Console user interface.

This module contains the console-based UI layer for the application.
It is responsible for all user interaction (printing menus, reading input,
and displaying results) so that business logic remains separate.
"""

from .house_quotes import HouseCleaningQuote
from .yard_quotes import YardServiceQuote
from .models import TimeHM


class ConsoleUI:
    """Console user interface for collecting inputs and displaying quotes."""

    @staticmethod
    def show_welcome() -> None:
        """
        Display the program welcome message.

        Returns:
            None
        """
        print("House Cleaning and Yard Services\n")
        print("This program provides quotes for house cleaning and yard services.\n")

    @staticmethod
    def show_services() -> None:
        """
        Display available services and example pricing.

        Notes:
            These lines are informational. Actual pricing calculations are handled by
            the pricing/quote domain logic.
        """
        print("\nHouse Services:")
        print("Carpet Cleaning: Small $100 | Medium $200 | Large $300")
        print("Bathroom Cleaning: Small $80 | Medium $100 | Large $120")
        print("Dusting: Small $60 | Medium $80 | Large $100")
        print("Surcharge: $2.50 per sq ft over 3,000\n")
        print("Yard Services:")
        print("Mowing: $6.00 per sq ft")
        print("Edging: $4.00 per linear ft")
        print("Shrub Pruning: $25 per shrub")
        print("Labor: $80/hr + surcharge for large yards\n")

    @staticmethod
    def read_int(
        prompt: str,
        min_val: int | None = None,
        max_val: int | None = None,
        allowed: set[int] | None = None,
    ) -> int:
        """
        Read an integer from stdin and validate it.

        The value can be constrained by:
        - a minimum value (min_val),
        - a maximum value (max_val),
        - and/or membership in an allowed set.

        Args:
            prompt (str): Prompt text shown to the user.
            min_val (int | None): Minimum allowed value (inclusive), if provided.
            max_val (int | None): Maximum allowed value (inclusive), if provided.
            allowed (set[int] | None): Explicit allowed values. If provided, min/max
                checks are not applied.

        Returns:
            int: A validated integer input from the user.
        """
        while True:
            try:
                v = int(input(prompt))

                if allowed is not None:
                    if v not in allowed:
                        print(f"Please enter one of: {sorted(allowed)}")
                        continue
                    return v

                if min_val is not None and v < min_val:
                    print(f"Enter a value >= {min_val}.")
                    continue

                if max_val is not None and v > max_val:
                    print(f"Enter a value <= {max_val}.")
                    continue

                return v

            except ValueError:
                print("Please enter a valid integer.")

        raise RuntimeError("Unreachable code")

    @staticmethod
    def read_yes_no(prompt: str) -> bool:
        """
        Read a yes/no response from stdin.

        Args:
            prompt (str): Prompt text shown to the user.

        Returns:
            bool: True for yes (y/yes), False for no (n/no).
        """
        while True:
            resp = input(prompt).strip().lower()
            if resp in {"y", "yes"}:
                return True
            if resp in {"n", "no"}:
                return False
            print("Please enter y/yes or n/no.")

    def ask_service_choice(self) -> int:
        """
        Prompt the user to select a service type.

        Returns:
            int: Service selection code (1, 2, 3, or 9).
        """
        print("House Cleaning = 1")
        print("Yard Service = 2")
        print("Both = 3")
        print("Exit = 9\n")

        return self.read_int("Selection: ", allowed={1, 2, 3, 9})

    def build_house_quote(self, age: int) -> HouseCleaningQuote:
        """
        Collect inputs and create a HouseCleaningQuote.

        Args:
            age (int): Customer age used to determine senior discount eligibility.

        Returns:
            HouseCleaningQuote: Fully populated quote object.
        """
        thorough = self.read_int("Light=1, Thorough=2: ", 1, 2) == 2
        house_sqft = self.read_int("House square footage: ", 1)
        carpet_rooms = self.read_int("Carpet rooms: ", 0)
        bathrooms = self.read_int("Bathrooms: ", 0)
        dust_rooms = self.read_int("Rooms to dust: ", 0)

        return HouseCleaningQuote(
            house_sqft=house_sqft,
            carpet_rooms=carpet_rooms,
            bathrooms=bathrooms,
            dust_rooms=dust_rooms,
            thorough=thorough,
            is_senior=age >= 65,
        )

    def build_yard_quote(self, age: int) -> YardServiceQuote:
        """
        Collect inputs and create a YardServiceQuote.

        Args:
            age (int): Customer age used to determine senior discount eligibility.

        Returns:
            YardServiceQuote: Fully populated quote object.
        """
        yard_sqft = self.read_int("Yard square footage: ", 1)
        shrubs = self.read_int("Number of shrubs: ", 0)

        start = TimeHM(
            self.read_int("Start hour: ", 0, 23),
            self.read_int("Start minute: ", 0, 59),
        )
        end = TimeHM(
            self.read_int("End hour: ", 0, 23),
            self.read_int("End minute: ", 0, 59),
        )

        return YardServiceQuote(
            yard_sqft=yard_sqft,
            shrubs=shrubs,
            start=start,
            end=end,
            is_senior=age >= 65,
        )

    @staticmethod
    def print_itemized(title: str, items: list[tuple[str, float]]) -> None:
        """
        Print an itemized list of charges.

        Args:
            title (str): Title of the quote section.
            items (list[tuple[str, float]]): Itemized charges as (label, amount).
        """
        print(f"\n{title} breakdown:")
        for label, amount in items:
            sign = "-" if amount < 0 else ""
            print(f"  {label:<25} {sign}${abs(amount):.2f}")

    @staticmethod
    def print_total(label: str, amount: float) -> None:
        """
        Print a formatted total amount.

        Args:
            label (str): Label describing the total (e.g., "House Cleaning").
            amount (float): Amount to display.

        Returns:
            None
        """
        print(f"\n{label} total: ${amount:.2f}")
