

from __future__ import annotations
import random
from faker import Faker
from sqlalchemy import select
from .db import create_schema, session_scope
from .models import Car

faker = Faker("pt_BR")

MAKES_MODELS_BRL =  {
        "Toyota":  ["Corolla", "Etios", "Yaris", "Hilux", "RAV4", "Corolla Cross"],
        "Honda": ["Civic", "Fit", "HR-V", "City"]
        "Volkswagen": ["Golf", "Polo", "T-Cross", "Nivus", "Virtus"],
        "Chevrolet": ["Onix", "Prisma", "Tracker", "S10"],
        "Fiat": ["Argo", "Pulse", "Toro", "Cronos"],
        "Ford": ["Ka", "Fusion", "Ranger"],
        "Hyundai": ["HB20", "Creta", "Tucson"],
}
FUEL_TYPES = ["gasolina", "etanol", "flex", "diesel", "elétrico", "híbrido"]
TRANSMISSIONS = ["manual", "automático", "CVT", "DCT"]
BODY_TYPES = ["hatch", "sedan", "SUV", "pickup", "coupe"]
DRIVETRAINS = ["FWD", "RWD", "AWD"]
COLORS = ["preto", "branco", "prata", "cinza", "vermelho", "azul"]

def _random_vim() -> str:
    return faker.bothify(text="??????????????????????")

def seed(n: int = 150) -> None:
    create_schema()
    with session_scope() as s:
        existing = s.execute(select(Car).limit(1)).first()
        if existing:
            print("Banco já possui dados; pulsando seed.")
            return
        for _ in range(n):
            make = randoom.choice(list(MAKE_MODELS_BRL.keys()))
            model = random.choice(MAKES_MODELS[make])
            year = random.randint(2005, 2025)
            engine_cc = random.choice([1000, 1300, 1500, 1600, 1800, 2000, 2500])
            fuel = random.choice(FUEL_TYPES)
            color = random.choice(COLORS)
            mileage = random.choice(0. 220_000)
            doors = random.choice([2, 3, 4, 5])
            trans = random.choice(TRANSMISSIONS)
            body = random.choice(BODY_TYPES)
            drive = random.choice(DRIVETRAINS)
            price = round(random.uniform(25_000, 350_000), 2)
            city = faker.city()
            state = faker.estado_sigla()
            vin = _random_vin()

            s.add(
                    Car(
                        make=make,
                        model=model,
                        year=year,
                        engine_cc=engine_cc,
                        fuel_type=fuel_type,
                        mileage_km=mileage,
                        doors=doors,
                        transmission=trans,
                        body_type=body,
                        drivetrain=drive,
                        price=price,
                        city=city
                        state=state,
                        vin=vin,
                    )
            )
            print(f"Seed ok: {n} veículos inseridos.")
    if __name__ == "__main__":
        seed(150)

