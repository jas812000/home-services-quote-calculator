"""
ui.py

Console user interface.
Handles all input/output so business logic stays clean.
"""

from .quotes import HouseCleaningQuote, YardServiceQuote
from .models import TimeHM


class ConsoleUI:
    """Handles all console interaction."""

    def show_welcome(self) -> None:
        print("House Cleaning and Yard Services\n")
        print("This program provides quotes for house cleaning and yard services.\n")

    def show_services(self):
        """Display available services and pricing."""
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

    def read_int(
        self,
        prompt: str,
        min_val: int | None = None,
        max_val: int | None = None,
        allowed: set[int] | None = None,
        ) -> int:
        """Read and validate integer input."""
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

    def read_yes_no(self, prompt: str) -> bool:
        """Read a yes/no response. Returns True for yes, False for no."""
        while True:
            resp = input(prompt).strip().lower()
            if resp in {"y", "yes"}:
                return True
            if resp in {"n", "no"}:
                return False
            print("Please enter y/yes or n/no.")

    def ask_service_choice(self) -> int:
        """Prompt user to select service type."""
        print("House Cleaning = 1")
        print("Yard Service = 2")
        print("Both = 3")
        print("Exit = 9\n")

        return self.read_int(
            "Selection: ",
            allowed={1, 2, 3, 9}
        )

    def build_house_quote(self, age: int) -> HouseCleaningQuote:
        """Collect inputs and build a house quote."""
        thorough = (self.read_int("Light=1, Thorough=2: ", 1, 2) == 2)
        house_sqft = self.read_int("House square footage: ", 1)
        carpet_rooms = self.read_int("Carpet rooms: ", 0)
        bathrooms = self.read_int("Bathrooms: ", 0)
        dust_rooms = self.read_int("Rooms to dust: ", 0)

        return HouseCleaningQuote(
            house_sqft, carpet_rooms, bathrooms, dust_rooms, thorough, age >= 65
        )

    def build_yard_quote(self, age: int) -> YardServiceQuote:
        """Collect inputs and build a yard quote."""
        yard_sqft = self.read_int("Yard square footage: ", 1)
        shrubs = self.read_int("Number of shrubs: ", 0)

        start = TimeHM(
            self.read_int("Start hour: ", 0, 23),
            self.read_int("Start minute: ", 0, 59)
        )
        end = TimeHM(
            self.read_int("End hour: ", 0, 23),
            self.read_int("End minute: ", 0, 59)
        )

        return YardServiceQuote(yard_sqft, shrubs, start, end, age >= 65)

    def print_total(self, label: str, amount: float):
        """Print formatted total."""
        print(f"\n{label} total: ${amount:.2f}")


    
