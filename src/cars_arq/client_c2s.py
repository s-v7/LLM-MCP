from __future__ import annotations

import difflib
import json
import re
import socket
import unicodedata
import uuid
from typing import Optional
from decimal import Decimal, ROUND_DOWN

from rich.console import Console
from rich.table import Table

from .configs import Settings_Cars

console = Console()

COMMON_FUELS = {"gasolina", "etanol", "flex", "diesel", "elétrico", "eletrico", "híbrido", "hibrido"}
COMMON_BODIES = {
    "hatch",
    "sedan",
    "suv",
    "pickup",
    "picape",
    "coupe",
    "cupe",
    "cupê",
}

BR_STATES = {
    "AC",
    "AL",
    "AP",
    "AM",
    "BA",
    "CE",
    "DF",
    "ES",
    "GO",
    "MA",
    "MT",
    "MS",
    "MG",
    "PA",
    "PB",
    "PR",
    "PE",
    "PI",
    "RJ",
    "RN",
    "RS",
    "RO",
    "RR",
    "SC",
    "SP",
    "SE",
    "TO",
}

KNOWN_MAKES = [
    "Toyota",
    "Honda",
    "Volkswagen",
    "Chevrolet",
    "Fiat",
    "Ford",
    "Hyundai",
]

KNOWN_MODELS = [
    "Corolla",
    "Etios",
    "Yaris",
    "Hilux",
    "RAV4",
    "Civic",
    "Fit",
    "HR-V",
    "City",
    "Golf",
    "Polo",
    "T-Cross",
    "Nivus",
    "Virtus",
    "Onix",
    "Prisma",
    "Tracker",
    "S10",
    "Argo",
    "Pulse",
    "Toro",
    "Cronos",
    "Ka",
    "Fusion",
    "Ranger",
    "HB20",
    "Creta",
    "Tucson",
]

TEST_QUERIES = [
    "Sedan flex até 80.000 de 2018 pra cima",
    "SUV a diesel entre 2016 e 2019 em SP",
    "Toyota até 120000",
    "quero HVR",
    "tcross até 50 mil 2022",
    "Picape elétrica 2015",
]

PRICE_RE = re.compile(r"(\d{2,3}[\.]?\d{3}|\d{4,6})(?:\s*(?:reais|r\$))?", re.I)

MODEL_ANALIASES = {
    "hrv": "HR-V",
    "hvr": "HR-V",
    "hr-v": "HR-V",
    "tcross": "T-Cross",
    "t-cross": "T-Cross",
    "t cross": "T-Cross",
}


def _norm(txt: str) -> str:
    return (
        unicodedata.normalize("NFKD", txt or "")
        .encode("ascii", "ignore")
        .decode("ascii")
        .lower()
    )


def _looks_like_year(n: int) -> bool:
    return 1900 <= n <= 2025


def _parse_money_raw(token: str) -> Optional[int]:
    if not token:
        return None
    t = token.strip().lower().replace(" ", "")
    mil_flag = "mil" in t
    t = t.replace("mil", "").replace(".", "").replace(",", ".")
    m = re.search(r"\d+(?:\.\d+)?", t)
    if not m:
        return None
    val = Decimal(m.group(0))
    if mil_flag and val < Decimal(1000):
        val *= Decimal(1000)
    val = val.quantize(Decimal("1"), rounding=ROUND_DOWN)
    return int(val)


def _fuzzy_one(token: str, population: list[str], *, cutoff: float = 0.7) -> Optional[str]:
    if not token:
        return None
    matches = difflib.get_close_matches(token, population, n=1, cutoff=cutoff)
    return matches[0] if matches else None


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


def mcp_query(
    filters: dict,
    *,
    host: Optional[str] = None,
    port: Optional[int] = None,
    timeout: float = 5.0,
) -> dict:
    host = host or Settings_Cars.server_host_c2s
    port = port or Settings_Cars.server_port_c2s
    env = {
        "kind": "query",
        "id": str(uuid.uuid4()),
        "payload": {"filters": filters or {}},
    }
    blob = (json.dumps(env, ensure_ascii=False) + "\n").encode("utf-8")
    with socket.create_connection((host, port), timeout=timeout) as s, s.makefile(
        "r", encoding="utf-8"
    ) as reader:
        s.sendall(blob)
        line = reader.readline()
    if not line:
        return {"kind": "error", "id": env["id"], "payload": {"message": "Resposta vazia do servidor"}}
    try:
        return json.loads(line)
    except Exception as e:
        return {"kind": "error", "id": env["id"], "payload": {"message": f"Falha ao parsear resposta: {e}"}}


def interactive_relax(filters: dict, *, ask: bool = True) -> dict:
    new_filters = dict(filters)
    if "price_max" in new_filters:
        if ask:
            console.print("[yellow]Sem resultados.[/yellow] Posso aumentar o teto de preço em ~20%?")
            if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
                new_filters["price_max"] = int(new_filters["price_max"] * 1.2)
            else:
                new_filters["price_max"] = int(new_filters["price_max"] * 1.2)
        else:
            new_filters["price_max"] = int(new_filters["price_max"] * 1.2)
    if "year_min" in new_filters:
        if ask:
            console.print("Quer considerar 1–2 anos mais antigos?")
            if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
                new_filters["year_min"] = max(1990, new_filters["year_min"] - 2)
            else:
                new_filters["year_min"] = max(1990, new_filters["year_min"] - 2)
        else:
            new_filters["year_min"] = max(1990, new_filters["year_min"] - 2)
    if "fuel_type" in new_filters:
        if ask:
            console.print("Tiro a preferência de combustível para ampliar opções?")
            if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
                new_filters.pop("fuel_type", None)
            else:
                new_filters.pop("fuel_type", None)
        else:
            new_filters.pop("fuel_type", None)
    if "body_type" in new_filters:
        if ask:
            console.print("Posso considerar outras carrocerias além da escolhida?")
            if console.input("[cyan](s/N)> [/cyan]").strip().lower() == "s":
                new_filters.pop("body_type", None)
            else:
                new_filters.pop("body_type", None)
        else:
            new_filters.pop("body_type", None)
    console.print("[bold]Rodando testes (corretas e falsas)…[/bold]")
    try:
        for q in TEST_QUERIES:
            console.print(f"\n[green]> {q}[/green]")
            f = parse_user_query(q)
            console.print(f"[dim]Filtros:[/dim] {f}")
            resp = mcp_query(f)
            if resp.get("kind") == "error":
                console.print(f"[red]Erro:[/red] {resp.get('payload', {}).get('message')}")
                continue
            items = resp.get("payload", {}).get("items", [])
            if not items:
                console.print("[yellow]Sem resultados. Tentando relaxar…[/yellow]")
                relaxed = interactive_relax(f, ask=False)
                console.print(f"[dim]Novos filtros:[/dim] {relaxed}")
                resp = mcp_query(relaxed)
                items = resp.get("payload", {}).get("items", [])
            render_results(items)
    except (KeyboardInterrupt, EOFError):
        console.print("\n[red]Teste interrompido pelo usuário.[/red]")
    return new_filters


def parse_user_query(text: str) -> dict:
    result: dict = {}
    if not text:
        result.setdefault("limit", 20)
        return result

    raw = text.strip()
    t = _norm(raw)

    for body in COMMON_BODIES:
        if re.search(rf"\b{re.escape(body)}\b", t):
            if body in {"picape"}:
                result["body_type"] = "pickup"
            elif body in {"cupe", "cupê", "coupe"}:
                result["body_type"] = "coupe"
            else:
                result["body_type"] = body.upper() if body == "suv" else body
            break

    fuel_patterns = [
        (r"\beletric\w*\b", "elétrico"),
        (r"\bhibrid\w*\b", "híbrido"),
        (r"\bdiesel\b", "diesel"),
        (r"\bgasolina\b", "gasolina"),
        (r"\betanol\b", "etanol"),
        (r"\bflex\b", "flex"),
    ]
    for pat, fuel_norm in fuel_patterns:
        if re.search(pat, t):
            result["fuel_type"] = fuel_norm
            break

    for make in KNOWN_MAKES:
        if _norm(make) in t:
            result["make"] = make
            break

    tokens = [tok for tok in re.findall(r"[A-Za-zÀ-ÿ0-9\-]+", raw) if len(tok) >= 2]
    cand_model = None
    norm_models = [_norm(m) for m in KNOWN_MODELS]
    for tok in tokens:
        tnorm = _norm(tok).replace("-", " ")
        if tnorm in MODEL_ANALIASES:
            cand_model = MODEL_ANALIASES[tnorm]
            break
        match = _fuzzy_one(tnorm, norm_models, cutoff=0.72)
        if match:
            cand_model = KNOWN_MODELS[norm_models.index(match)]
            break
    if cand_model:
        result["model"] = cand_model

    for token in re.findall(r"\b[A-Z]{2}\b", raw):
        if token in BR_STATES:
            result["state"] = token
            break

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

    w = re.search(r"\b(at[eé]|no maximo|no máximo|por at[eé])\s*([\d\.\, ]+(?:mil)?)", t)
    if w:
        p = _parse_money_raw(w.group(2))
        if p is not None:
            result["price_max"] = p
    else:
        w = PRICE_RE.search(raw)
        if w:
            p = _parse_money_raw(w.group(1))
            if p is not None:
                result["price_max"] = p
        m2 = re.search(r"(r\$)?\s*([\d\.\, ]+(?:\s*mil)?)", t, re.I)
        if m2:
            has_currency = bool(m2.group(1)) or ("mil" in m2.group(2))
            p = _parse_money_raw(m2.group(2))
            if p is not None:
                if has_currency or not _looks_like_year(p):
                    result["price_max"] = p
        if "price_max" in result and ("year_min" not in result and "year_max" not in result):
            tail_year = re.search(r"(20\d{2}|19\d{2})\b", t[::-1])
            if not tail_year:
                years = re.findall(r"(20\d{2}|19\d{2})", t)
                if years:
                    result["year_min"] = int(years[-1])

    result.setdefault("limit", 20)
    return result


def main() -> None:
    console.print(
        "[bold]Bem-vindo![/bold] Me diga o que você procura. Ex.: 'Quero um sedan flex até 80.000, de 2018 pra cima'."
    )
    console.print("[dim]Comandos: :tests para rodar perguntas corretas e falsas; :q para sair[/dim]")
    while True:
        try:
            user = console.input("\n[cyan]Você> [/cyan]")
        except (KeyboardInterrupt, EOFError):
            console.print("\n[red]Encerrando…[/red]")
            break
        low = user.strip().lower()
        if low in {":q", "sair", "exit", "quit"}:
            break
        if low == ":tests":
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
        console.print("[yellow]Nenhum veículo encontrado.[/yellow]")
        p = parse_user_query(user)
        if p.get("model") and _norm(p["model"]) not in _norm(user):
            console.print(f"Você quis dizer [bold]{p['model']}[/bold]?")
        filters = interactive_relax(filters, ask=True)
        console.print(f"[dim]Reconsultando:[/dim] {filters}")
        resp = mcp_query(filters)
        items = resp.get("payload", {}).get("items", [])
        render_results(items)


if __name__ == "__main__":
    main()
