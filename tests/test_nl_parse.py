import pytest
from cars_arq.client_c2s import parse_user_query, _norm

@pytest.mark.parametrize("q,expect", [
    ("preço até 50.000", {"price_max": 50000}),
    ("preco ate 70 mil", {"price_max": 70000}),
    ("R$ 45.060,56", {"price_max": 45060}),
])
def test_parse_price_max(q, expect):
    f = parse_user_query(q)
    assert f.get("price_max") == expect["price_max"]
    assert f.get("limit") == 20

@pytest.mark.parametrize("q,expect_min,expect_max", [
    ("entre 2016 e 2019", 2016, 2019),
    ("de 2018 pra cima", 2018, None),
    ("a partir de 2020", 2020, None),
    ("até 2015", None, 2015),
])
def test_parse_years(q, expect_min, expect_max):
    f = parse_user_query(q)
    if expect_min is not None:
        assert f.get("year_min") == expect_min
    if expect_max is not None:
        assert f.get("year_max") == expect_max

@pytest.mark.parametrize("q,expect", [
    ("quero um hatch", "hatch"),
    ("SUV a diesel", "SUV"),
    ("picape elétrica", "pickup"),
    ("coupe gasolina", "coupe"),
])
def test_parse_body_and_fuel(q, expect):
    f = parse_user_query(q)
    if expect.lower() in {"hatch", "sedan", "pickup", "coupe"}:
        assert f.get("body_type") == (expect.upper() if expect == "SUV" else expect)
    if "diesel" in _norm(q):
        assert f.get("fuel_type") == "diesel"
    if "eletrica" in _norm(q):
        assert f.get("fuel_type") in {"elétrico", "eletrico"}
    if "gasolina" in _norm(q):
        assert f.get("fuel_type") == "gasolina"

@pytest.mark.parametrize("q,expect_state", [
    ("em SP", "SP"),
    ("busca no RJ", "RJ"),
])
def test_parse_state(q, expect_state):
    f = parse_user_query(q)
    assert f.get("state") == expect_state

@pytest.mark.parametrize("q,expect_make,expect_model", [
    ("toyota até 120000", "Toyota", None),
    ("quero HVR", None, "HR-V"),       # fuzzy hr-v
    ("tcross até 50 mil 2022", None, "T-Cross"),  # alias tcross
])
def test_parse_make_and_model(q, expect_make, expect_model):
    f = parse_user_query(q)
    if expect_make:
        assert f.get("make") == expect_make
    if expect_model:
        assert f.get("model") == expect_model

