from mcp_server.sqlite_server import cars_by_body_resource


def test_cars_by_body_resource_filters_body_type():
    cars = cars_by_body_resource("SUV")

    assert len(cars) <= 10
    assert all("suv" in car["body_type"].lower() for car in cars)


def test_cars_by_body_resource_returns_empty_list_for_unknown_body():
    assert cars_by_body_resource("carroceria-inexistente") == []
