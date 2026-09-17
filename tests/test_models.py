import pytest

from home_services_quote_calculator.models import TimeHM


def test_timehm_as_hours():
    time = TimeHM(2, 30)

    assert time.as_hours() == 2.5


@pytest.mark.parametrize(
    ("hour", "minute"),
    [
        (0, 0),
        (0, 59),
        (23, 0),
        (23, 59),
    ],
)
def test_timehm_accepts_valid_boundaries(hour, minute):
    time = TimeHM(hour, minute)

    assert time.hour == hour
    assert time.minute == minute


@pytest.mark.parametrize("hour", [-1, 24])
def test_timehm_rejects_invalid_hour(hour):
    with pytest.raises(ValueError, match="Hour must be between 0 and 23"):
        TimeHM(hour, 0)


@pytest.mark.parametrize("minute", [-1, 60])
def test_timehm_rejects_invalid_minute(minute):
    with pytest.raises(ValueError, match="Minute must be between 0 and 59"):
        TimeHM(12, minute)
