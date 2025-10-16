
from __future__ import annotations
from dataclasses import dataclass 

@dataclass(frozen=True)
class Settings_Cars:
    db_uri_c2s: str = "sqlite:///./cars.db"
    server_c2s: str = "127.0.0.1"
    server_port: int = 8765

SETTINGS_C2S = SETTINGS_CARS()

