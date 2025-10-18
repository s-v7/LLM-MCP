
from __future__ import annotations
import random
import sys
from typing import Optional

from faker import Faker
from sqlalchemy import select
from .db_c2s import create_schema, session_scope
from .models_c2s import Car

faker = Faker("pt_BR")


### para modelos reais interação com APIS_EXTERNAS || dados próprios ....
MAKES_MODELS_BRL =  {
    "Toyota": ["Corolla", "Etios", "Yaris", "Hilux", "RAV4", "Corrolla Cross"],
    "Honda": ["Accord", "Civic", "Fit", "HR-V", "City"],
    "Volkswagen": ["Amarok", "Tera", "Gol", "Golf", "Polo", "T-Cross", "Nivus", "Virtus"],
    "Chevrolet": ["Onix", "Prisma", "Tracker", "S10"],
    "Fiat": ["Argo", "Pulse", "Toro", "Cronos"],
    "Ford": ["Ka", "Fusion", "Ranger", "Raptor", "EcoSport", "Mustang"],
    "Hyundai": ["HB20", "Creta", "Tucson"],        
}
FUEL_TYPES = ["gasolina", "etanol", "flex", "diesel", "elétrico", "híbrido"]
TRANSMISSIONS = ["manual", "automático", "CVT", "DCT"]
BODY_TYPES = ["hatch", "sedan", "SUV", "pickup", "coupe"]
DRIVETRAINS = ["FWD", "RWD", "AWD"]
COLORS = ["preto", "branco", "prata", "cinza", "vermelho", "azul"]

_VIN_CHARS = "ABCDEFGHJKLMNPRSTUVWXYZ0123456789"

def _random_vin(length: int = 17) -> str:
    return "".join(random.choice(_VIN_CHARS) for _ in range(length))

def seed(n: int = 150) -> None:
    # garante que as tabelas existam
    create_schema()

    with session_scope() as s:
        # evita semear duas vezes
        if s.execute(select(Car).limit(1)).first():
            print("Banco já possui dados; pulando seed.")
            return

        for _ in range(n):
            make = random.choice(list(MAKES_MODELS_BRL.keys()))
            model = random.choice(MAKES_MODELS_BRL[make])
            year = random.randint(2005, 2025)
            engine_cc = random.choice([1000, 1300, 1500, 1600, 1800, 2000, 2500])
            fuel = random.choice(FUEL_TYPES)
            color = random.choice(COLORS)
            mileage = random.randint(0, 220_000)
            doors = random.choice([2, 3, 4, 5])
            trans = random.choice(TRANSMISSIONS)
            body = random.choice(BODY_TYPES)
            drive = random.choice(DRIVETRAINS)
            price = round(random.uniform(25_000, 350_000), 2)
            city = faker.city()
            try:
                state = faker.estado_sigla()
            except AttributeError:
                state = "".join(random.choice("ABCDEFGHIJKLMNOPQRSTUVWXYZ") for _ in range(2))
            vin = _random_vin()

            s.add(
                Car(
                    make=make,
                    model=model,
                    year=year,
                    engine_cc=engine_cc,
                    fuel_type=fuel,
                    color=color,
                    mileage_km=mileage,
                    doors=doors,
                    transmission=trans,
                    body_type=body,
                    drivetrain=drive,
                    price=price,
                    city=city,
                    state=state,
                    vin=vin,
                )
            )

        print(f"Seed ok: {n} veículos inseridos.")

if __name__ == "__main__":
    qty: int = int(sys.argv[1]) if len(sys.argv) > 1 else 150
    seed(qty)
