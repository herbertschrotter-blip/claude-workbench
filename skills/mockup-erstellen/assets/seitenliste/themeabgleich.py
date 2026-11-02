"""Theme-Abgleich: sucht feste Werte in den Dateien der Seiten (references/seitenliste.md#Theme-Abgleich).

Aufruf: python3 tools/themeabgleich.py                       gibt die Treffer je Seite als JSON aus, ändert nichts
        python3 tools/themeabgleich.py --uebernehmen <datei> schreibt die bewerteten Treffer nach `ziel` der Config
Das Skript findet Muster und versteht kein CSS: Die Treffer bewertet Claude, erst danach kommen sie in die Seitenliste.
Die Hinweise blockieren nichts.
"""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path

import seitenliste as sl

FARBE = re.compile(r"""(?<![\w&])(?<!href=["'])#(?:[0-9a-fA-F]{8}|[0-9a-fA-F]{6}|[0-9a-fA-F]{3,4})\b|\b(?:rgb|hsl)a?\([^)]*\)""")
TOKEN = re.compile(r"--([\w-]+)\s*:\s*([^;}]+)")
PIXEL = re.compile(r"\d*\.?\d+(?:px|rem|em)\b")


def tokens(cfg: dict) -> dict[str, str]:
    """Wert → Token-Name aus den Theme-Dateien; bei gleichem Wert gilt der erste Token."""
    aus: dict[str, str] = {}
    for d in cfg["themeabgleich"]["token"]:
        for name, wert in TOKEN.findall((sl.WURZEL / d).read_text(encoding="utf8")):
            aus.setdefault(wert.strip().lower(), name)
    return aus


def treffer_zeile(zeile: str, ta: dict, werte: dict[str, str]) -> list[dict]:
    if TOKEN.search(zeile):
        return []  # Definition eines Tokens, kein Gebrauch
    ohne = re.sub(r"var\([^)]*\)", "", zeile)
    aus = []
    for m in FARBE.finditer(ohne):
        aus.append({"wert": m[0], "token": werte.get(m[0].lower())})
    for e in ta.get("eigenschaften", []):
        for m in re.finditer(rf"(?<![\w-]){re.escape(e)}\s*:\s*([^;}}\"'`]+)", ohne):
            aus += [
                {"wert": f"{e}: {p}", "token": werte.get(p.lower())}
                for p in PIXEL.findall(m[1])
                if p not in ta.get("ausnahmen", [])
            ]
    return aus


def suchen(cfg: dict, gruppen: list[dict]) -> dict[str, list[dict]]:
    ta, werte = cfg["themeabgleich"], tokens(cfg)
    aus: dict[str, list[dict]] = {}
    for s in (s for g in gruppen for s in g["seiten"]):
        for datei in sl.code_pfade(cfg, s) + sl.mockup_pfad(cfg, s):
            pfad = sl.WURZEL / datei
            if not pfad.exists() or datei in ta["token"]:
                continue
            for nr, zeile in enumerate(pfad.read_text(encoding="utf8").splitlines(), 1):
                for t in treffer_zeile(zeile, ta, werte):
                    aus.setdefault(s["nr"], []).append({"datei": datei, "zeile": nr, **t})
    return aus


def main() -> None:
    cfg = sl.config()
    if "--uebernehmen" in sys.argv:
        bewertet = json.loads(Path(sys.argv[sys.argv.index("--uebernehmen") + 1]).read_text(encoding="utf8"))
        text = json.dumps(bewertet, ensure_ascii=False, indent=1, sort_keys=True) + "\n"
        (sl.WURZEL / cfg["themeabgleich"]["ziel"]).write_text(text, encoding="utf8")
        return
    print(json.dumps(suchen(cfg, sl.lesen(cfg)), ensure_ascii=False, indent=1))


if __name__ == "__main__":
    main()
