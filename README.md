# Home Services Quote Calculator

A modular Python command-line application that calculates cost estimates
for residential **house cleaning** and **yard services** using
structured pricing rules, surcharges, discounts, labor costs, and tax
calculations.

This project demonstrates **object-oriented design**, **separation of
concerns**, **domain validation**, **automated testing**, and **Python
packaging** in a small service-estimation domain. The application
includes an installable command-line entry point and is continuously
validated through GitHub Actions.

------------------------------------------------------------------------

## Application Preview

### House-Cleaning Quote

![House-Cleaning Quote](docs/screenshots/house-cleaning.png)

The application produces itemized estimates based on property size,
selected services, pricing rules, surcharges, discounts, and tax.

Additional screenshots demonstrate the complete command-line workflow:

-   [Main Menu](docs/screenshots/main-menu.png)
-   [Yard-Service Quote](docs/screenshots/yard-service.png)
-   [Combined House and Yard
    Quote](docs/screenshots/combined-service.png)
-   [Input Validation](docs/screenshots/input-validation.png)
-   [View All Application Screenshots](docs/screenshots/README.md)

------------------------------------------------------------------------

## Problem Overview

Service-based businesses often rely on ad-hoc or spreadsheet-driven
estimates that become difficult to maintain as pricing rules grow in
complexity.

This project models a simplified **service quote engine** that generates
deterministic cost estimates based on:

-   Property size
-   Selected services
-   Tiered pricing rules
-   Labor costs derived from validated time ranges
-   Property-size surcharges
-   Senior discounts
-   Sales tax

The system is designed for **clarity, correctness, and extensibility**,
rather than minimal code size.

------------------------------------------------------------------------

## Architecture & Design

The application separates console interaction, application
orchestration, pricing rules, and domain calculations into focused
modules:

``` text
src/home_services_quote_calculator/
├── __init__.py
├── __main__.py       # Package execution entry point
├── app.py            # Application orchestration and menu loop
├── ui.py             # Console input/output and input validation
├── models.py         # Shared value objects such as TimeHM
├── pricing.py        # Centralized pricing rules and calculations
├── house_quotes.py   # House-cleaning quote domain model
├── yard_quotes.py    # Yard-service quote domain model
└── quotes.py         # Public quote-model re-exports
```

### Key Design Decisions

**Separation of concerns**\
User interaction, application flow, pricing rules, and business
calculations are isolated into dedicated modules.

**No global application state**\
Quote data flows through domain objects, improving predictability and
testability.

**Centralized pricing rules**\
Shared pricing constants and calculations are maintained in `pricing.py`
to reduce duplication and pricing-rule drift.

**Domain-focused models**\
`HouseCleaningQuote` and `YardServiceQuote` encapsulate the calculations
and validation rules associated with their respective services.

**Defensive validation**\
Invalid domain states, including non-positive property sizes, negative
service quantities, invalid times, and yard-service end times that do
not occur after their start times, are rejected before calculations
proceed.

------------------------------------------------------------------------

## Core Components

### `HouseCleaningQuote`

Calculates house-cleaning estimates using:

-   Property-size pricing tiers
-   Carpet cleaning
-   Bathroom cleaning
-   Dusting
-   Large-property square-footage surcharges
-   Optional thorough-cleaning fees
-   Senior discounts
-   Sales tax

### `YardServiceQuote`

Calculates yard-service estimates using:

-   Mowing with a base charge plus size-based increments
-   Edging based on an estimated square-yard perimeter
-   Shrub pruning
-   Labor duration derived from validated start and end times
-   Large-yard hourly surcharges
-   Senior discounts
-   Sales tax

### `PriceRules`

Centralizes pricing constants and shared calculations used by the quote
models, keeping pricing policy separate from application and
user-interface logic.

### `TimeHM`

Represents validated hours and minutes used by yard-service labor
calculations. The CLI accepts several common 12-hour and 24-hour time
formats and converts them into this domain value object.

------------------------------------------------------------------------

## Requirements

-   Python 3.11+

------------------------------------------------------------------------

## Setup

Clone the repository and create a virtual environment:

``` bash
python -m venv .venv
source .venv/bin/activate
```

Install the project and development dependencies:

``` bash
python -m pip install --upgrade pip
python -m pip install -e ".[dev]"
```

------------------------------------------------------------------------

## Run

After installation, run the application using the console entry point:

``` bash
home-services-quote
```

The package can also be executed directly:

``` bash
python -m home_services_quote_calculator
```

The application supports house-cleaning quotes, yard-service quotes, or
a combined estimate.

------------------------------------------------------------------------

## Testing

The project includes **91 automated pytest tests** covering:

-   House-cleaning pricing calculations
-   Yard-service pricing calculations
-   Pricing boundaries and surcharges
-   Discounts and tax calculations
-   Domain validation and invalid states
-   Time validation and supported input formats
-   CLI input handling and retry behavior
-   House, yard, and combined CLI workflows

Run the complete test suite with:

``` bash
./scripts/test.sh
```

Tests can also be executed directly with:

``` bash
python -m pytest
```

------------------------------------------------------------------------

## Code Quality

[Ruff](https://docs.astral.sh/ruff/) is used for static analysis and
Python code-quality checks.

Run Ruff with:

``` bash
python -m ruff check src tests
```

------------------------------------------------------------------------

## Build

The project uses `pyproject.toml` and setuptools for Python packaging.

Build the source distribution and wheel with:

``` bash
python -m build
```

Successful builds are written to the `dist/` directory.

------------------------------------------------------------------------

## Continuous Integration

GitHub Actions validates the project on pushes and pull requests to
`main`.

The CI workflow:

1.  Checks out the repository
2.  Configures Python 3.11
3.  Installs the project and development dependencies
4.  Runs Ruff static analysis
5.  Runs the automated pytest suite

This ensures both code-quality checks and behavioral tests must pass
during normal repository development.

------------------------------------------------------------------------

## Engineering Focus

This project emphasizes:

-   Object-oriented design
-   Modular application architecture
-   Separation of concerns
-   Business-rule-driven computation
-   Defensive input and domain validation
-   Deterministic, testable logic
-   Automated unit and CLI testing
-   Python packaging and console entry points
-   Static code-quality analysis
-   Continuous integration

The architecture also leaves room for future extensions such as
persistent storage, alternative user interfaces, API-based quote
generation, or externally configured pricing rules.

------------------------------------------------------------------------

## License

This project is licensed under the MIT License. See the
[LICENSE](LICENSE) file for details.
