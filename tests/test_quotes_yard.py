import pytest

from home_services_quote_calculator.models import TimeHM
from home_services_quote_calculator.quotes import YardServiceQuote


def test_yard_total_non_negative():
    q = YardServiceQuote(
        yard_sqft=100,
        shrubs=0,
        start=TimeHM(9, 0),
        end=TimeHM(10, 0),
        is_senior=False,
    )
    assert q.total() >= 0


def test_yard_senior_discount_reduces_total():
    non_senior = YardServiceQuote(
        yard_sqft=200,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(11, 0),
        is_senior=False,
    )
    senior = YardServiceQuote(
        yard_sqft=200,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(11, 0),
        is_senior=True,
    )
    assert senior.total() < non_senior.total()


def test_yard_invalid_time_raises():
    # End time must be after start time
    with pytest.raises(ValueError):
        YardServiceQuote(
            yard_sqft=200,
            shrubs=1,
            start=TimeHM(10, 0),
            end=TimeHM(9, 0),
            is_senior=False,
        )
