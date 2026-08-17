from mcp_server.sqlite_server import healthcheck


def test_healthcheck_returns_server_status():
    assert healthcheck() == {
        "status": "ok",
        "server": "sqlite",
    }
