#!/usr/bin/env python3
"""Projekt-Generator von projekt-anlegen (nur Standardbibliothek): Erzeugungsauftrag → Projektdateien.

Ablauf und Grenzen: references/generator.md. Dieses Modul erzeugt die Dateien eines geprüften Auftrags in einen
leeren Ordner (`erzeugen`, Prepare); `anlegen` prüft und veröffentlicht (Verify & Publish) und räumt bei jedem
Fehler alles weg. Aufruf durch den Skill:

    python3 generate.py --auftrag auftrag.json --ablage <Projekte.Ablage> [--werkzeugablage <Projekte.Werkzeugablage>]

Mit Werkzeugablage liegt die Umgebung (.venv) unter <werkzeugablage>/<slug>/.venv, im Projekt steht ein Verweis.

Ausgabe: JSON mit ok, phase, ziel, dateien, pruefungen (name, dauer, ok, ausgabe) und fehler; Exit 0 nur bei ok.
"""

import argparse
import json
import os
import shutil
import sys
import tempfile
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from auftrag import TEMPLATES, AuftragFehler, manifeste, pruefen, zielordner  # noqa: E402
from bausteine import auswahl, aufloesen, dateiplan, ersetzen, komponenten, versionen, werte  # noqa: E402
from pruefung import ausfuehren, verweis  # noqa: E402

GENERATOR_VERSION = "1.0.0"
HERKUNFT = ".projekt-anlegen.json"


def _syntax(ziel, text):
    """Strukturierte Dateien nach dem Ersetzen prüfen: ein Platzhalterwert darf sie nie unlesbar machen."""
    try:
        if ziel.endswith(".toml"):
            tomllib.loads(text)
        elif ziel.endswith(".json"):
            json.loads(text)
    except (tomllib.TOMLDecodeError, json.JSONDecodeError) as exc:
        raise AuftragFehler([f"{ziel}: nach dem Ersetzen ungültig ({exc})"]) from None


def herkunft(auftrag, reihenfolge):
    """Inhalt von .projekt-anlegen.json: nur Herkunft, ohne Datum – gleicher Auftrag, gleiche Datei."""
    return {
        "schema_version": 1,
        "generator": {"name": "projekt-anlegen", "version": GENERATOR_VERSION},
        "template": dict(auftrag["template"]),
        "components": list(reihenfolge),
    }


def erzeugen(auftrag, ordner, templates=TEMPLATES):
    """Schreibt das Projekt in `ordner` (muss existieren und leer sein); gibt die Liste der Dateien zurück."""
    templates = Path(templates)
    arten = manifeste(templates)
    pruefen(auftrag, arten)
    katalog = komponenten(templates)
    reihenfolge = aufloesen(auswahl(auftrag, arten[auftrag["template"]["id"]]), katalog)
    platzhalter = werte(auftrag, versionen(templates))
    plan = dateiplan(reihenfolge, katalog, platzhalter, templates)

    ordner = Path(ordner)
    if not ordner.is_dir() or any(ordner.iterdir()):
        raise AuftragFehler([f"{ordner}: muss ein vorhandener, leerer Ordner sein"])

    inhalte = []
    for quelle, ziel in plan:
        text = ersetzen(quelle.read_text(encoding="utf-8"), platzhalter, quelle.relative_to(templates).as_posix())
        _syntax(ziel, text)
        inhalte.append((ziel, text))
    inhalte.append((HERKUNFT, json.dumps(herkunft(auftrag, reihenfolge), ensure_ascii=False, indent=2) + "\n"))

    for ziel, text in inhalte:  # erst alles rendern, dann schreiben: ein Fehler hinterlässt keine halben Dateien
        pfad = ordner / ziel
        pfad.parent.mkdir(parents=True, exist_ok=True)
        with open(pfad, "w", encoding="utf-8", newline="\n") as fh:
            fh.write(text)
    return [ziel for ziel, _ in inhalte]


def anlegen(auftrag, ablage, templates=TEMPLATES, pruefen_=True, *, werkzeugablage=None):
    """Prepare → Verify → Publish. Erzeugt zweimal in einen Zwischenordner der Ablage (gleiches Dateisystem): eine
    Fassung wird geprüft (mit .venv und Caches), die andere, saubere wird nach grüner Prüfung an ihren Platz
    verschoben. Bei jedem Fehler bleibt nichts zurück. Ergebnis als dict für den Skill (references/generator.md).
    Mit `werkzeugablage` liegt die Prüf-Umgebung vorübergehend dort; nach dem Veröffentlichen wird die Umgebung des
    Projekts unter <werkzeugablage>/<slug>/.venv eingerichtet und im Projekt verwiesen."""
    templates = Path(templates)
    ergebnis = {"ok": False, "phase": "auftrag", "pruefungen": []}
    try:
        pruefen(auftrag, manifeste(templates))
        ziel = zielordner(ablage, auftrag["project"]["slug"])
    except AuftragFehler as exc:
        return dict(ergebnis, fehler=exc.fehler)
    ergebnis["ziel"] = str(ziel)
    werkzeug = None
    if werkzeugablage:
        werkzeug = Path(werkzeugablage).resolve() / auftrag["project"]["slug"]
        if os.path.lexists(werkzeug):
            return dict(ergebnis, fehler=[f"Werkzeugablage {werkzeug}: existiert schon – nichts angelegt"])
        ergebnis["werkzeug"] = str(werkzeug / ".venv")
    art = manifeste(templates)[auftrag["template"]["id"]]
    zwischen = Path(tempfile.mkdtemp(prefix=".projekt-anlegen-", dir=ziel.parent))
    pruef_venv = Path(werkzeugablage).resolve() / zwischen.name / ".venv" if werkzeug else None
    try:
        ergebnis["phase"] = "erzeugen"
        pruef, sauber = zwischen / "pruefung", zwischen / "projekt"
        pruef.mkdir()
        sauber.mkdir()
        try:
            dateien = erzeugen(auftrag, pruef, templates)
            erzeugen(auftrag, sauber, templates)
        except AuftragFehler as exc:
            return dict(ergebnis, fehler=exc.fehler)
        ergebnis["dateien"] = dateien

        if pruefen_:
            ergebnis["phase"] = "pruefen"
            ok, ergebnis["pruefungen"] = ausfuehren(art.get("pruefung", {}), pruef, auftrag["project"]["package"],
                                                    venv=pruef_venv)
            if not ok:
                schritt = ergebnis["pruefungen"][-1]
                return dict(ergebnis, fehler=[f"Prüfung {schritt['name']} fehlgeschlagen – nichts angelegt"])

        ergebnis["phase"] = "veroeffentlichen"
        if os.path.lexists(ziel):  # erneut prüfen: in der Zwischenzeit angelegt?
            return dict(ergebnis, fehler=[f"Ziel {ziel}: existiert inzwischen – nichts angelegt"])
        if werkzeug:
            verweis(sauber, werkzeug / ".venv")
        try:
            os.rename(sauber, ziel)
        except OSError as exc:
            return dict(ergebnis, fehler=[f"Ziel {ziel}: Verschieben gescheitert ({exc}) – nichts angelegt"])
        if werkzeug and art.get("pruefung", {}).get("einrichten"):
            ergebnis["phase"] = "werkzeug"
            ok, schritte = ausfuehren(art["pruefung"], ziel, auftrag["project"]["package"], venv=werkzeug / ".venv",
                                      nur_einrichten=True)
            if not ok:  # das Projekt ist geprüft und angelegt; nur die Umgebung fehlt noch
                ergebnis["hinweise"] = [f"Umgebung unter {werkzeug / '.venv'} nicht eingerichtet: "
                                        f"{schritte[-1].get('ausgabe', '')}"]
        return dict(ergebnis, ok=True, phase="fertig")
    finally:
        shutil.rmtree(zwischen, ignore_errors=True)
        if pruef_venv:
            shutil.rmtree(pruef_venv.parent, ignore_errors=True)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Projekt-Generator von projekt-anlegen")
    parser.add_argument("--auftrag", required=True, help="Erzeugungsauftrag (JSON-Datei, - = stdin)")
    parser.add_argument("--ablage", required=True, help="Ordner, in dem das Projekt angelegt wird (Projekte.Ablage)")
    parser.add_argument("--werkzeugablage", help="Ordner für .venv und node_modules außerhalb des Projekts "
                        "(Projekte.Werkzeugablage); im Projekt steht dann ein Verweis")
    parser.add_argument("--ohne-pruefung", action="store_true", help="nur für Tests des Generators")
    args = parser.parse_args(argv)
    try:
        if args.auftrag == "-":
            daten = json.loads(sys.stdin.read())
        else:
            with open(args.auftrag, encoding="utf-8-sig") as fh:
                daten = json.load(fh)
    except (OSError, json.JSONDecodeError) as exc:
        print(json.dumps({"ok": False, "phase": "auftrag", "fehler": [f"Auftrag nicht lesbar: {exc}"]},
                         ensure_ascii=False))
        return 1
    ergebnis = anlegen(daten, args.ablage, pruefen_=not args.ohne_pruefung, werkzeugablage=args.werkzeugablage)
    print(json.dumps(ergebnis, ensure_ascii=False, indent=2))
    return 0 if ergebnis["ok"] else 1


if __name__ == "__main__":
    sys.exit(main())
