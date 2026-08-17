from mcp_server.sqlite_server import car_resource


def test_car_resource_returns_existing_car():
    car = car_resource("1")

    assert car is not None
    assert car["id"] == 1
    assert car["make"] == "Ford"
    assert "model" in car
    assert "price" in car


def test_car_resource_returns_none_for_unknown_car():
    assert car_resource("999999") is None
