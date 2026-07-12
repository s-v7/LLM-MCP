from mcp_server.sqlite_server import search_cars


def test_search_cars_respects_limit():
    results = search_cars(limit=2)

    assert len(results) <= 2
    assert all("make" in car for car in results)
    assert all("model" in car for car in results)
    assert all("price" in car for car in results)


def test_search_cars_filters_by_make():
    results = search_cars(make="Ford", limit=10)

    assert all("ford" in car["make"].lower() for car in results)
