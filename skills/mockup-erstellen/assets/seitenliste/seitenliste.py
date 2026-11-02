"""Erzeugt aus der Quelldatei die Seitenliste: Doku und veröffentlichte Seite (Standard: mockup-erstellen,
references/seitenliste.md).

Aufruf: python3 tools/seitenliste.py [--abnahme <nr> ... | --abnahme alle]
Alle Projektwerte stehen in tools/seitenliste.config.json. --abnahme setzt den Fingerabdruck der Code-Dateien neu.
"""

from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

WURZEL = Path(__file__).resolve().parent.parent


def config() -> dict:
    return json.loads((WURZEL / "tools/seitenliste.config.json").read_text(encoding="utf8"))


def lesen(cfg: dict) -> list[dict]:
    return json.loads((WURZEL / cfg["quelle"]).read_text(encoding="utf8"))


def schreiben(cfg: dict, gruppen: list[dict]) -> None:
    (WURZEL / cfg["quelle"]).write_text(json.dumps(gruppen, ensure_ascii=False, indent=1) + "\n", encoding="utf8")


def md(cfg: dict, gruppen: list[dict]) -> str:
    aus = [
        f"# {cfg['titel']}\n",
        f"Erzeugt aus `{cfg['quelle']}` (`python3 tools/seitenliste.py`) – dort ändern, nicht hier. Die **Nr.** ist der",
        "feste Ort einer Seite. Je Seite zwei Versionen: läuft **Mockup** vor **Code**, ist es abgenommen, aber noch nicht",
        "gebaut. **1.0** = überarbeitet und abgenommen, **0.1** = noch nicht durchgegangen.\n",
    ]
    for g in gruppen:
        aus += [
            f"## {g['nr']} {g['bereich']}\n",
            "| Nr. | Seite | Art | Version Mockup | Version Code | Mockup | Code |",
            "|---|---|---|---|---|---|---|",
        ]
        for s in g["seiten"]:
            m = s.get("mockup") or (f"{s['mockup_alt']} (alt)" if s.get("mockup_alt") else "–")
            aus.append(
                f"| {s['nr']} | {s['name']} | {s['art']} | {s.get('version_mockup') or '–'} "
                f"| {s.get('version_code') or '–'} | `{m}` | `{s.get('code') or '–'}` |"
            )
        aus.append("")
    return "\n".join(aus)


def html(cfg: dict, gruppen: list[dict]) -> str:
    vorlage = (WURZEL / cfg["vorlage"]).read_text(encoding="utf8")
    daten = json.dumps(gruppen, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    tabellen = {"schema": None, "gruppen": []}
    if cfg.get("daten"):
        tabellen = json.loads((WURZEL / cfg["daten"]["quelle"]).read_text(encoding="utf8"))
    tabellen_text = json.dumps(tabellen, ensure_ascii=False, separators=(",", ":")).replace("</", "<\\/")
    return (
        vorlage.replace("@@TITEL@@", cfg["titel"]).replace("@@START@@", cfg["start"])
        .replace("@@DATEN@@", daten).replace("@@TABELLEN@@", tabellen_text)
    )  # fmt: skip


def dateien(s: dict) -> list[str]:
    return sorted(x.strip() for x in (s.get("code") or "").split(",") if x.strip())


def stand(cfg: dict, s: dict) -> str:
    """Fingerabdruck der Code-Dateien einer Seite; ändert sich der Code ohne neue Version, meldet der Abgleich es."""
    h = hashlib.sha1(usedforsecurity=False)
    for d in dateien(s):
        h.update((WURZEL / cfg["code_wurzel"] / d).read_bytes())
    return h.hexdigest()[:10]


def main() -> None:
    cfg = config()
    gruppen = lesen(cfg)
    abnahme = sys.argv[sys.argv.index("--abnahme") + 1 :] if "--abnahme" in sys.argv else []
    for g in gruppen:
        for s in g["seiten"]:
            s.setdefault("zu", [])
            s.setdefault("nutzt", [])
            s.setdefault("verlauf", [])
            if s["nr"] in abnahme or "alle" in abnahme or "code_stand" not in s:
                s["code_stand"] = stand(cfg, s)
    schreiben(cfg, gruppen)
    (WURZEL / cfg["doku"]).write_text(md(cfg, gruppen), encoding="utf8")
    (WURZEL / cfg["seite"]).write_text(html(cfg, gruppen), encoding="utf8")


if __name__ == "__main__":
    main()
