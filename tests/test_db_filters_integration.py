import pytest
from cars_arq.db_c2s import query_cars

def _all(items, pred):
    return all(pred(x) for x in items)

@pytest.mark.parametrize("price_max", [30000, 70000, 120000])
def test_db_price_max(price_max):
    items = query_cars({"price_max": price_max})
    assert isinstance(items, list)
    if items:
        assert _all(items, lambda r: r.price <= float(price_max))

@pytest.mark.parametrize("year_min,year_max", [
    (2016, 2019),
    (2018, None),
    (None, 2015),
])
def test_db_year_bounds(year_min, year_max):
    f = {}
    if year_min is not None:
        f["year_min"] = year_min
    if year_max is not None:
        f["year_max"] = year_max
    items = query_cars(f)
    if items:
        if year_min is not None:
            assert _all(items, lambda r: r.year >= year_min)
        if year_max is not None:
            assert _all(items, lambda r: r.year <= year_max)

@pytest.mark.parametrize("body", ["hatch","sedan","SUV","pickup","coupe"])
def test_db_body_type(body):
    norm = body.upper() if body == "SUV" else ("pickup" if body=="pickup" else body)
    items = query_cars({"body_type": norm})
    if items:
        assert _all(items, lambda r: (r.body_type or "").lower() == norm.lower())

@pytest.mark.parametrize("fuel", ["gasolina", "etanol", "flex", "diesel"])
def test_db_fuel_type(fuel):
    items = query_cars({"fuel_type": fuel})
    if items:
        assert _all(items, lambda r: (r.fuel_type or "").lower() == fuel)

@pytest.mark.parametrize("state", ["SP","RJ","MG","BA"])
def test_db_state(state):
    items = query_cars({"state": state})
    if items:
        assert _all(items, lambda r: (r.state or "") == state)

@pytest.mark.parametrize("make", ["Toyota","Honda","Volkswagen","Chevrolet","Fiat","Ford","Hyundai"])
def test_db_make(make):
    items = query_cars({"make": make})
    if items:
        assert _all(items, lambda r: (r.make or "") == make)

@pytest.mark.parametrize("mileage_max", [50000, 100000, 150000])
def test_db_mileage_max(mileage_max):
    items = query_cars({"mileage_max": mileage_max})
    if items:
        assert _all(items, lambda r: (r.mileage_km or 0) <= mileage_max)

