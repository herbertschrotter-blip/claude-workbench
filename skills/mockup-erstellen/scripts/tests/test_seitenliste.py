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


class AktualisierenTest(SeitenlisteTest):
    """Dieselben Prüfungen in einem Git-Repo, dazu der Lauf „aktualisiere Seitenliste“."""

    def setUp(self):
        super().setUp()
        shutil.copy(ASSETS / "themeabgleich.py", self.w / "tools")
        self.git("init", "-q")
        self.git("config", "user.email", "t@t")
        self.git("config", "user.name", "t")
        self.commit("start")
        self.lauf("seitenliste.py", "--start")
        self.commit("[v1] Doku, Docs: Seitenliste aktualisiert")

    def git(self, *args):
        subprocess.run(["git", *args], cwd=self.w, capture_output=True, check=True)

    def commit(self, titel):
        self.git("add", "-A")
        self.git("commit", "-q", "--allow-empty", "-m", titel)

    def offen(self):
        r = self.lauf("seitenliste.py", "--offen")
        self.assertEqual(r.returncode, 0, r.stderr)
        return json.loads(r.stdout)

    def eintragen(self, liste):
        d = self.w / "eintraege.json"
        d.write_text(json.dumps(liste), encoding="utf8")
        r = self.lauf("seitenliste.py", "--eintragen", str(d))
        self.assertEqual(r.returncode, 0, r.stderr)
        d.unlink()

    def test_start_setzt_stand_und_abnahme(self):
        s = self.daten()[0]["seiten"]
        self.assertTrue(s[0]["stand_commit"])
        self.assertEqual(s[0]["version_abgenommen"], "1.0")
        self.assertEqual(self.offen()["seiten"], [])

    def test_offen_zeigt_commits_und_gemeinsame_dateien(self):
        with open(self.w / "src/app.js", "a", encoding="utf8") as fh:
            fh.write("// a\n")
        self.commit("erste Änderung")
        with open(self.w / "src/app.js", "a", encoding="utf8") as fh:
            fh.write("// b\n")
        self.commit("zweite Änderung")
        o = self.offen()
        self.assertEqual([x["nr"] for x in o["seiten"]], ["1.1", "1.2"])
        self.assertEqual([c["titel"] for c in o["seiten"][0]["code"]], ["erste Änderung", "zweite Änderung"])
        self.assertEqual(o["seiten"][0]["gemeinsam"], ["app.js"])

    def test_nicht_committete_aenderung_wird_genannt(self):
        with open(self.w / "src/app.js", "a", encoding="utf8") as fh:
            fh.write("// a\n")
        self.assertTrue(self.offen()["nicht_committet"])

    def test_version_fuer_version(self):
        with open(self.w / "src/app.js", "a", encoding="utf8") as fh:
            fh.write("// a\n")
        self.commit("Änderung")
        self.eintragen([
            {"nr": "1.1", "art": "code", "was": "Knopf ergänzt", "commit": "abc", "datum": "01.11.2026"},
            {"nr": "1.1", "art": "code", "was": "Text korrigiert", "ticket": "FE-1"},
        ])  # fmt: skip
        s = self.daten()[0]["seiten"]
        self.assertEqual(s[0]["version_code"], "0.3")
        self.assertEqual(s[0]["version_mockup"], "1.0")
        self.assertEqual(s[0]["verlauf"][-2]["commit"], "abc")
        self.assertEqual(s[0]["verlauf"][-1]["ticket"], "FE-1")
        self.assertEqual(s[1]["version_code"], "0.1")
        self.assertEqual(self.lauf("seitenliste_check.py").returncode, 0)
        self.commit("[v1] Doku, Docs: Seitenliste aktualisiert")
        self.assertEqual(self.offen()["seiten"], [])

    def test_0_9_wird_0_10_und_nie_1_0(self):
        self.aendern(lambda s: s[1].update(version_code="0.9"))
        self.eintragen([{"nr": "1.2", "art": "code", "was": "Fix"}])
        self.assertEqual(self.daten()[0]["seiten"][1]["version_code"], "0.10")

    def test_mockup_aenderung_gilt_nicht_als_abgenommen(self):
        self.eintragen([{"nr": "1.1", "art": "mockup", "was": "Entwurf"}])
        s = self.daten()[0]["seiten"][0]
        self.assertEqual((s["version_mockup"], s["version_abgenommen"]), ("1.1", "1.0"))
        self.assertIn("version: '1.1'", (self.w / "mockups/seiten/start.html").read_text(encoding="utf8"))
        self.assertEqual(self.lauf("seitenliste_check.py").returncode, 0)
        self.lauf("seitenliste.py", "--abgenommen", "1.1")
        self.assertEqual(self.daten()[0]["seiten"][0]["version_abgenommen"], "1.1")

    def test_gebaut_zieht_code_auf_die_abnahme(self):
        self.eintragen([{"nr": "1.1", "art": "code", "was": "gebaut", "gebaut": True}])
        self.assertEqual(self.daten()[0]["seiten"][0]["version_code"], "1.0")

    def test_gebaut_geht_nie_zurueck(self):
        self.aendern(lambda s: s[0].update(version_code="1.3"))
        self.eintragen([{"nr": "1.1", "art": "code", "was": "gebaut", "gebaut": True}])
        self.assertEqual(self.daten()[0]["seiten"][0]["version_code"], "1.3")

    def test_abgenommen_ueber_mockup_ist_rot(self):
        self.aendern(lambda s: s[0].update(version_abgenommen="2.0"))
        self.lauf("seitenliste.py")
        self.assertIn("abgenommen 2.0", self.lauf("seitenliste_check.py").stdout)

    def themecfg(self):
        self.cfg.pop("theme")
        self.cfg["themeabgleich"] = {"ziel": "mockups/theme-hinweise.json", "token": ["mockups/theme-app.css"],
                                     "eigenschaften": ["padding"], "ausnahmen": ["0"]}  # fmt: skip
        (self.w / "tools/seitenliste.config.json").write_text(json.dumps(self.cfg), encoding="utf8")
        (self.w / "mockups/theme-app.css").write_text(":root { --akzent:#1a73e8; --luft:8px; }", encoding="utf8")

    def test_theme_treffer_mit_und_ohne_token(self):
        self.themecfg()
        (self.w / "src/app.js").write_text(
            "const ANSICHT = { start: a, detail: b }\n"
            "// color:#1a73e8; background:#123456; padding:8px; padding:14px; padding:0\n"
            "// color:var(--akzent)\n--eigen:#ffffff;\nhref=\"#abc\"\n", encoding="utf8")  # fmt: skip
        r = self.lauf("themeabgleich.py")
        self.assertEqual(r.returncode, 0, r.stderr)
        t = json.loads(r.stdout)["1.1"]
        self.assertEqual([(x["wert"], x["token"]) for x in t], [
            ("#1a73e8", "akzent"), ("#123456", None), ("padding: 8px", "luft"), ("padding: 14px", None)])  # fmt: skip
        self.assertEqual(t[0]["zeile"], 2)

    def test_theme_hinweise_in_der_seite_und_nur_hinweis(self):
        self.themecfg()
        d = self.w / "bewertet.json"
        d.write_text(json.dumps({"1.1": [{"datei": "src/app.js", "zeile": 2, "wert": "#123456", "token": None}]}), encoding="utf8")
        self.assertEqual(self.lauf("themeabgleich.py", "--uebernehmen", str(d)).returncode, 0)
        self.lauf("seitenliste.py")
        html = (self.w / "mockups/index.html").read_text(encoding="utf8")
        self.assertIn('"wert":"#123456"', html)
        self.assertNotIn("@@", html)
        r = self.lauf("seitenliste_check.py")
        self.assertEqual(r.returncode, 0, r.stdout)
        self.assertIn("Theme-Abgleich: 1 feste Werte auf 1 Seiten", r.stdout)


class VorlageTest(SeitenlisteTest):
    """Rote Markierung, Gesamtübersicht und Dev-Schalter."""

    def ungleich(self, m, c):
        text = (ASSETS / "seitenliste_vorlage.html").read_text(encoding="utf8")
        zeilen = [z for z in text.splitlines() if z.startswith(("const ver=", "const ungleich="))]
        code = "\n".join(zeilen) + f"\nconsole.log(ungleich({json.dumps({'version_mockup': m, 'version_code': c})}))"
        return subprocess.run(["node", "-e", code], capture_output=True, text=True, check=True).stdout.strip() == "true"

    @unittest.skipUnless(shutil.which("node"), "node fehlt")
    def test_ungleich(self):
        self.assertTrue(self.ungleich("1.0", "0.1"))
        self.assertTrue(self.ungleich("0.10", "0.1"))  # als Kommazahl wären sie gleich
        self.assertFalse(self.ungleich("1.2", "1.2"))
        self.assertFalse(self.ungleich(None, "0.1"))
        self.assertFalse(self.ungleich("0.1", None))

    def test_gesamt_und_fenster_in_der_seite(self):
        t = (self.w / "mockups/index.html").read_text(encoding="utf8")
        for teil in ('data-gesamt="1"', 'id="gesamt"', "rot: M und C ungleich", "#fenster[hidden]", "--rot-g"):
            self.assertIn(teil, t)
        self.assertNotIn("@@", t)

    def test_mockup_zeigt_nummer_und_version(self):
        self.assertIn('<div class="vnr">${opt.nr} v${opt.version}</div>', (ASSETS / "theme.js").read_text(encoding="utf8"))

    def devcfg(self, ziel="src/seitenversionen.js"):
        self.cfg["dev_versionen"] = ziel
        (self.w / "tools/seitenliste.config.json").write_text(json.dumps(self.cfg), encoding="utf8")
        self.assertEqual(self.lauf("seitenliste.py").returncode, 0)

    def test_dev_versionen_js(self):
        self.devcfg()
        t = (self.w / "src/seitenversionen.js").read_text(encoding="utf8")
        self.assertIn("export const SEITEN", t)
        self.assertIn('"ansicht:detail"', t)
        self.assertEqual(self.lauf("seitenliste_check.py").returncode, 0)

    def test_dev_versionen_json_ohne_entwurf(self):
        g = self.daten()
        g[0]["seiten"].append({"nr": "1.3", "name": "Neu", "art": "Blatt", "schluessel": ["blatt:neu"], "version_mockup": "0.1"})
        (self.w / "mockups/seiten.json").write_text(json.dumps(g), encoding="utf8")
        self.devcfg("mockups/dev.json")
        d = json.loads((self.w / "mockups/dev.json").read_text(encoding="utf8"))
        self.assertEqual(d["ansicht:detail"], {"nr": "1.2", "v": "0.1"})
        self.assertNotIn("blatt:neu", d)

    def test_dev_versionen_veraltet_ist_rot(self):
        self.devcfg()
        (self.w / "src/seitenversionen.js").write_text("alt", encoding="utf8")
        lauf = self.lauf("seitenliste_check.py")
        self.assertEqual(lauf.returncode, 1)
        self.assertIn("seitenversionen.js veraltet", lauf.stdout)


if __name__ == "__main__":
    unittest.main()
