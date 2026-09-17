import pytest

from home_services_quote_calculator.quotes import HouseCleaningQuote


def make_house_quote(
    house_sqft=1000,
    carpet_rooms=0,
    bathrooms=0,
    dust_rooms=0,
    thorough=False,
    is_senior=False,
):
    return HouseCleaningQuote(
        house_sqft=house_sqft,
        carpet_rooms=carpet_rooms,
        bathrooms=bathrooms,
        dust_rooms=dust_rooms,
        thorough=thorough,
        is_senior=is_senior,
    )


@pytest.mark.parametrize(
    ("house_sqft", "expected_tier"),
    [
        (1, "small"),
        (1200, "small"),
        (1201, "medium"),
        (2000, "medium"),
        (2001, "large"),
        (3000, "large"),
        (3001, "large"),
    ],
)
def test_house_tier_boundaries(house_sqft, expected_tier):
    quote = make_house_quote(house_sqft=house_sqft)

    assert quote.tier() == expected_tier


@pytest.mark.parametrize(
    (
        "house_sqft",
        "carpet_rooms",
        "bathrooms",
        "dust_rooms",
        "expected_subtotal",
    ),
    [
        (1000, 1, 1, 1, 240.00),
        (1500, 1, 1, 1, 380.00),
        (2500, 1, 1, 1, 520.00),
    ],
)
def test_house_subtotal_uses_tier_rates(
    house_sqft,
    carpet_rooms,
    bathrooms,
    dust_rooms,
    expected_subtotal,
):
    quote = make_house_quote(
        house_sqft=house_sqft,
        carpet_rooms=carpet_rooms,
        bathrooms=bathrooms,
        dust_rooms=dust_rooms,
    )

    assert quote.subtotal() == pytest.approx(expected_subtotal)


def test_house_large_house_surcharge_starts_above_3000_sqft():
    at_threshold = make_house_quote(house_sqft=3000)
    above_threshold = make_house_quote(house_sqft=3001)

    assert at_threshold.subtotal() == pytest.approx(0.00)
    assert above_threshold.subtotal() == pytest.approx(2.50)


def test_house_large_house_surcharge_calculation():
    quote = make_house_quote(house_sqft=3542)

    assert quote.subtotal() == pytest.approx(1355.00)


def test_house_thorough_service_fee_is_ten_percent_of_subtotal():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=True,
    )

    assert quote.subtotal() == pytest.approx(240.00)
    assert quote.service_fee() == pytest.approx(24.00)


def test_house_light_cleaning_has_no_service_fee():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=False,
    )

    assert quote.service_fee() == pytest.approx(0.00)


def test_house_senior_discount_is_fifteen_percent_after_service_fee():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=True,
        is_senior=True,
    )

    expected_discount = (240.00 + 24.00) * 0.15

    assert quote.discount() == pytest.approx(expected_discount)


def test_house_non_senior_has_no_discount():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        is_senior=False,
    )

    assert quote.discount() == pytest.approx(0.00)


def test_house_tax_is_eight_percent_after_discount():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=True,
        is_senior=True,
    )

    taxable = (240.00 + 24.00) - ((240.00 + 24.00) * 0.15)

    assert quote.tax() == pytest.approx(taxable * 0.08)


def test_house_total_exact_calculation():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=True,
        is_senior=True,
    )

    taxable = 224.40
    tax = 17.952
    expected_total = taxable + tax

    assert quote.total() == pytest.approx(expected_total)


def test_house_senior_discount_reduces_total():
    non_senior = make_house_quote(
        house_sqft=1500,
        carpet_rooms=2,
        bathrooms=1,
        dust_rooms=2,
        thorough=True,
        is_senior=False,
    )
    senior = make_house_quote(
        house_sqft=1500,
        carpet_rooms=2,
        bathrooms=1,
        dust_rooms=2,
        thorough=True,
        is_senior=True,
    )

    assert senior.total() < non_senior.total()


def test_house_items_include_calculation_details():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=2,
        bathrooms=1,
        dust_rooms=3,
    )

    items = quote.items()

    assert ("Carpet Cleaning", "2 rooms × $100.00", 200.00) in items
    assert ("Bathroom Cleaning", "1 bathroom × $80.00", 80.00) in items
    assert ("Dusting", "3 rooms × $60.00", 180.00) in items


def test_house_items_include_thorough_fee():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        thorough=True,
    )

    labels = [label for label, _, _ in quote.items()]

    assert "Thorough Cleaning Fee" in labels


def test_house_items_include_senior_discount_as_negative_amount():
    quote = make_house_quote(
        house_sqft=1000,
        carpet_rooms=1,
        bathrooms=1,
        dust_rooms=1,
        is_senior=True,
    )

    senior_item = next(
        item for item in quote.items() if item[0] == "Senior Discount"
    )

    assert senior_item[2] < 0


@pytest.mark.parametrize(
    "house_sqft",
    [0, -1],
)
def test_house_rejects_non_positive_square_footage(house_sqft):
    with pytest.raises(
        ValueError,
        match="House square footage must be greater than 0",
    ):
        make_house_quote(house_sqft=house_sqft)


@pytest.mark.parametrize(
    ("field", "kwargs", "message"),
    [
        (
            "carpet rooms",
            {"carpet_rooms": -1},
            "Carpet rooms cannot be negative",
        ),
        (
            "bathrooms",
            {"bathrooms": -1},
            "Bathrooms cannot be negative",
        ),
        (
            "dust rooms",
            {"dust_rooms": -1},
            "Dust rooms cannot be negative",
        ),
    ],
)
def test_house_rejects_negative_service_counts(field, kwargs, message):
    with pytest.raises(ValueError, match=message):
        make_house_quote(**kwargs)
