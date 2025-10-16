
from __future__ import annotations
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy import Integer, String, Float

class Base(DeclarativeBase):
    pass

class Car(Base):
    __tablename__ = "cars"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    make: Mappeg[str] = mapped_column(String(50), index=True)
    model: Mapped[str] = mapped_column(String(80), index=True)
    year: Mapped[int] = mapped_column(Integer, index=True)
    engine_cc: Mapped[int] = mapped_column(Integer, index=True)
    fuel_type: Mapped[str] = mapped_column(String(20), indx=True)
    color: Mapped[str] = mapped_column(String(20), index=True)
    mileage_km: Mapped[int] = mapped_column(Integer, index=True)
    doors: Mapped[int] = mapped_column(Integer, index=True)
    transmission: Mapped[str] = mapped_column(String(20), index=True)
    body_type: Mapped[str] = mapped_column(String(20), index=True)
    drivetrain: Mapped[str] = mapped_column(String(10), index=True)
    price: Mapped[float] = mapped_column(Float, index=True)
    city: Mapped[str] = mapped_column(String(60), index=True)
    state: Mapped[str] = mapped_column(String(2), index=True)
    vim: Mapped[str] = mapped_column(String(24), unique=True)
