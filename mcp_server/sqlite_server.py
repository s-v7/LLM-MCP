from mcp.server.fastmcp import FastMCP
from cars_arq.db_c2s import query_cars
from cars_arq.db_c2s import get_car_by_id, query_cars

mcp = FastMCP("LLM-MCP SQLite Server")


@mcp.tool()
def healthcheck() -> dict[str, str]:
    """Return the current status of the MCP server."""
    return {"status": "ok", "server": "sqlite"}


@mcp.tool()
def search_cars(
    make: str | None = None,
    model: str | None = None,
    year_min: int | None = None,
    year_max: int | None = None,
    fuel_type: str | None = None,
    body_type: str | None = None,
    state: str | None = None,
    price_max: float | None = None,
    limit: int = 10,
) -> list[dict]:
    """Search cars using structured filters."""

    filters = {
        "make": make,
        "model": model,
        "year_min": year_min,
        "year_max": year_max,
        "fuel_type": fuel_type,
        "body_type": body_type,
        "state": state,
        "price_max": price_max,
    }

    cars = query_cars(filters, limit=limit)

    return [
        {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "fuel_type": car.fuel_type,
            "body_type": car.body_type,
            "transmission": car.transmission,
            "price": car.price,
            "city": car.city,
            "state": car.state,
        }
        for car in cars
    ]

@mcp.tool()
def get_car(car_id: int) -> dict | None:
    """Return one car by its identifier."""

    car = get_car_by_id(car_id)

    if car is None:
        return None

    return {
        "id": car.id,
        "make": car.make,
        "model": car.model,
        "year": car.year,
        "engine_cc": car.engine_cc,
        "fuel_type": car.fuel_type,
        "color": car.color,
        "mileage_km": car.mileage_km,
        "doors": car.doors,
        "transmission": car.transmission,
        "body_type": car.body_type,
        "drivetrain": car.drivetrain,
        "price": car.price,
        "city": car.city,
        "state": car.state,
    }

@mcp.resource("cars://{car_id}")
def car_resource(car_id: str) -> dict | None:
    """Expose a car as an MCP Resource."""

    car = get_car_by_id(int(car_id))

    if car is None:
        return None

    return {
        "id": car.id,
        "make": car.make,
        "model": car.model,
        "year": car.year,
        "engine_cc": car.engine_cc,
        "fuel_type": car.fuel_type,
        "color": car.color,
        "mileage_km": car.mileage_km,
        "doors": car.doors,
        "transmission": car.transmission,
        "body_type": car.body_type,
        "drivetrain": car.drivetrain,
        "price": car.price,
        "city": car.city,
        "state": car.state,
    }

@mcp.resource("cars://state/{state}")
def cars_by_state_resource(state: str) -> list[dict]:
    """Expose cars filtered by Brazilian state."""

    cars = query_cars({"state": state}, limit=10)

    return [
        {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "fuel_type": car.fuel_type,
            "body_type": car.body_type,
            "transmission": car.transmission,
            "price": car.price,
            "city": car.city,
            "state": car.state,
        }
        for car in cars
    ]

@mcp.resource("cars://make/{make}")
def cars_by_make_resource(make: str) -> list[dict]:
    """Expose cars filtered by manufacturer."""
    cars = query_cars({"make": make}, limit=10)
    return [
        {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "fuel_type": car.fuel_type,
            "body_type": car.body_type,
            "transmission": car.transmission,
            "price": car.price,
            "city": car.city,
            "state": car.state
        }
        for car in cars

    ]


@mcp.resource("cars://model/{model}")
def cars_by_model_resource(model: str) -> list[dict]:
    """Expose cars filtered by model."""
    cars = query_cars({"model": model}, limit=10)
    return [
        {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "fuel_type": car.fuel_type,
            "body_type": car.body_type,
            "transmission": car.transmission,
            "price": car.price,
            "city": car.city,
            "state": car.state
        }
        for car in cars
    ]


@mcp.resource("cars://fuel/{fuel_type}")
def cars_by_fuel_resource(fuel_type: str) -> list[dict]:
    """Expose cars filtered by fuel type."""
    cars = query_cars({"fuel_type": fuel_type}, limit=10)
    return [
        {
            "id": car.id,
            "make": car.make,
            "model": car.model,
            "year": car.year,
            "fuel_type": car.fuel_type,
            "body_type": car.body_type,
            "transmission": car.transmission,
            "price": car.price,
            "city": car.city,
            "state": car.state
        }
        for car in cars
    ]
    
if __name__ == "__main__":
    mcp.run()
