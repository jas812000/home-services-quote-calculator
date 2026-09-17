import builtins

import pytest

from home_services_quote_calculator.app import main
from home_services_quote_calculator.ui import ConsoleUI


@pytest.mark.parametrize(
    ("entered_time", "expected_hour", "expected_minute"),
    [
        ("0700", 7, 0),
        ("700", 7, 0),
        ("07:00", 7, 0),
        ("7:00", 7, 0),
        ("7 am", 7, 0),
        ("7 AM", 7, 0),
        ("7:00 am", 7, 0),
        ("7:00 AM", 7, 0),
        ("7 pm", 19, 0),
        ("7:30 PM", 19, 30),
        ("1900", 19, 0),
        ("19:00", 19, 0),
        ("12 AM", 0, 0),
        ("12 PM", 12, 0),
    ],
)
def test_read_time_accepts_supported_formats(
    monkeypatch,
    entered_time,
    expected_hour,
    expected_minute,
):
    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": entered_time,
    )

    result = ConsoleUI.read_time("Time: ")

    assert result.hour == expected_hour
    assert result.minute == expected_minute


def test_read_time_reprompts_after_invalid_input(monkeypatch, capsys):
    inputs = iter(["25:00", "7:75 PM", "invalid", "7:00 AM"])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    result = ConsoleUI.read_time("Time: ")
    output = capsys.readouterr().out

    assert result.hour == 7
    assert result.minute == 0
    assert output.count("Enter a valid time") == 3


def test_read_int_accepts_valid_integer(monkeypatch):
    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": "5",
    )

    result = ConsoleUI.read_int("Number: ", min_val=0, max_val=10)

    assert result == 5


def test_read_int_reprompts_after_non_integer(monkeypatch, capsys):
    inputs = iter(["abc", "5"])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    result = ConsoleUI.read_int("Number: ")
    output = capsys.readouterr().out

    assert result == 5
    assert "Please enter a valid integer." in output


def test_read_int_reprompts_when_below_minimum(monkeypatch, capsys):
    inputs = iter(["-1", "5"])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    result = ConsoleUI.read_int("Number: ", min_val=0)
    output = capsys.readouterr().out

    assert result == 5
    assert "Enter a value >= 0." in output


def test_read_int_reprompts_when_above_maximum(monkeypatch, capsys):
    inputs = iter(["11", "5"])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    result = ConsoleUI.read_int("Number: ", max_val=10)
    output = capsys.readouterr().out

    assert result == 5
    assert "Enter a value <= 10." in output


def test_read_int_reprompts_when_value_not_allowed(
    monkeypatch,
    capsys,
):
    inputs = iter(["4", "2"])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    result = ConsoleUI.read_int(
        "Selection: ",
        allowed={1, 2, 3, 9},
    )
    output = capsys.readouterr().out

    assert result == 2
    assert "Please enter one of:" in output


def test_cli_exit_option_9_prints_goodbye(capsys, monkeypatch):
    inputs = iter(["9"])

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    main()

    output = capsys.readouterr().out

    assert "Goodbye!" in output


def test_cli_house_flow_prints_breakdown_total_and_exits(
    capsys,
    monkeypatch,
):
    inputs = iter(
        [
            "1",      # Selection
            "25",     # Age
            "1",      # Light cleaning
            "1000",   # House square footage
            "1",      # Carpet rooms
            "1",      # Bathrooms
            "1",      # Rooms to dust
            "n",      # Run another quote?
        ]
    )

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    main()

    output = capsys.readouterr().out

    assert "House breakdown:" in output
    assert "Carpet Cleaning" in output
    assert "Bathroom Cleaning" in output
    assert "Dusting" in output
    assert "House total:" in output
    assert "Goodbye!" in output


def test_cli_yard_flow_prints_breakdown_total_and_exits(
    capsys,
    monkeypatch,
):
    inputs = iter(
        [
            "2",          # Selection
            "25",         # Age
            "1000",       # Yard square footage
            "2",          # Shrubs
            "9:00 AM",    # Start time
            "10:00 AM",   # End time
            "n",          # Run another quote?
        ]
    )

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    main()

    output = capsys.readouterr().out

    assert "Yard breakdown:" in output
    assert "Mowing" in output
    assert "Edging" in output
    assert "Shrub Pruning" in output
    assert "Labor" in output
    assert "Yard total:" in output
    assert "Goodbye!" in output


def test_cli_combined_flow_prints_both_breakdowns_and_total(
    capsys,
    monkeypatch,
):
    inputs = iter(
        [
            "3",          # Selection
            "66",         # Age
            "2",          # Thorough cleaning
            "3542",       # House square footage
            "9",          # Carpet rooms
            "8",          # Bathrooms
            "7",          # Rooms to dust
            "7456",       # Yard square footage
            "19",         # Shrubs
            "0700",       # Start time
            "4:00 PM",    # End time
            "n",          # Run another quote?
        ]
    )

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    main()

    output = capsys.readouterr().out

    assert "House breakdown:" in output
    assert "Yard breakdown:" in output
    assert "Senior Discount" in output
    assert "House total:" in output
    assert "Yard total:" in output
    assert "Combined total:" in output
    assert "Goodbye!" in output


def test_cli_yard_reprompts_when_end_time_is_before_start_time(
    capsys,
    monkeypatch,
):
    inputs = iter(
        [
            "2",          # Selection
            "25",         # Age
            "1000",       # Yard square footage
            "0",          # Shrubs
            "10:00 AM",   # Invalid range start
            "9:00 AM",    # Invalid range end
            "9:00 AM",    # Retry start
            "10:00 AM",   # Retry end
            "n",          # Run another quote?
        ]
    )

    monkeypatch.setattr(
        builtins,
        "input",
        lambda prompt="": next(inputs),
    )

    main()

    output = capsys.readouterr().out

    assert "Invalid yard time range:" in output
    assert "End time must be after start time." in output
    assert "Yard total:" in output
    assert "Goodbye!" in output
