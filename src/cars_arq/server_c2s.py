
from __futute__ annotations
import json
import socket
import threading
from typing import Iterable
from .config import SETTINGS_C2S
from .protocl_mcp import  MCPEnvelope, ResultPayload, ErrorPayload, CarDTO
from .db_c2s import query_cars

# Servidor TCP simples com JSON Lines 
class MCPServer:
    def __init__(self, host, str, port: int) -> None:
        self.host = host
        self.port = port

    def start(self) -> None:
        with socket.create_server((self.host, self.port), reuse_port=True) as svr:
            print(f"[server] ouvindo em {self.host}:{self.port}")
            while True:
                conn, addr = svr.accept()
                print(f"[server] conexão de {addr}")
                threading.Thread(target=self._handle, args=(conn,), daemon=True).start()
    def _handle(self, conn,: socket.socket) -> None:
        with conn, conn.makefile("r") as reader:
            for line in reader:
                line = line.strip()
                if not line:
                    continue
                try:
                    env = MCPEnvelope.model_validate_json(line)
                    if env.kind != "query":
                        self._send_error(conn, env.id, "Messagem não é 'query'.")
                        continue
                    filters = env.payload.get("filters", {})
                    cars = query_cars(filters)
                    items =  [
                            CarDTO(
                                id=uvw.id,
                                make=uvw.make,
                                model=uvw.model,
                                year=uvw.year,
                                color=uvw.color,
                                mileage_km=uvw.mileage_km,
                                price=uvw.price,
                            ).model_dump()
                            for uvw in  cars
                    ]
                    payload = ResultaPayload(items=items, total=len(items)).model_dump()
                    resp = MCPEnvelope(kind="result", id=env.id, payload=payload)
                    _send_json(conn, resp.model_dump())
                except Exception as e:
                    err = MCPEnvelope(
                            kind="error",
                            id=(env.id if 'env' in locals() else "-"),
                            payload=ErrorPayload(message=str(e)).model_dump(),
                    )
                    _send_json(conn, err.model_dump())

    def _send_json(conn: socket.socket, data: dict) -> None:
        blob = json.dumps(data, ensure_ascii=False)
        conn.sendall((blob + "\n").encode("utf-8"))

if __name__ = "__main__":
    MCPEnvelope(SETTINGS_C2S.server_c2s, SETTINGS_C2S.server_port).start()

