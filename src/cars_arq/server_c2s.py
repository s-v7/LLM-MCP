
from __future__ import annotations
import json
import socket
import threading
from typing import Iterable
from .configs import Settings_Cars
from .protocol_mcp_c2s import  MCPEnvelope, ResultPayload, ErrorPayload, CarDTO
from .db_c2s import query_cars


# Servidor TCP simples com JSON Lines

class MCPServer:
    def __init__(self, host: str, port: int) -> None:
        self.host = host
        self.port = port

    def start(self) -> None:
        with socket.create_server((self.host, self.port), reuse_port=True) as srv:
            print(f"[server] ouvindo em {self.host}:{self.port}")
            while True:
                conn, addr = srv.accept()
                print(f"[server] conexão de {addr}")
                threading.Thread(target=self._handle, args=(conn,), daemon=True).start()

    def _handle(self, conn: socket.socket) -> None:
        with conn, conn.makefile("r") as reader:
            for line in reader:
                line = line.strip()
                if not line:
                    continue
                try:
                    env = MCPEnvelope.model_validate_json(line)
                    if env.kind != "query":
                        self._send_error(conn, env.id, "Mensagem não é 'query'.")
                        continue
                    filters = env.payload.get("filters", {})
                    cars = query_cars(filters)
                    items = [
                        CarDTO(
                            id=c.id,
                            make=c.make,
                            model=c.model,
                            year=c.year,
                            color=c.color,
                            mileage_km=c.mileage_km,
                            price=c.price,
                        ).model_dump()
                        for c in cars
                    ]
                    payload = ResultPayload(items=items, total=len(items)).model_dump() # pyright: ignore[reportArgumentType]
                    resp = MCPEnvelope(kind="result", id=env.id, payload=payload)
                    _send_jsonl(conn, resp.model_dump())
                except Exception as e:  # manter o server vivo e responder error
                    err = MCPEnvelope(
                        kind="error",
                        id=(env.id if 'env' in locals() else "-"),
                        payload=ErrorPayload(message=str(e)).model_dump(),
                    )
                    _send_jsonl(conn, err.model_dump())

    def _send_error(self, conn: socket.socket, id: str, message: str) -> None:
        err = MCPEnvelope(
            kind="error",
            id=id,
            payload=ErrorPayload(message=message).model_dump(),
        )
        _send_jsonl(conn, err.model_dump())

def _send_jsonl(conn: socket.socket, data: dict) -> None:
    blob = json.dumps(data, ensure_ascii=False)
    conn.sendall((blob + "\n").encode("utf-8"))

if __name__ == "__main__":
    MCPServer(Settings_Cars.server_host_c2s, Settings_Cars.server_port_c2s).start()

