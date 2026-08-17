from mcp_server.sqlite_server import cars_by_make_resource


def test_cars_by_make_resource_filters_make():
    cars = cars_by_make_resource("Ford")

    assert len(cars) <= 10
    assert all("ford" in car["make"].lower() for car in cars)


def test_cars_by_make_resource_returns_empty_list_for_unknown_make():
    assert cars_by_make_resource("MarcaInexistenteXYZ") == []
