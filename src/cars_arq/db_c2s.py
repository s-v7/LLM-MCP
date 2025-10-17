
from __future__ import annotations
from contextlib import contextmanager
from sqlalchemy import create_engine, select
from sqlalchemy.orm import sessionmaker
from .configs import Settings_Cars
from .models_c2s import Base, Car

_engine_c2s = create_engine(Settings_Cars.db_uri_c2s, echo=False, future=True)
_session_c2s = sessionmaker(bind=_engine_c2s, autoflush=False, expire_on_commit=False, autocommit=False, future=True)

def create_schema() -> None:
    Base.metadata.create_all(_engine_c2s)

@contextmanager
def session_scope():
    session = _session_c2s()
    try:
        yield session
        session.commit()
    except Exception:
        session.rollback()
        raise
    finally:
        session.close()


def query_cars(filters: dict) -> list[Car]:
    """Consulta com filtros dinâmicos seguros.
    Filtros aceitos: make, model, year_min, year_max, fuel_type, transmission
    price_min, price_max, mileage_max, body_type, color, city, state
    """
    stmt = select(Car)
    if make := filters.get("make"):
        stmt = stmt.where(Car.make.ilike(f"%{make}%"))
    if model := filters.get("model"):
        stmt = stmt.where(Car.model.ilike(f"%{model}%"))
    if filters.get("year_min") is not None:
        stmt = stmt.where(Car.year >= int(filters["year_min"]))
    if filters.get("year_max") is not None:
        stmt = stmt.where(Car.year <= int(filters["year_max"]))
    if fuel := filters.get("fuel_type"):
        stmt = stmt.where(Car.fuel_type.ilike(f"%{fuel}%"))
    if trans := filters.get("transmission"):
        stmt = stmt.where(Car.transmission.ilike(f"%{trans}%"))
    if bt := filters.get("body_type"):
        stmt = stmt.where(Car.body_type.ilike(f"%{bt}%"))
    if color := filters.get("color"):
        stmt = stmt.where(Car.color.ilike(f"%{color}%"))
    if city := filters.get("city"):
        stmt = stmt.where(Car.city.ilike(f"%{city}%"))
    if state := filters.get("state"):
        stmt = stmt.where(Car.state.ilike(f"%{state}%"))
    if filters.get("price_min") is not None:
        stmt = stmt.where(Car.price >= float(filters["price_min"]))
    if filters.get("price_max") is not None:
        stmt = stmt.where(Car.price <= float(filters["price_max"]))
    if filters.get("mileage_max") is not None:
        stmt = stmt.where(Car.mileage_km <= int(filters["mileage_max"]))
    
    with session_scope() as s:
        return list(s.scalars(stmt.limit(100)))
