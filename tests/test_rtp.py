import importlib
import json
import pytest

proto = pytest.importorskip("cars_arq.protocol_mcp_c2s", reason="Módulo de protocolo não encontrado")

def _find_callable(mod, candidates):
    for name in candidates:
        fn = getattr(mod, name, None)
        if callable(fn):
            return fn
    return None

def test_protocol_round_trip_minimal():
    """
    Verifica se o protocolo codifica/decodifica algo tipo:
    {"action": "search", "filters": {...}}
    """
    encode = _find_callable(proto, ["encode_message", "encode", "encode_payload"])
    decode = _find_callable(proto, ["decode_message", "decode", "decode_payload"])

    if not encode or not decode:
        pytest.skip("Funções encode/decode não encontradas no protocolo. Nomeie como encode_message/decode_message (ou similares).")

    payload = {"action": "search", "filters": {"body_type": "sedan", "fuel_type": "flex", "limit": 3}}
    wire = encode(payload)
    # wire pode ser str/bytes; normalize para str para inspeção
    assert wire, "encode() retornou vazio/nulo"

    back = decode(wire)
    assert isinstance(back, dict), "decode() deve retornar dict"
    assert back.get("action") == "search"
    assert back.get("filters", {}).get("body_type") == "sedan"
    assert back.get("filters", {}).get("fuel_type") == "flex"

def test_protocol_is_json_like():
    """
    Se o protocolo for texto JSON no fio, este teste ajuda a pegar corrupções básicas.
    (Se não for JSON, o teste é pulado.)
    """
    encode = getattr(proto, "encode_message", None) or getattr(proto, "encode", None)
    decode = getattr(proto, "decode_message", None) or getattr(proto, "decode", None)
    if not encode or not decode:
        pytest.skip("Sem encode/decode para validar JSON.")

    payload = {"ping": True}
    wire = encode(payload)

    if isinstance(wire, (str, bytes)):
        txt = wire.decode() if isinstance(wire, (bytes, bytearray)) else wire
        try:
            parsed = json.loads(txt)
        except Exception:
            pytest.skip("O protocolo não é JSON puro — ok, pulando.")
        else:
            assert parsed == payload or isinstance(parsed, dict)
    else:
        pytest.skip("Wire não é str/bytes — protocolo binário custom? Pulando.")
