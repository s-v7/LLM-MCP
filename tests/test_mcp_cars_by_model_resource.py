
from mcp_server.sqlite_server import cars_by_model_resource

def test_cars_by_resource_filters_model():
    cars = cars_by_model_resource("Fusion")

    assert len(cars) <= 10
    assert all("fusion" in car["model"].lower() for car in cars)

def test_cars_by_model_resource_returns_empty_list_for_unknown_model():
    assert cars_by_model_resource("modeloInexistenteXYZ") == []

