from mcp.server.fastmcp import FastMCP
from cars_arq.db_c2s import query_cars

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


if __name__ == "__main__":
    mcp.run()
