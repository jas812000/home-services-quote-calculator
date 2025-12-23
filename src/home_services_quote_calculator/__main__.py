"""
__main__.py

Package execution entry point.

This module allows the application to be run using:
    python -m home_services_quote_calculator

It delegates execution to the main application entry point.
"""

from .app import main


if __name__ == "__main__":
    main()
