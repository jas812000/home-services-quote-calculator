"""
app.py

Program entry point.

This module coordinates the console user interface and quote calculation
logic. It drives the main application loop and handles high-level program
flow.
"""

from .ui import ConsoleUI


def main() -> None:
    """
    Run the application main loop.

    This function initializes the console UI, prompts the user for service
    selections and input data, generates service quotes, and displays
    calculated totals. The loop continues until the user chooses to exit.

    Returns:
        None
    """
    ui = ConsoleUI()
    ui.show_welcome()

    while True:
        ui.show_services()
        choice = ui.ask_service_choice()

        if choice == 9:
            print("Goodbye!")
            return

        age = ui.read_int("Age: ", 0, 120)

        if choice == 1:
            house = ui.build_house_quote(age)
            ui.print_total("House", house.total())
        elif choice == 2:
            yard = ui.build_yard_quote(age)
            ui.print_total("Yard", yard.total())
        elif choice == 3:
            house = ui.build_house_quote(age)
            yard = ui.build_yard_quote(age)
            ui.print_total("Combined", house.total() + yard.total())

        if not ui.read_yes_no("\nRun another quote? (y/n): "):
            print("Goodbye!")
            return


if __name__ == "__main__":
    main()
