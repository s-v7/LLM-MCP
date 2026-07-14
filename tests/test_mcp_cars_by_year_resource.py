from mcp_server.sqlite_server import cars_by_year_resource


def test_cars_by_year_resource_filters_year():
    cars = cars_by_year_resource("2024")

    assert len(cars) <= 10
    assert all(car["year"] == 2024 for car in cars)


def test_cars_by_year_resource_returns_empty_list_for_unknown_year():
    assert cars_by_year_resource("1900") == []
