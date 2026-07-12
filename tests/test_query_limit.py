from cars_arq.db_c2s import query_cars


def test_query_cars_caps_limit_at_ten():
    results = query_cars({}, limit=999)

    assert len(results) <= 10


def test_query_cars_uses_minimum_limit_one():
    results = query_cars({}, limit=0)

    assert len(results) <= 1
