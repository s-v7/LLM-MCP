from mcp_server.sqlite_server import get_car


def test_get_car_returns_existing_car():
    car = get_car(1)

    assert car is not None
    assert car["id"] == 1
    assert "make" in car
    assert "model" in car
    assert "price" in car


def test_get_car_returns_none_for_unknown_id():
    assert get_car(999999) is None
