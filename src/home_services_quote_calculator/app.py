"""
app.py

Program entry point.
Coordinates UI and quote calculations.
"""

from .ui import ConsoleUI


def main():
    ui = ConsoleUI()
    ui.show_welcome()
    ui.show_services()

    choice = ui.ask_service_choice()

    if choice == 1:
        house = ui.build_house_quote()
        ui.print_total("House", house.total())
    elif choice == 2:
        yard = ui.build_yard_quote()
        ui.print_total("Yard", yard.total())
    else:
        house = ui.build_house_quote()
        yard = ui.build_yard_quote()
        ui.print_total("Combined", house.total() + yard.total())


if __name__ == "__main__":
    main()
