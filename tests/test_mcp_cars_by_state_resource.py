from mcp_server.sqlite_server import cars_by_state_resource


def test_cars_by_state_resource_filters_state():
    cars = cars_by_state_resource("RN")

    assert len(cars) <= 10
    assert all(car["state"] == "RN" for car in cars)


def test_cars_by_state_resource_returns_empty_list_for_unknown_state():
    assert cars_by_state_resource("ZZ") == []
