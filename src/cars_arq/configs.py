
from __future__ import annotations
from dataclasses import dataclass 
from pathlib import Path

@dataclass(frozen=True)
class Settings_Cars:
    _project_root: Path = Path(__file__).resolve().parents[2]
    _db_path: Path = _project_root / "cars.db"
    db_uri_c2s: str = f"sqlite:///{_db_path}"
    server_host_c2s: str = "127.0.0.1"
    server_port_c2s: int = 8765

SETTINGS_C2S = Settings_Cars()

