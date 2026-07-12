from mcp_server.sqlite_server import search_cars


def test_search_cars_combines_filters():
    results = search_cars(
        make="Ford",
        year_min=2000,
        year_max=2026,
        limit=10,
    )

    assert all("ford" in car["make"].lower() for car in results)
    assert all(2000 <= car["year"] <= 2026 for car in results)


def test_search_cars_filters_by_price():
    results = search_cars(price_max=100000, limit=10)

    assert all(car["price"] <= 100000 for car in results)
