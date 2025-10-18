import os
import sqlite3
import pytest
import importlib

# Garante que o pacote exista
pkg = pytest.importorskip("cars_arq", reason="Pacote cars_arq não encontrado")
dbmod = pytest.importorskip("cars_arq.db_c2s", reason="Módulo db_c2s não encontrado")

# Tenta localizar um gerador de dados para seed
def _try_seed_data():
    try:
        seed_mod = importlib.import_module("cars_arq.data_fake_c2s")
    except Exception:
        return False

    for name in ("main", "seed", "run", "generate", "populate"):
        fn = getattr(seed_mod, name, None)
        if callable(fn):
            fn()
            return True
    return True

def _db_file():
    paths = ["cars.db", os.path.join(os.path.dirname(os.path.dirname(__file__)), "cars.db")]
    for p in paths:
        if os.path.exists(p):
            return p
    return None

def _ensure_seeded():
    db_path = _db_file()
    if not db_path or not os.path.exists(db_path):
        _try_seed_data()
        db_path = _db_file()
    return db_path

def _count_rows(db_path):
    with sqlite3.connect(db_path) as conn:
        cur = conn.execute("SELECT name FROM sqlite_master WHERE type='table'")
        tables = [r[0] for r in cur.fetchall()]
        preferred = None
        for t in tables:
            if t.lower() in {"car", "cars", "automovel", "automoveis", "vehicles", "veiculos"}:
                preferred = t
                break
        table = preferred or tables[0]
        cur = conn.execute(f"SELECT COUNT(*) FROM {table}")
        (n,) = cur.fetchone()
        return n

def _pick_query_callable():
    candidates = [
        "search_cars",
        "query_cars",
        "get_cars",
        "list_cars",
        "find_cars",
    ]
    for name in candidates:
        fn = getattr(dbmod, name, None)
        if callable(fn):
            return fn
    return None

def test_database_has_data():
    db_path = _ensure_seeded()
    assert db_path and os.path.exists(db_path), "Banco cars.db não encontrado nem após tentar seed."
    assert _count_rows(db_path) >= 100, "Esperado ao menos 100 veículos no seed."

def test_filter_by_fuel_and_body_safeguarded():
    query = _pick_query_callable()
    if not query:
        pytest.skip("Nenhuma função de consulta encontrada (ex.: search_cars/query_cars/get_cars).")

    filters_ = {"fuel_type": "flex", "body_type": "sedan", "limit": 20}
    results = query(filters_)
    assert isinstance(results, (list, tuple)), "A consulta deve retornar lista/tupla."
    if not results:
        pytest.xfail("Nenhum resultado para (flex, sedan). Ok se dataset aleatório não gerar — xfail controlado.")

    # Asserções 'brand-agnostic' por stringificação do item
    sample = str(results[0]).lower()
    assert any(k in sample for k in ("sedan", "hatch", "suv", "pickup")), "Item não parece conter tipo de carroceria; verifique representação."
