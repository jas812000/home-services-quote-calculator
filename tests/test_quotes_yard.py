import pytest

from home_services_quote_calculator.models import TimeHM
from home_services_quote_calculator.quotes import YardServiceQuote


def make_yard_quote(
    yard_sqft=1000,
    shrubs=0,
    start=None,
    end=None,
    is_senior=False,
):
    return YardServiceQuote(
        yard_sqft=yard_sqft,
        shrubs=shrubs,
        start=start or TimeHM(9, 0),
        end=end or TimeHM(10, 0),
        is_senior=is_senior,
    )


def test_yard_labor_hours_calculation():
    quote = make_yard_quote(
        start=TimeHM(9, 15),
        end=TimeHM(11, 45),
    )

    assert quote.labor_hours() == pytest.approx(2.5)


@pytest.mark.parametrize(
    ("yard_sqft", "expected_cost"),
    [
        (1, 60.00),
        (1000, 60.00),
        (1001, 75.00),
        (2000, 75.00),
        (5000, 120.00),
        (7456, 165.00),
    ],
)
def test_yard_mowing_cost_uses_base_charge_and_size_increments(
    yard_sqft,
    expected_cost,
):
    quote = make_yard_quote(yard_sqft=yard_sqft)

    mowing_item = next(
        item for item in quote.items() if item[0] == "Mowing"
    )

    assert mowing_item[2] == pytest.approx(expected_cost)


def test_yard_mowing_item_includes_calculation_details():
    quote = make_yard_quote(yard_sqft=7456)

    mowing_item = next(
        item for item in quote.items() if item[0] == "Mowing"
    )

    assert mowing_item == (
        "Mowing",
        "$45 base + 8 × $15 per 1,000 sq ft",
        165.00,
    )


def test_yard_edging_uses_estimated_square_perimeter():
    quote = make_yard_quote(yard_sqft=100)

    edging_item = next(
        item for item in quote.items() if item[0] == "Edging"
    )

    # sqrt(100) * 4 = 40 linear feet; 40 * $4 = $160.
    assert edging_item[2] == pytest.approx(160.00)


def test_yard_shrub_pruning_cost():
    quote = make_yard_quote(
        yard_sqft=100,
        shrubs=3,
    )

    shrub_item = next(
        item for item in quote.items() if item[0] == "Shrub Pruning"
    )

    assert shrub_item[2] == pytest.approx(75.00)


def test_yard_base_labor_cost():
    quote = make_yard_quote(
        yard_sqft=100,
        start=TimeHM(9, 0),
        end=TimeHM(11, 0),
    )

    labor_item = next(
        item for item in quote.items() if item[0] == "Labor"
    )

    assert labor_item[2] == pytest.approx(160.00)


@pytest.mark.parametrize(
    ("yard_sqft", "expected_hourly_surcharge"),
    [
        (5000, 0.00),
        (5001, 35.00),
        (7000, 35.00),
        (7001, 70.00),
        (9000, 70.00),
        (9001, 105.00),
    ],
)
def test_yard_hourly_surcharge_boundaries(
    yard_sqft,
    expected_hourly_surcharge,
):
    quote = make_yard_quote(yard_sqft=yard_sqft)

    assert quote.hourly_surcharge() == pytest.approx(
        expected_hourly_surcharge
    )


def test_yard_large_yard_surcharge_uses_labor_hours():
    quote = make_yard_quote(
        yard_sqft=7456,
        start=TimeHM(7, 0),
        end=TimeHM(16, 0),
    )

    surcharge_item = next(
        item
        for item in quote.items()
        if item[0] == "Large Yard Surcharge"
    )

    # 7,456 sq ft = $70/hour surcharge; 9 hours = $630.
    assert surcharge_item[2] == pytest.approx(630.00)


def test_yard_senior_discount_is_fifteen_percent_of_subtotal():
    quote = make_yard_quote(
        yard_sqft=100,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(10, 0),
        is_senior=True,
    )

    assert quote.discount() == pytest.approx(
        quote.subtotal() * 0.15
    )


def test_yard_non_senior_has_no_discount():
    quote = make_yard_quote(is_senior=False)

    assert quote.discount() == pytest.approx(0.00)


def test_yard_tax_is_eight_percent_after_discount():
    quote = make_yard_quote(
        yard_sqft=100,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(10, 0),
        is_senior=True,
    )

    taxable = quote.subtotal() - quote.discount()

    assert quote.tax() == pytest.approx(taxable * 0.08)


def test_yard_total_exact_calculation():
    quote = make_yard_quote(
        yard_sqft=100,
        shrubs=0,
        start=TimeHM(9, 0),
        end=TimeHM(10, 0),
        is_senior=False,
    )

    # Mowing: $45 base + 1 × $15 = $60
    # Edging: 40 estimated linear ft × $4 = $160
    # Labor: 1 hour × $80 = $80
    # Subtotal: $300
    # Tax: $24
    # Total: $324
    assert quote.subtotal() == pytest.approx(300.00)
    assert quote.tax() == pytest.approx(24.00)
    assert quote.total() == pytest.approx(324.00)


def test_yard_senior_discount_reduces_total():
    non_senior = make_yard_quote(
        yard_sqft=200,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(11, 0),
    )
    senior = make_yard_quote(
        yard_sqft=200,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(11, 0),
        is_senior=True,
    )

    assert senior.total() < non_senior.total()


def test_yard_items_include_calculation_details():
    quote = make_yard_quote(
        yard_sqft=100,
        shrubs=2,
        start=TimeHM(9, 0),
        end=TimeHM(10, 0),
    )

    items = quote.items()

    assert (
        "Mowing",
        "$45 base + 1 × $15 per 1,000 sq ft",
        60.00,
    ) in items
    assert (
        "Shrub Pruning",
        "2 shrubs × $25.00",
        50.00,
    ) in items
    assert (
        "Labor",
        "1.00 hr × $80.00/hr",
        80.00,
    ) in items


def test_yard_items_include_senior_discount_as_negative_amount():
    quote = make_yard_quote(
        yard_sqft=100,
        is_senior=True,
    )

    senior_item = next(
        item
        for item in quote.items()
        if item[0] == "Senior Discount"
    )

    assert senior_item[2] < 0


@pytest.mark.parametrize("yard_sqft", [0, -1])
def test_yard_rejects_non_positive_square_footage(yard_sqft):
    with pytest.raises(
        ValueError,
        match="Yard square footage must be greater than 0",
    ):
        make_yard_quote(yard_sqft=yard_sqft)


def test_yard_rejects_negative_shrub_count():
    with pytest.raises(
        ValueError,
        match="Shrub count cannot be negative",
    ):
        make_yard_quote(shrubs=-1)


def test_yard_rejects_end_time_before_start_time():
    with pytest.raises(
        ValueError,
        match="End time must be after start time",
    ):
        make_yard_quote(
            start=TimeHM(10, 0),
            end=TimeHM(9, 0),
        )


def test_yard_rejects_end_time_equal_to_start_time():
    with pytest.raises(
        ValueError,
        match="End time must be after start time",
    ):
        make_yard_quote(
            start=TimeHM(10, 0),
            end=TimeHM(10, 0),
        )
