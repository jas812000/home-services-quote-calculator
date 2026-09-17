"""
ui.py

Console user interface.

This module contains the console-based UI layer for the application.
It is responsible for all user interaction (printing menus, reading input,
and displaying results) so that business logic remains separate.
"""

from .house_quotes import HouseCleaningQuote
from .models import TimeHM
from .yard_quotes import YardServiceQuote


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
        print("Mowing: $45 base + $15 per 1,000 sq ft (rounded up)")
        print("Edging: $4.00 per estimated linear ft (based on yard square footage)")
        print("Shrub Pruning: $25 per shrub")
        print("Labor: $80/hr + $35/hr per 2,000 sq ft increment over 5,000 sq ft\n")

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
                value = int(input(prompt))
            except ValueError:
                print("Please enter a valid integer.")
                continue

            if allowed is not None and value not in allowed:
                print(f"Please enter one of: {sorted(allowed)}")
                continue

            if allowed is None:
                if min_val is not None and value < min_val:
                    print(f"Enter a value >= {min_val}.")
                    continue

                if max_val is not None and value > max_val:
                    print(f"Enter a value <= {max_val}.")
                    continue

            return value

    @staticmethod
    def read_time(prompt: str) -> TimeHM:
        """
        Read a time in common 12-hour or 24-hour formats.

        Examples:
            0700
            07:00
            7 am
            7:00 am
            7 AM
            7:00 AM
            1900
            19:00

        Args:
            prompt (str): Prompt text shown to the user.

        Returns:
            TimeHM: Validated time converted to 24-hour representation.
        """
        while True:
            value = input(prompt).strip().upper()

            try:
                period = None

                if value.endswith(("AM", "PM")):
                    period = value[-2:]
                    value = value[:-2].strip()

                if ":" in value:
                    hour_text, minute_text = value.split(":", 1)
                    hour = int(hour_text)
                    minute = int(minute_text)
                else:
                    digits = value.replace(" ", "")

                    if not digits.isdigit():
                        raise ValueError

                    if period is not None and len(digits) <= 2:
                        hour = int(digits)
                        minute = 0
                    elif len(digits) in {3, 4}:
                        hour = int(digits[:-2])
                        minute = int(digits[-2:])
                    else:
                        raise ValueError

                if not 0 <= minute <= 59:
                    raise ValueError

                if period is not None:
                    if not 1 <= hour <= 12:
                        raise ValueError

                    if period == "AM":
                        hour = 0 if hour == 12 else hour
                    else:
                        hour = 12 if hour == 12 else hour + 12
                elif not 0 <= hour <= 23:
                    raise ValueError

                return TimeHM(hour, minute)

            except ValueError:
                print(
                    "Enter a valid time, such as 0700, 07:00, "
                    "7 AM, or 7:00 AM."
                )

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
            is_senior=age >= 65
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

        while True:
            start = self.read_time("Start time (e.g., 7:00 AM): ")
            end = self.read_time("End time (e.g., 4:00 PM): ")

            try:        
                return YardServiceQuote(
                    yard_sqft=yard_sqft,
                    shrubs=shrubs,
                    start=start,
                    end=end,
                    is_senior=age >= 65,
                )
            except ValueError:
                print("\nInvalid yard time range:")
                print("End time must be after start time.")
                print("Try again.\n")

    @staticmethod
    def print_itemized(title: str, items: list[tuple[str, str, float]]) -> None:
        """
        Print an itemized list of charges.

        Args:
            title (str): Title of the quote section.
            items (list[tuple[str, str, float]]): Service, calculation detail,
                and amount for each charge.
        """
        print(f"\n{title} breakdown:")

        for label, calculation, amount in items:
            formatted_amount = f"${abs(amount):,.2f}"
            if amount < 0:
                formatted_amount = f"-{formatted_amount}"

            print(f"  {label:<24} {calculation:<38} {formatted_amount:>12}")

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
        print(f"\n{label} total: ${amount:,.2f}")
