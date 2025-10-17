from __future__ import annotations
import json
import re
import socket
import uuid
import unicodedata
import difflib
from typing import Optional

from rich.console import Console
from rich.table import Table

from .configs import Settings_Cars

console = Console()

COMMON_FUELS = {"gasolina", "etanol", "flex", "diesel", "elétrico", "eletrico", "híbrido", "hibrido"}
COMMON_BODIES = {"hatch", "sedan", "suv", "pickup", "picape", "coupe", "cupe", "cupê"}
BR_STATES = {
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA","MT","MS","MG",
    "PA","PB","PR","PE","PI","RJ","RN","RS","RO","RR","SC","SP","SE","TO"
}
KNOWN_MAKES = ["Toyota","Honda","Volkswagen","Chevrolet","Fiat","Ford","Hyundai"]
KNOWN_MODELS = [
    # Toyota
    "Corolla","Etios","Yaris","Hilux","RAV4",
    # Honda
    "Civic","Fit","HR-V","City",
    # Volkswagen
    "Golf","Polo","T-Cross","Nivus","Virtus",
    # Chevrolet
    "Onix","Prisma","Tracker","S10",
    # Fiat
    "Argo","Pulse","Toro","Cronos",
    # Ford
    "Ka","Fusion","Ranger",
    # Hyundai
    "HB20","Creta","Tucson"
]

PRICE_RE = re.compile(r"(\d{2,3}[\.]?\d{3}|\d{4,6})(?:\s*(?:reais|r\$))?", re.I)

def _norm(txt: str) -> str:
    return unicodedata.normalize("NFKD", txt or "").encode("ascii","ignore").decode("ascii").lower()

def _parse_money_raw(token: str) -> Optional[int]:
    if not token:
        return None
    t = token.strip().lower()
    t = t.replace(" ", "")
    mil_flag = "mil" in t
    t = t.replace("mil", "")
    t = t.replace(".", "").replace(",", ".")
    m = re.search(r"\d+(?:\.\d+)?", t)
    if not m:
        return None
    val = float(m.group(0))
    if mil_flag and val < 1000:
        val *= 1000
    return int(round(val))

def _fuzzy_one(token: str, population: list[str], *, cutoff: float = 0.7) -> Optional[str]:
    if not token:
        return None
    matches = difflib.get_close_matches(token, population, n=1, cutoff=cutoff)
    return matches[0] if matches else None


def parse_user_query(text: str) -> dict:
    """
    Extrai filtros a partir de frases livres.
    Retorna sempre dict (possivelmente vazio).
    Reconhece: make, model (via fuzzy), body_type, fuel_type, state, year_min/max, price_max, limit.
    """
    result: dict = {}
    if not text:
        return result

    raw = text.strip()
    t = _norm(raw)

    # body_type
    for body in COMMON_BODIES:
        if re.search(rf"\b{re.escape(body)}\b", t):
            if body in {"picape"}:
                result["body_type"] = "pickup"
            elif body in {"cupe", "cupê", "coupe"}:
                result["body_type"] = "coupe"
            else:
                result["body_type"] = body.upper() if body == "suv" else body
            break

    # fuel_type
    for fuel in COMMON_FUELS:
        if re.search(rf"\b{re.escape(fuel)}\b", t):
            if fuel == "eletrico":
                result["fuel_type"] = "elétrico"
            elif fuel == "hibrido":
                result["fuel_type"] = "híbrido"
            else:
                result["fuel_type"] = fuel
            break

    # make (exato) e model (fuzzy)
    for make in KNOWN_MAKES:
        if _norm(make) in t:
            result["make"] = make
            break

    # tenta detectar um token que pareça modelo e aplicar fuzzy
    tokens = [tok for tok in re.findall(r"[A-Za-zÀ-ÿ0-9\-]+", raw) if len(tok) >= 2]
    # exemplos: "HVR" → "HR-V", "tcross" → "T-Cross"
    cand_model = None
    for tok in tokens:
        match = _fuzzy_one(tok, KNOWN_MODELS, cutoff=0.75)
        if match:
            cand_model = match
            break
    if cand_model:
        result["model"] = cand_model  # o servidor só filtrará por model se suportar

    # estado (sigla) – tokens 2 letras maiúsculas no original
    for token in re.findall(r"\b[A-Z]{2}\b", raw):
        if token in BR_STATES:
            result["state"] = token
            break

    # anos
    m = re.search(r"entre\s*(20\d{2}|19\d{2})\s*e\s*(20\d{2}|19\d{2})", t)
    if m:
        y1, y2 = int(m.group(1)), int(m.group(2))
        result["year_min"], result["year_max"] = min(y1, y2), max(y1, y2)
    else:
        m = re.search(r"(de|a partir de|pra cima de|acima de)\s*(20\d{2}|19\d{2})", t)
        if m:
            result["year_min"] = int(m.group(2))
        m = re.search(r"\bate\s*(20\d{2}|19\d{2})", t)
        if m:
            result["year_max"] = int(m.group(1))

    # preço
    m = re.search(r"\bate\s*([\d\.\, ]+(?:mil)?)", t)
    if m:
        p = _parse_money_raw(m.group(1))
        if p is not None:
            result["price_max"] = p
    else:
        m = PRICE_RE.search(raw)
        if m:
            p = _parse_money_raw(m.group(1))
            if p is not None:
                result["price_max"] = p

    result.setdefault("limit", 20)
    return result

# ----------------------------
# Renderização
# ----------------------------
def render_results(items: list[dict]) -> None:
    if not items:
        console.print("[yellow]Nenhum veículo encontrado com esses critérios.[/yellow]")
        return

    table = Table(title=f"Resultados ({len(items)})")
    table.add_column("Marca", style="bold")
    table.add_column("Modelo")
    table.add_column("Ano", justify="right")
    table.add_column("Cor")
    table.add_column("KM", justify="right")
    table.add_column("Preço (R$)", justify="right")

    for it in items:
        km = it.get("mileage_km", 0)
        price = it.get("price", 0.0)
        table.add_row(
            str(it.get("make", "")),
            str(it.get("model", "")),
            str(it.get("year", "")),
            str(it.get("color", "")),
            f"{km:,}".replace(",", "."),
            f"{price:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."),
        )

    console.print(table)

def mcp_query(filters: dict, *, host: Optional[str] = None, port: Optional[int] = None, timeout: float = 5.0) -> dict:
    host = host or Settings_Cars.server_host_c2s
    port = port or Settings_Cars.server_port_c2s
    env = {
        "kind": "query",
        "id": str(uuid.uuid4()),
        "payload": {"filters": filters or {}},
    }
    blob = (json.dumps(env, ensure_ascii=False) + "\n").encode("utf-8")
    with socket.create_connection((host, port), timeout=timeout) as s, s.makefile("r", encoding="utf-8") as reader:
        s.sendall(blob)
        line = reader.readline()
    if not line:
        return {"kind": "error", "id": env["id"], "payload": {"message": "Resposta vazia do servidor"}}
    try:
        return json.loads(line)
    except Exception as e:
        return {"kind": "error", "id": env["id"], "payload": {"message": f"Falha ao parsear resposta: {e}"}}

def interactive_relax(filters: dict) -> dict:
    """
    Quando não houver resultados, sugere correções e relaxamentos.
    Retorna os filtros possivelmente modificados.
    """
    new_filters = dict(filters)

    # Sugere relax de preço
    if "price_max" in new_filters:
        console.print("[yellow]Sem resultados.[/yellow] Posso aumentar o teto de preço em ~20%?")
        if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
            new_filters["price_max"] = int(new_filters["price_max"] * 1.2)

    # Sugere relax de ano mínimo
    if "year_min" in new_filters:
        console.print("Quer considerar 1–2 anos mais antigos?")
        if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
            new_filters["year_min"] = max(1990, new_filters["year_min"] - 2)

    # Sugere remover combustível
    if "fuel_type" in new_filters:
        console.print("Tiro a preferência de combustível para ampliar opções?")
        if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
            new_filters.pop("fuel_type", None)

    # Sugere remover tipo de carroceria
    if "body_type" in new_filters:
        console.print("Posso considerar outras carrocerias além da escolhida?")
        if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
            new_filters.pop("body_type", None)

    return new_filters

# ----------------------------
# Modo testes: corretas e falsas
# ----------------------------
TEST_QUERIES = [
    # corretas (devem retornar algo em geral)
    "Sedan flex até 80.000 de 2018 pra cima",
    "SUV a diesel entre 2016 e 2019 em SP",
    "Toyota até 120000",
    # “falsas”/difíceis (typos, restrições duras)
    "quero HVR",                 # typo → HR-V
    "tcross até 50 mil 2022",    # possivelmente muito barato → testar relax
    "Picape elétrica 2015",      # combinação rara → relax/remover combustível
]

def run_tests():
    console.print("[bold]Rodando testes (corretas e falsas)…[/bold]")
    for q in TEST_QUERIES:
        console.print(f"\n[green]> {q}[/green]")
        filters = parse_user_query(q)
        console.print(f"[dim]Filtros:[/dim] {filters}")
        resp = mcp_query(filters)
        if resp.get("kind") == "error":
            console.print(f"[red]Erro:[/red] {resp.get('payload', {}).get('message')}")
            continue
        items = resp.get("payload", {}).get("items", [])
        if not items:
            console.print("[yellow]Sem resultados. Tentando relaxar…[/yellow]")
            relaxed = interactive_relax(filters)
            console.print(f"[dim]Novos filtros:[/dim] {relaxed}")
            resp = mcp_query(relaxed)
            items = resp.get("payload", {}).get("items", [])
        render_results(items)

# ----------------------------
# CLI principal
# ----------------------------
def main() -> None:
    console.print("[bold]Bem-vindo![/bold] Me diga o que você procura. Ex.: 'Quero um sedan flex até 80.000, de 2018 pra cima'.")
    console.print("[dim]Comandos: :tests para rodar perguntas corretas e falsas; :q para sair[/dim]")

    while True:
        user = console.input("\n[cyan]Você> [/cyan]")
        if user.strip().lower() in {":q", "sair", "exit", "quit"}:
            break
        if user.strip().lower() == ":tests":
            run_tests()
            continue

        filters = parse_user_query(user) or {}
        console.print(f"[dim]Consultando com filtros:[/dim] {filters}")
        resp = mcp_query(filters)
        if resp.get("kind") == "error":
            console.print(f"[red]Erro:[/red] {resp.get('payload', {}).get('message')}")
            continue

        items = resp.get("payload", {}).get("items", [])
        if items:
            render_results(items)
            continue

        # Sem resultados: tente corrigir/relaxar
        console.print("[yellow]Nenhum veículo encontrado.[/yellow]")
        # Sugestão de correção se foi detectado um modelo fuzzy
        p = parse_user_query(user)   
        if p.get("model") and _norm(p["model"]) not in _norm(user):
            console.print(f"Você quis dizer [bold]{p['model']}[/bold]?")
        filters = interactive_relax(filters)
        console.print(f"[dim]Reconsultando:[/dim] {filters}")
        resp = mcp_query(filters)
        items = resp.get("payload", {}).get("items", [])
        render_results(items)

if __name__ == "__main__":
    main()

