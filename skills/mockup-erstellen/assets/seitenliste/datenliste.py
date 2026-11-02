"""Erzeugt die Datenliste: Quelldatei und Doku, wo was gespeichert ist (Reiter „Daten“ der Seitenliste).

Aufruf: python3 tools/datenliste.py, danach python3 tools/seitenliste.py. Der Aufbau kommt aus `schema_befehl` der Config,
der ein frisch erzeugtes, leeres Schema als JSON ausgibt; echte Daten werden nie gelesen, die Liste zeigt nur Aufbau.
Zuordnung und Zweck stehen in tools/seitenliste.config.json unter `daten`.
"""

from __future__ import annotations

import json
import subprocess
import sys

import seitenliste as sl


def schema(d: dict) -> dict:
    """{"version": …, "tabellen": {name: {"felder": [[name, typ, schlüssel]], "fk": [tabelle]}}}"""
    lauf = subprocess.run(d["schema_befehl"], cwd=sl.WURZEL, capture_output=True, text=True, check=True)
    return json.loads(lauf.stdout)


def aufbauen(d: dict, stand: dict) -> dict:
    tabellen = stand["tabellen"]
    nr = {t: f"D{i}.{j}" for i, g in enumerate(d["gruppen"], 1) for j, t in enumerate(g["tabellen"], 1)}
    gruppen = []
    for i, g in enumerate(d["gruppen"], 1):
        zeilen = []
        for t, zweck in g["tabellen"].items():
            x = tabellen[t]
            zu = sorted(nr[z] for z in x["fk"] if z != t)
            zeilen.append({"nr": nr[t], "name": t, "art": "Tabelle", "zweck": zweck, "felder": x["felder"], "zu": zu})
        gruppen.append({"nr": f"D{i}", "bereich": g["bereich"], "seiten": g.get("seiten", []), "seiten_liste": zeilen})
    for i, o in enumerate(d.get("orte", []), 1):
        zeilen = [
            {"nr": f"S{i}.{j}", "name": n, "art": o["art"], "zweck": z, "felder": [], "zu": []}
            for j, (n, z) in enumerate(o["eintraege"].items(), 1)
        ]
        gruppen.append({"nr": f"S{i}", "bereich": o["bereich"], "seiten": o.get("seiten", []), "seiten_liste": zeilen})
    return {"schema": stand.get("version"), "gruppen": gruppen}


def md(daten: dict) -> str:
    aus = [f"# Daten\n\nErzeugt von `tools/datenliste.py` aus einem leeren Schema ({daten['schema']}). Nur Aufbau, keine Inhalte.\n"]
    for g in daten["gruppen"]:
        aus += [f"## {g['nr']} {g['bereich']}\n", "| Nr. | Name | Zweck | Felder | Verweist auf |", "|---|---|---|---|---|"]
        for z in g["seiten_liste"]:
            aus.append(f"| {z['nr']} | `{z['name']}` | {z['zweck']} | {len(z['felder']) or '–'} | {', '.join(z['zu']) or '–'} |")
        aus.append("")
    return "\n".join(aus)


def eingeordnet(d: dict) -> set[str]:
    return {t for g in d["gruppen"] for t in g["tabellen"]}


def main() -> int:
    d = sl.config()["daten"]
    stand = schema(d)
    fehlt = sorted(set(stand["tabellen"]) - eingeordnet(d))
    if fehlt:
        print("nicht eingeordnet (Config, daten.gruppen):", ", ".join(fehlt))
        return 1
    daten = aufbauen(d, stand)
    (sl.WURZEL / d["quelle"]).write_text(json.dumps(daten, ensure_ascii=False, indent=1) + "\n", encoding="utf8")
    (sl.WURZEL / d["doku"]).write_text(md(daten), encoding="utf8")
    return 0


if __name__ == "__main__":
    sys.exit(main())
