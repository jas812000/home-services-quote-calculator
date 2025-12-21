import builtins

from home_services_quote_calculator.app import main


def test_cli_exit_option_9_prints_goodbye(capsys, monkeypatch):
    # Sequence:
    # 1) Selection: 9
    inputs = iter(["9"])

    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    main()

    out = capsys.readouterr().out
    assert "Goodbye!" in out


def test_cli_house_flow_prints_total_and_exits(capsys, monkeypatch):
    # Sequence expected by app:
    # Selection -> Age -> Light/Thorough -> House sqft -> Carpet rooms -> Bathrooms -> Dust rooms -> rerun y/n
    inputs = iter([
        "1",     # Selection
        "25",    # Age
        "1",     # Light=1, Thorough=2
        "1000",  # House square footage
        "1",     # Carpet rooms
        "1",     # Bathrooms
        "1",     # Rooms to dust
        "n",     # Run another quote? (y/n)
    ])

    monkeypatch.setattr(builtins, "input", lambda prompt="": next(inputs))
    main()

    out = capsys.readouterr().out
    assert "House total:" in out
    assert "Goodbye!" in out
