from home_services_quote_calculator.quotes import HouseCleaningQuote


def test_house_total_non_negative():
    q = HouseCleaningQuote(
        house_sqft=1000,
        carpet_rooms=0,
        bathrooms=0,
        dust_rooms=0,
        thorough=False,
        is_senior=False,
    )
    assert q.total() >= 0


def test_house_thorough_increases_total():
    light = HouseCleaningQuote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=False,
        is_senior=False,
    )
    thorough = HouseCleaningQuote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=True,
        is_senior=False,
    )
    assert thorough.total() > light.total()


def test_house_senior_discount_reduces_total():
    non_senior = HouseCleaningQuote(
        house_sqft=1500,
        carpet_rooms=2,
        bathrooms=1,
        dust_rooms=2,
        thorough=True,
        is_senior=False,
    )
    senior = HouseCleaningQuote(
        house_sqft=1500,
        carpet_rooms=2,
        bathrooms=1,
        dust_rooms=2,
        thorough=True,
        is_senior=True,
    )
    assert senior.total() < non_senior.total()


def test_house_total_increases_with_sqft_over_threshold():
    # Monotonic check around surcharge threshold.
    base = HouseCleaningQuote(
        house_sqft=3000,
        carpet_rooms=0,
        bathrooms=0,
        dust_rooms=0,
        thorough=False,
        is_senior=False,
    )
    over = HouseCleaningQuote(
        house_sqft=3001,
        carpet_rooms=0,
        bathrooms=0,
        dust_rooms=0,
        thorough=False,
        is_senior=False,
    )
    assert over.total() >= base.total()
