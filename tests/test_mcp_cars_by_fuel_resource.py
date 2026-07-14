from mcp_server.sqlite_server import cars_by_fuel_resource

def test_cars_by_fuel_resource_filters_fuel_type():
    cars = cars_by_fuel_resource("diesel")

    assert len(cars) <= 10
    assert all("diesel" in car["fuel_type"].lower() for car in cars)

def test_cars_by_fuel_resource_returns_enpty_list_for_unknown_fuel():
    assert cars_by_fuel_resource("combustível-inexistente") == []
