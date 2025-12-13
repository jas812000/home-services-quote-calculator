# Home Services Quote Calculator

A modular Python application that calculates cost estimates for residential house cleaning and yard services using structured pricing rules, surcharges, discounts, and tax calculations.

This project demonstrates object-oriented design, separation of concerns, and maintainable system architecture in a small-scale service estimation domain.

---

## Problem Overview

Service-based businesses often rely on ad-hoc or spreadsheet-driven estimates that are difficult to maintain as pricing rules grow in complexity.  
This project models a simplified service-quote engine that calculates accurate cost estimates based on:

- Property size
- Selected services
- Tiered pricing rules
- Labor costs
- Surcharges
- Senior discounts
- Sales tax

The system is designed to be extensible and readable, rather than optimized for minimal code length.

---

## Architecture & Design

The application is structured using clear separation of responsibilities:
```
service-quote-calculator/
│
├── app.py # Application entry point
├── ui.py # Console input/output handling
├── pricing.py # Centralized pricing rules and constants
├── quotes.py # Quote calculation logic
└── models.py # Simple data models
```


### Key Design Decisions

- **Separation of concerns**  
  User interaction, pricing rules, and calculations are isolated into dedicated modules.

- **No global state**  
  All data flows through objects, improving testability and maintainability.

- **Rule centralization**  
  Pricing rules are defined in a single location (`pricing.py`) to avoid duplication.

- **Object-oriented modeling**  
  Each quote type encapsulates its own calculation logic.

---

## Core Components

### `HouseCleaningQuote`
Handles:
- Tier-based pricing by square footage
- Per-room service costs
- Square-footage surcharges
- Optional thorough-cleaning fees
- Senior discounts and tax

### `YardServiceQuote`
Handles:
- Mowing, edging, and shrub services
- Labor time calculation
- Yard-size-based hourly surcharges
- Senior discounts and tax

### `PriceRules`
Defines all pricing constants and rate calculations used throughout the system.

---

## How to Run

Requirements:
- Python 3.9+

Run from the project root:

```bash
python app.py
```
---

## Engineering Focus
This project emphasizes:
- Object-oriented design
- Modular architecture
- Readability and maintainability
- Business-rule-driven computation
- Defensive input handling
- Clear data modeling
The codebase is structured to support future extensions such as:
- GUI or web interfaces
- Persistent storage
- API-based quote generation
- Automated testing

---

## Future Improvements
- Add unit tests for pricing logic
- Persist quotes to file or database
- Introduce a graphical or web-based UI
- Externalize pricing rules to configuration files

---

## License
© 2025 James Stevens. All rights reserved.

This source code is provided for educational, evaluation, and portfolio review purposes.
Permission is granted to clone and run the code locally for non-commercial review.

No permission is granted to copy, modify, redistribute, or use this code in
commercial or production systems without explicit written consent from the author.

---
