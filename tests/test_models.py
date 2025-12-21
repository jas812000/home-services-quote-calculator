from home_services_quote_calculator.models import TimeHM


def test_timehm_as_hours():
    t = TimeHM(2, 30)
    assert t.as_hours() == 2.5
