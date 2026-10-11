#!/usr/bin/env python3
"""Versionen der Werkzeuge in templates/versions.json mit PyPI vergleichen (nur Standardbibliothek).

projekt-anlegen ruft das vor jedem neuen Projekt auf und nennt neuere Versionen; es ist nur ein Hinweis. Angehoben
wird erst nach grüner CI des Generators (references/generator.md, Pflege der Vorlagen).

    python3 versionen.py [--json]

Exit immer 0; ohne Netz steht beim Paket „nicht prüfbar“.
"""

import argparse
import json
import sys
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auftrag import TEMPLATES  # noqa: E402

PYPI = "https://pypi.org/pypi/{name}/json"
TIMEOUT = 10
# Pakete, die nur gemeinsam angehoben werden: das HA-Testpaket gehört zu genau einer HA-Version
GEKOPPELT = {"homeassistant": "pytest-homeassistant-custom-component",
             "pytest-homeassistant-custom-component": "homeassistant"}


def neueste(name):
    """Neueste stabile Version auf PyPI oder None, wenn PyPI nicht erreichbar ist."""
    try:
        with urllib.request.urlopen(PYPI.format(name=name), timeout=TIMEOUT) as antwort:
            return json.load(antwort)["info"]["version"]
    except (urllib.error.URLError, OSError, ValueError, KeyError):
        return None


def _teile(version):
    try:
        return tuple(int(t) for t in version.split("."))
    except ValueError:
        return None


def vergleichen(angeheftet, abfrage=neueste):
    """[{paket, angeheftet, neueste, stand}] mit stand: aktuell, neuer, nicht prüfbar."""
    zeilen = []
    for name, version in sorted(angeheftet.items()):
        neu = abfrage(name)
        if neu is None:
            stand = "nicht prüfbar"
        else:
            alt_t, neu_t = _teile(str(version)), _teile(neu)
            stand = "neuer" if (neu_t > alt_t if alt_t and neu_t else neu != str(version)) else "aktuell"
        zeilen.append({"paket": name, "angeheftet": str(version), "neueste": neu or "–", "stand": stand})
    return zeilen


def tabelle(zeilen):
    text = ["| Paket | angeheftet | neueste | Stand |", "|---|---|---|---|"]
    for z in zeilen:
        hinweis = f" (nur zusammen mit {GEKOPPELT[z['paket']]})" if z["stand"] == "neuer" and z["paket"] in GEKOPPELT else ""
        text.append(f"| {z['paket']} | {z['angeheftet']} | {z['neueste']} | {z['stand']}{hinweis} |")
    return "\n".join(text)


def main(argv=None):
    parser = argparse.ArgumentParser(description="versions.json mit PyPI vergleichen")
    parser.add_argument("--json", action="store_true", help="Ergebnis als JSON")
    args = parser.parse_args(argv)
    with open(Path(TEMPLATES) / "versions.json", encoding="utf-8") as fh:
        zeilen = vergleichen(json.load(fh))
    print(json.dumps(zeilen, ensure_ascii=False, indent=2) if args.json else tabelle(zeilen))
    return 0


if __name__ == "__main__":
    sys.exit(main())
