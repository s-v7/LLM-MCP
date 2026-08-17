from mcp_server.sqlite_server import cars_by_max_price_resource


def test_cars_by_max_price_resource_filters_price():
    cars = cars_by_max_price_resource("100000")

    assert len(cars) <= 10
    assert all(car["price"] <= 100000 for car in cars)


def test_cars_by_max_price_resource_invalid_value_returns_empty():
    assert cars_by_max_price_resource("abc") == []
