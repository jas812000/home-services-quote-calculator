"""
app.py

Program entry point.
Coordinates UI and quote calculations.
"""

from .ui import ConsoleUI


def main():
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

        again = input("\nRun another quote? (y/n): ").strip().lower()
        if again != "y":
            print("Goodbye!")
            return


if __name__ == "__main__":
    main()
