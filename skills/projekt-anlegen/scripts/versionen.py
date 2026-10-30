#!/usr/bin/env python3
"""Versionen der Werkzeuge in templates/versions.json mit PyPI vergleichen (nur Standardbibliothek).

projekt-anlegen ruft das vor jedem neuen Projekt auf und nennt neuere Versionen; es ist nur ein Hinweis. Angehoben
wird erst nach grüner CI des Generators (references/generator.md, Pflege der Vorlagen).

    python3 versionen.py [--json]

Exit immer 0; ohne Netz steht beim Paket „nicht prüfbar“, bei einer Version, die nicht nach PEP 440 lesbar ist,
„unklar“.
"""

import argparse
import json
import re
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


_PEP440 = re.compile(
    r"v?(?:(?P<epoch>\d+)!)?(?P<release>\d+(?:\.\d+)*)"
    r"(?:[-_.]?(?P<pre>alpha|beta|preview|pre|rc|a|b|c)[-_.]?(?P<pre_n>\d+)?)?"
    r"(?P<post>-\d+|[-_.]?(?:post|rev|r)[-_.]?\d*)?"
    r"(?:[-_.]?(?P<dev>dev)[-_.]?(?P<dev_n>\d+)?)?",
    re.IGNORECASE,
)
_PRE_RANG = {"a": 0, "alpha": 0, "b": 1, "beta": 1, "c": 2, "rc": 2, "pre": 2, "preview": 2}


def schluessel(version):
    """Sortierschlüssel nach PEP 440 (Epoche, Release, a/b/rc, post, dev) oder None; lokaler Teil (+…) zählt nicht."""
    m = _PEP440.fullmatch(str(version).strip().split("+", 1)[0])
    if not m:
        return None
    release = [int(t) for t in m["release"].split(".")]
    while len(release) > 1 and release[-1] == 0:  # 1.0 == 1.0.0
        release.pop()
    if m["pre"]:
        pre = (1, _PRE_RANG[m["pre"].lower()], int(m["pre_n"] or 0))
    elif m["dev"] and not m["post"]:  # 1.0.dev1 liegt vor 1.0a1
        pre = (0, 0, 0)
    else:
        pre = (2, 0, 0)
    post = (1, int(re.search(r"\d*$", m["post"]).group() or 0)) if m["post"] else (0, 0)
    dev = (0, int(m["dev_n"] or 0)) if m["dev"] else (1, 0)
    return int(m["epoch"] or 0), tuple(release), pre, post, dev


def vergleichen(angeheftet, abfrage=neueste):
    """[{paket, angeheftet, neueste, stand}] mit stand: aktuell, neuer, unklar, nicht prüfbar."""
    zeilen = []
    for name, version in sorted(angeheftet.items()):
        neu = abfrage(name)
        if neu is None:
            stand = "nicht prüfbar"
        else:
            alt_k, neu_k = schluessel(version), schluessel(neu)
            if alt_k is None or neu_k is None:
                stand = "unklar"  # nicht nach PEP 440 lesbar: nichts Neueres behaupten
            else:
                stand = "neuer" if neu_k > alt_k else "aktuell"
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
