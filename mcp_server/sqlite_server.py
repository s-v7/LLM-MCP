from mcp.server.fastmcp import FastMCP

mcp = FastMCP("LLM-MCP SQLite Server")


@mcp.tool()
def healthcheck() -> dict[str, str]:
    """Return the current status of the MCP server."""
    return {"status": "ok", "server": "sqlite"}


if __name__ == "__main__":
    mcp.run()
