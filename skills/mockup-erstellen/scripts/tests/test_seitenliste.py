#!/usr/bin/env python3
"""Tests der Vorlagen unter assets/seitenliste (nur Standardbibliothek)."""

import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ASSETS = Path(__file__).resolve().parents[2] / "assets/seitenliste"
THEME = "import pathlib; pathlib.Path('mockups/theme-app.css').write_text('neu')"


class SeitenlisteTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        w = self.w = Path(self.tmp.name)
        for d in ("tools", "mockups/seiten", "docs", "src"):
            (w / d).mkdir(parents=True)
        for f in ("seitenliste.py", "seitenbeziehungen.py", "seitenliste_check.py", "datenliste.py", "seitenliste_vorlage.html"):
            shutil.copy(ASSETS / f, w / "tools")
        (w / "src/app.js").write_text(
            "const ANSICHT = { start: a, detail: b }\nfunction startAnsicht() { oeffneDetail(); }\n", encoding="utf8"
        )
        (w / "mockups/theme-app.css").write_text("neu", encoding="utf8")
        (w / "mockups/seiten/start.html").write_text("M.start({ nr: '1.1', version: '1.0' })", encoding="utf8")
        self.cfg = {
            "titel": "Test", "quelle": "mockups/seiten.json", "doku": "docs/seiten.md", "seite": "mockups/index.html",
            "vorlage": "tools/seitenliste_vorlage.html", "mockup_ablage": "mockups", "code_wurzel": "src", "start": "1.1",
            "theme": {"befehl": [sys.executable, "-c", THEME], "dateien": ["mockups/theme-app.css"]},
            "seiten_im_code": [{"praefix": "ansicht", "datei": "src/app.js", "block": "const ANSICHT = \\{([^}]*)\\}",
                                "eintrag": "(\\w+)\\s*:"}],
            "beziehungen": {"dateien": "*.js", "kopf": "^(?:function\\s+(\\w+))", "einstieg": {"1.1": ["startAnsicht"]},
                            "ziel": {"\\boeffneDetail\\(": ["1.2"]}, "hand": {}, "bausteine": {"Karte": ["1.1", "1.2"]}},
        }  # fmt: skip
        self.gruppen = [{"nr": "1", "bereich": "Start", "seiten": [
            {"nr": "1.1", "name": "Start", "art": "Seite", "code": "app.js", "schluessel": ["ansicht:start"],
             "version_mockup": "1.0", "version_code": "0.1", "mockup": "seiten/start.html",
             "verlauf": [{"v": "1.0", "datum": "02.11.2026", "was": "neu"}]},
            {"nr": "1.2", "name": "Detail </script>", "art": "Blatt", "code": "app.js", "schluessel": ["ansicht:detail"],
             "version_mockup": None, "version_code": "0.1",
             "verlauf": [{"v": "0.1", "datum": "02.11.2026", "was": "aufgenommen"}]},
        ]}]  # fmt: skip
        self.schreiben()
        for befehl in ("seitenbeziehungen.py", "seitenliste.py"):
            self.lauf(befehl)

    def schreiben(self):
        (self.w / "tools/seitenliste.config.json").write_text(json.dumps(self.cfg), encoding="utf8")
        (self.w / "mockups/seiten.json").write_text(json.dumps(self.gruppen), encoding="utf8")

    def lauf(self, befehl, *args):
        return subprocess.run([sys.executable, str(self.w / "tools" / befehl), *args], cwd=self.w, capture_output=True,
                              text=True, check=False)  # fmt: skip

    def daten(self):
        return json.loads((self.w / "mockups/seiten.json").read_text(encoding="utf8"))

    def aendern(self, feld):
        g = self.daten()
        feld(g[0]["seiten"])
        (self.w / "mockups/seiten.json").write_text(json.dumps(g, ensure_ascii=False, indent=1) + "\n", encoding="utf8")

    def test_gruen(self):
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)
        self.assertIn("2 Seiten, 0 Fehler", r.stdout)

    def test_beziehungen_und_erzeugtes(self):
        s = self.daten()[0]["seiten"]
        self.assertEqual(s[0]["zu"], ["1.2"])
        self.assertEqual(s[0]["nutzt"], ["Karte"])
        html = (self.w / "mockups/index.html").read_text(encoding="utf8")
        self.assertNotIn("@@", html)
        self.assertNotIn("Detail </script>", html)
        self.assertIn("| 1.1 | Start |", (self.w / "docs/seiten.md").read_text(encoding="utf8"))

    def test_seite_im_code_fehlt_in_der_liste(self):
        (self.w / "src/app.js").write_text("const ANSICHT = { start: a, detail: b, neu: c }\n", encoding="utf8")
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 1)
        self.assertIn("ansicht:neu", r.stdout)

    def test_doppelte_nummer_und_tote_verbindung(self):
        def f(s):
            s[1]["nr"] = "1.1"
            s[0]["zu"] = ["9.9"]
        self.aendern(f)
        r = self.lauf("seitenliste_check.py")
        self.assertIn("Nummer doppelt: 1.1", r.stdout)
        self.assertIn("9.9", r.stdout)

    def test_version_passt_nicht_zum_verlauf_und_mockup(self):
        self.aendern(lambda s: s[0].update(version_mockup="1.1"))
        r = self.lauf("seitenliste_check.py")
        self.assertIn("Verlauf reicht bis 1.0", r.stdout)
        self.assertIn("Version 1.1 fehlt im Mockup", r.stdout)

    def test_erzeugtes_veraltet(self):
        self.aendern(lambda s: s[0].update(name="Anders"))
        self.assertIn("docs/seiten.md veraltet", self.lauf("seitenliste_check.py").stdout)

    def test_theme_veraltet_und_wiederhergestellt(self):
        (self.w / "mockups/theme-app.css").write_text("alt", encoding="utf8")
        r = self.lauf("seitenliste_check.py")
        self.assertIn("Theme veraltet", r.stdout)
        self.assertEqual((self.w / "mockups/theme-app.css").read_text(encoding="utf8"), "alt")

    def test_fingerabdruck_ist_nur_hinweis_und_abnahme_setzt_neu(self):
        with open(self.w / "src/app.js", "a", encoding="utf8") as fh:
            fh.write("// neu\n")
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("Code geändert ohne neue Version", r.stdout)
        self.lauf("seitenliste.py", "--abnahme", "alle")
        self.assertNotIn("Code geändert", self.lauf("seitenliste_check.py").stdout)

    def test_neue_seite_vor_dem_bau_ist_gruen(self):
        def f(s):
            s.append({"nr": "1.3", "name": "Neu", "art": "Seite", "version_mockup": "0.1", "version_code": None,
                      "schluessel": ["ansicht:neu"], "verlauf": [{"v": "0.1", "datum": "02.11.2026", "was": "Entwurf"}]})  # fmt: skip
        self.aendern(f)
        self.lauf("seitenliste.py")
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 0, r.stdout)

    def test_fix_mit_mockup_voraus_ist_gruen(self):
        def f(s):
            s[0]["version_code"] = "0.2"
            s[0]["verlauf"].append({"v": "0.2", "datum": "02.11.2026", "was": "Fix"})
        self.aendern(f)
        self.lauf("seitenliste.py")
        self.assertEqual(self.lauf("seitenliste_check.py").returncode, 0)

    def test_startseite_fehlt(self):
        self.cfg["start"] = "9.9"
        (self.w / "tools/seitenliste.config.json").write_text(json.dumps(self.cfg), encoding="utf8")
        self.lauf("seitenliste.py")
        self.assertIn("Startseite fehlt", self.lauf("seitenliste_check.py").stdout)

    def test_variante_zaehlt_als_hauptseite(self):
        self.aendern(lambda s: s[1].update(schluessel=["ansicht:detail#leer"]))
        self.lauf("seitenliste.py")
        self.assertEqual(self.lauf("seitenliste_check.py").returncode, 0)


class DatenlisteTest(SeitenlisteTest):
    """Dieselben Prüfungen mit Datenliste, dazu der Abgleich des Schemas."""

    def setUp(self):
        super().setUp()
        self.schema = {"version": 3, "tabellen": {"kunde": {"felder": [["id", "INTEGER", True]], "fk": []},
                                                  "auftrag": {"felder": [["id", "INTEGER", True]], "fk": ["kunde"]}}}  # fmt: skip
        self.cfg["daten"] = {
            "quelle": "mockups/daten.json", "doku": "docs/daten.md",
            "schema_befehl": [sys.executable, "tools/schema.py"],
            "gruppen": [{"bereich": "Kern", "seiten": ["1.1"], "tabellen": {"kunde": "Kunden", "auftrag": "Aufträge"}}],
            "orte": [{"bereich": "Browser", "art": "Schlüssel", "eintraege": {"ansicht": "Letzte Ansicht"}}],
        }  # fmt: skip
        (self.w / "tools/seitenliste.config.json").write_text(json.dumps(self.cfg), encoding="utf8")
        self.schema_schreiben()
        self.assertEqual(self.lauf("datenliste.py").returncode, 0)
        self.lauf("seitenliste.py")

    def schema_schreiben(self):
        (self.w / "tools/schema.py").write_text(f"print({json.dumps(json.dumps(self.schema))})", encoding="utf8")

    def test_gruen(self):
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 0, r.stdout + r.stderr)

    def test_nummern_und_verknuepfung(self):
        d = json.loads((self.w / "mockups/daten.json").read_text(encoding="utf8"))
        self.assertEqual([z["nr"] for z in d["gruppen"][0]["seiten_liste"]], ["D1.1", "D1.2"])
        self.assertEqual(d["gruppen"][0]["seiten_liste"][1]["zu"], ["D1.1"])
        self.assertEqual(d["gruppen"][1]["seiten_liste"][0]["nr"], "S1.1")
        self.assertIn('"nr":"D1.1"', (self.w / "mockups/index.html").read_text(encoding="utf8"))

    def test_neue_tabelle_ohne_eintrag_ist_rot(self):
        self.schema["tabellen"]["neu"] = {"felder": [], "fk": []}
        self.schema_schreiben()
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 1)
        self.assertIn("Tabelle ohne Eintrag: neu", r.stdout)
        self.assertEqual(self.lauf("datenliste.py").returncode, 1)

    def test_schema_aenderung_ohne_befehl_ist_rot(self):
        self.schema["tabellen"]["kunde"]["felder"].append(["name", "TEXT", False])
        self.schema_schreiben()
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 1)
        self.assertIn("daten.json veraltet", r.stdout)

    def test_unbekannte_seite(self):
        self.cfg["daten"]["gruppen"][0]["seiten"] = ["9.9"]
        (self.w / "tools/seitenliste.config.json").write_text(json.dumps(self.cfg), encoding="utf8")
        self.lauf("datenliste.py")
        self.lauf("seitenliste.py")
        self.assertIn("Seite gibt es nicht: 9.9", self.lauf("seitenliste_check.py").stdout)


if __name__ == "__main__":
    unittest.main()
