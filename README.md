# Home Services Quote Calculator

A modular Python command-line application that calculates cost estimates for residential **house cleaning** and **yard 
services** using structured pricing rules, surcharges, discounts, and tax calculations.

This project demonstrates **object-oriented design**, **separation of concerns**, and **testable system architecture** in a 
small-scale service estimation domain. The application is packaged as a real Python project, includes automated tests, and is 
continuously validated via GitHub Actions.

---

## Problem Overview

Service-based businesses often rely on ad-hoc or spreadsheet-driven estimates that become difficult to maintain as pricing rules 
grow in complexity.

This project models a simplified **service quote engine** that generates deterministic cost estimates based on:

- Property size
- Selected services
- Tiered pricing rules
- Labor costs derived from validated time ranges
- Surcharges
- Senior discounts
- Sales tax

The system is designed for **clarity, correctness, and extensibility**, rather than minimal code size.

---

## Architecture & Design

The application follows a **layered, domain-driven structure** with explicit responsibility boundaries:
```
src/home_services_quote_calculator/
├── app.py # Application orchestration and menu loop
├── ui.py # Console input/output and validation
├── pricing.py # Centralized pricing rules and constants
├── quotes.py # Domain quote models and calculations
└── models.py # Shared value objects (e.g., TimeHM)
```

### Key Design Decisions

**Separation of concerns**  
User interaction, pricing rules, and business calculations are isolated into dedicated modules.

**No global state**  
All data flows through objects, improving testability and predictability.

**Rule centralization**  
Pricing logic is defined in one place (`pricing.py`) to avoid duplication and drift.

**Domain-driven modeling**  
Each quote type encapsulates its own calculations and validation rules.

**Defensive validation**  
Invalid domain states (e.g., end time before start time) are rejected at object creation.

---

## Core Components

### `HouseCleaningQuote`
Handles:
- Tier-based pricing by square footage
- Per-room service costs
- Square-footage surcharges
- Optional thorough-cleaning fees
- Senior discounts and sales tax

### `YardServiceQuote`
Handles:
- Mowing, edging, and shrub services
- Labor cost derived from validated time ranges
- Yard-size-based hourly surcharges
- Senior discounts and sales tax

### `PriceRules`
Defines all pricing constants and rate calculations used throughout the system.

---

## Build & Run

### Requirements
- Python 3.9+

### Setup
```bash
python -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -e ".[dev]"
```

---

## Run
```bash
python -m home_services_quote_calculator
```

---

## Testing
The project includes a fully automated pytest suite:
- Unit tests for domain calculations
- Validation tests for edge cases and error conditions
- CLI smoke tests verifying startup, exit behavior, and output

### Run tests
```bash
pytest
```
All tests pass on a clean checkout and are automatically executed in CI.

---

## Engineering Focus
This project emphasizes:
- Object-oriented design
- Modular, maintainable architecture
- Business-rule-driven computation
- Defensive input and domain validation
- Deterministic, testable logic
- Professional Python packaging
- Continuous integration with automated testing

The codebase is intentionally structured to support future extensions such as:
- Web or GUI interfaces
- Persistent storage
- API-based quote generation
- Externalized configuration

---

## License
This project is licensed under the MIT License. See the [LICENSE](LICENSE) file for details.

---




