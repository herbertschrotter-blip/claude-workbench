"""Tests für checks.py: python3 -m unittest discover -s skills/git-commit-helper/scripts/tests"""

import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import checks as c

PY = sys.executable.replace("\\", "/")
PROFIL = f"""# Demo

## Skill-Profil

- Profil-Version: 1

### Checks
- logik: {PY} -c "print('logik')" [src/**; pyproject.toml]
- doku: {PY} -c "print('doku; ok')" [docs/**]
- immer: {PY} -c "print('immer')"
- rot: {PY} -c "import sys; print('kaputt'); sys.exit(3)" [src/**]
- langsam-a: {PY} -c "import time; time.sleep(1)" [src/**]
- langsam-b: {PY} -c "import time; time.sleep(1)" [src/**]
- schwer: {PY} -c "print('allein')" (allein) [src/**]
- kette: cd src && {PY} -c "import os; print(os.path.basename(os.getcwd()))"; {PY} -c "print('zwei')" [src/**]
- fehlt: befehl-den-es-nicht-gibt-xyz [src/**]
- stand: {PY} -c "print('stand')" (allein) [auswahl: src/**] [eingaben: src/**; tests/**; pyproject.toml]
- nur-eingaben: {PY} -c "print('[x]')" [eingaben: tests/**]

### Commit
- Pre-Commit-Checks: logik; doku; immer

## Danach

### Checks
- fremd: nicht aus dem Profil [**]
"""


def git(wurzel, *args):
    subprocess.run(["git", *args], cwd=wurzel, check=True, capture_output=True)


class ProfilTest(unittest.TestCase):
    def test_checks_und_vor_commit(self):
        p = c.profil_lesen(PROFIL)
        self.assertEqual(p["vor_commit"], ["logik", "doku", "immer"])
        self.assertEqual(p["checks"]["logik"]["muster"], ["src/**", "pyproject.toml"])
        self.assertEqual(p["checks"]["immer"]["muster"], [])
        self.assertTrue(p["checks"]["schwer"]["allein"])
        self.assertNotIn("fremd", p["checks"])
        self.assertEqual(len(p["checks"]["kette"]["befehle"]), 2)
        self.assertEqual(len(p["checks"]["doku"]["befehle"]), 1)  # Semikolon in Anführungszeichen
        self.assertEqual(p["checks"]["logik"]["eingaben"], [])  # alte Zeile: Klammer ohne Schlüssel = Auswahl

    def test_auswahl_und_eingaben(self):
        p = c.profil_lesen(PROFIL)["checks"]
        self.assertEqual(p["stand"]["muster"], ["src/**"])
        self.assertEqual(p["stand"]["eingaben"], ["src/**", "tests/**", "pyproject.toml"])
        self.assertTrue(p["stand"]["allein"])
        self.assertEqual(p["nur-eingaben"]["muster"], [])
        self.assertEqual(p["nur-eingaben"]["befehle"], [f"{PY} -c \"print('[x]')\""])  # Klammer im Befehl bleibt

    def test_fehlerhafte_angaben_abgelehnt(self):
        for zeile in ["- x: echo a [quelle: src/**]",          # unbekannter Schlüssel
                      "- x: echo a [auswahl: src/**] [auswahl: b/**]",  # doppelt
                      "- x: echo a [src/**] [auswahl: b/**]",  # alte Klammer und auswahl zugleich
                      "- x: echo a []",                         # leer
                      "- x: echo a [eingaben: ]",               # leer mit Schlüssel
                      "- x: echo a src/**]",                    # ohne öffnende Klammer
                      "- x: echo 'a [src/**]",                  # Anführungszeichen offen
                      "- x: [src/**]",                          # kein Befehl
                      "- x: echo a [auswahl: s/**] b",          # Angabe nicht am Ende
                      "- x: echo ok && [ -f x ]",               # Shell-Klammer statt Muster
                      "- x: echo a [src/** tests/**]"]:         # Leerzeichen im Muster
            with self.subTest(zeile=zeile), self.assertRaises(c.ProfilFehler):
                c.profil_lesen(f"## Skill-Profil\n\n### Checks\n{zeile}\n")

    def test_ohne_profil(self):
        with self.assertRaises(c.ProfilFehler):
            c.profil_lesen("# nur Text\n")

    def test_muster(self):
        dateien = {"src/a.py", "src/x/b.py", "README.md", "a.py", "docs/n.md"}
        self.assertEqual(c.passende(dateien, ["src/**"]), ["src/a.py", "src/x/b.py"])
        self.assertEqual(c.passende(dateien, ["**/*.py"]), ["a.py", "src/a.py", "src/x/b.py"])
        self.assertEqual(c.passende(dateien, ["*.md"]), ["README.md"])
        self.assertEqual(c.passende(dateien, []), sorted(dateien))


class LaufTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.wurzel = self.tmp.name
        git(self.wurzel, "init", "-q")
        (Path(self.wurzel) / "src").mkdir()
        (Path(self.wurzel) / "src" / "a.py").write_text("x = 1\n", encoding="utf-8")
        self.profil = c.profil_lesen(PROFIL)

    def lauf(self, namen, **kw):
        return {e["name"]: e for e in c.laufen(self.wurzel, self.profil, namen, c.geaendert(self.wurzel), **kw)}

    def test_nur_passende_und_ohne_muster_immer(self):
        r = self.lauf(["logik", "doku", "immer"])
        self.assertEqual(r["logik"]["ergebnis"], "grün")
        self.assertEqual(r["doku"]["ergebnis"], "übersprungen")
        self.assertEqual(r["immer"]["ergebnis"], "grün")

    def test_schon_gruen_bis_zur_aenderung(self):
        self.lauf(["logik"])
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "schon grün")
        self.assertEqual(self.lauf(["logik"], immer=True)["logik"]["ergebnis"], "grün")
        (Path(self.wurzel) / "src" / "a.py").write_text("x = 2\n", encoding="utf-8")
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "grün")

    def test_rot_mit_ausgabe_und_ohne_merker(self):
        r = self.lauf(["rot"])["rot"]
        self.assertEqual((r["ergebnis"], r["exit"]), ("rot", 3))
        self.assertIn("kaputt", r["ausgabe"])
        self.assertEqual(self.lauf(["rot"])["rot"]["ergebnis"], "rot")  # rot wird nie gemerkt

    def test_parallel(self):
        start = time.monotonic()
        r = self.lauf(["langsam-a", "langsam-b"])
        self.assertLess(time.monotonic() - start, 1.9)
        self.assertEqual({e["ergebnis"] for e in r.values()}, {"grün"})

    def test_allein_und_kette(self):
        r = self.lauf(["schwer", "kette"])
        self.assertEqual(r["schwer"]["ergebnis"], "grün")
        log = Path(r["kette"]["log"]).read_text(encoding="utf-8")
        self.assertEqual(log.split(), ["src", "zwei"])

    @unittest.skipIf(os.name == "nt", "Exit 127 der POSIX-Shell")
    def test_befehl_fehlt(self):
        r = self.lauf(["fehlt", "logik"])
        self.assertEqual(r["fehlt"]["ergebnis"], "fehlt")
        self.assertEqual(c.exit_code(list(r.values())), 2)

    def test_fehlertext_allein_ist_kein_fehlender_befehl(self):
        check = {"befehle": [f"{PY} -c \"print('x is not recognized as y'); raise SystemExit(1)\""], "muster": [],
                 "allein": False}
        r = c.ausfuehren("t", check, self.wurzel, self.wurzel)
        self.assertEqual(r["ergebnis"], "rot")

    def test_zeitlimit_wird_genannt(self):
        check = {"befehle": [f"{PY} -c \"print('vorher', flush=True); import time; time.sleep(5)\""], "muster": [],
                 "allein": False}
        alt, c.TIMEOUT = c.TIMEOUT, 1
        try:
            r = c.ausfuehren("t", check, self.wurzel, self.wurzel)
        finally:
            c.TIMEOUT = alt
        self.assertEqual(r["ergebnis"], "rot")
        self.assertTrue(r["ausgabe"].startswith("Zeitlimit 1 s überschritten"), r["ausgabe"])

    def test_unbekannter_check_ist_fehler(self):
        r = c.laufen(self.wurzel, self.profil, ["gibtsnicht"], set())
        self.assertEqual(r[0]["ergebnis"], "unbekannt")
        self.assertEqual(c.exit_code(r), 1)

    def test_merker_liegt_in_git(self):
        self.lauf(["logik"])
        merker = Path(self.wurzel) / ".git" / c.MERKER
        daten = json.loads(merker.read_text(encoding="utf-8"))
        self.assertEqual(daten["schema"], c.SCHEMA)
        self.assertIn("logik", daten["checks"])
        self.assertNotIn(c.MERKER, " ".join(c.geaendert(self.wurzel)))
        self.assertNotIn(c.ARTEFAKTE, " ".join(c.geaendert(self.wurzel)))

    def test_alter_merker_zaehlt_nicht(self):
        abdruck = c.fingerabdruck(self.wurzel, self.profil["checks"]["logik"], ["src/a.py"])
        (Path(self.wurzel) / ".git" / c.MERKER).write_text(json.dumps({"logik": abdruck}), encoding="utf-8")
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "grün")

    def eingaben_repo(self):
        """Stand nach einem Commit: tests/ und pyproject.toml unverändert, nur src/a.py geändert."""
        (Path(self.wurzel) / "tests").mkdir()
        (Path(self.wurzel) / "tests" / "test_a.py").write_text("assert True\n", encoding="utf-8")
        (Path(self.wurzel) / "pyproject.toml").write_text("[tool]\n", encoding="utf-8")
        git(self.wurzel, "add", "-A")
        git(self.wurzel, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "start")
        (Path(self.wurzel) / "src" / "a.py").write_text("x = 3\n", encoding="utf-8")

    def test_unveraenderte_eingabe_entwertet_gruen(self):
        self.eingaben_repo()
        self.assertEqual(self.lauf(["stand"])["stand"]["ergebnis"], "grün")
        self.assertEqual(self.lauf(["stand"])["stand"]["ergebnis"], "schon grün")
        # Test geändert und eingecheckt: nicht mehr in git status, aber Eingabe – der alte Grün-Vermerk gilt nicht
        (Path(self.wurzel) / "tests" / "test_a.py").write_text("assert 1\n", encoding="utf-8")
        git(self.wurzel, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "test", "tests/test_a.py")
        self.assertEqual(self.lauf(["stand"])["stand"]["ergebnis"], "grün")

    def test_hinzufuegen_und_loeschen_aendert_abdruck(self):
        self.eingaben_repo()
        check = self.profil["checks"]["stand"]
        vorher = c.eingaben_stand(self.wurzel, check)["digest"]
        neu = Path(self.wurzel) / "tests" / "conftest.py"
        neu.write_text("\n", encoding="utf-8")
        mit = c.eingaben_stand(self.wurzel, check)["digest"]
        neu.unlink()
        (Path(self.wurzel) / "pyproject.toml").unlink()
        ohne = c.eingaben_stand(self.wurzel, check)["digest"]
        self.assertEqual(len({vorher, mit, ohne}), 3)

    def test_nur_eingaben_loest_aus(self):
        self.eingaben_repo()
        self.assertEqual(self.lauf(["nur-eingaben"])["nur-eingaben"]["ergebnis"], "übersprungen")
        (Path(self.wurzel) / "tests" / "test_a.py").write_text("assert 2\n", encoding="utf-8")
        self.assertEqual(self.lauf(["nur-eingaben"])["nur-eingaben"]["ergebnis"], "grün")

    def test_datensatz(self):
        self.eingaben_repo()
        self.lauf(["stand", "logik"])
        daten = json.loads((Path(self.wurzel) / ".git" / c.MERKER).read_text(encoding="utf-8"))["checks"]
        d = daten["stand"]
        for feld in ("schema", "check", "definition_digest", "inputs", "environment", "started_at", "finished_at",
                     "exit_code", "result_artifact", "input_stable"):
            self.assertIn(feld, d)
        self.assertEqual(d["inputs"]["patterns"], ["src/**", "tests/**", "pyproject.toml"])
        self.assertEqual([f["path"] for f in d["inputs"]["files"]], ["pyproject.toml", "src/a.py", "tests/test_a.py"])
        self.assertTrue(d["input_stable"])
        self.assertEqual(d["exit_code"], 0)
        self.assertEqual(d["definition_digest"], c.definition_digest(self.profil["checks"]["stand"]))
        artefakt = Path(self.wurzel) / d["result_artifact"]["path"]
        self.assertEqual(c.datei_hash(artefakt), d["result_artifact"]["sha256"])
        self.assertIn("stand", artefakt.read_text(encoding="utf-8"))
        self.assertEqual(daten["logik"]["inputs"]["patterns"], [])  # ohne Eingabemuster kein Gesamtstand
        self.assertIsNone(daten["logik"]["inputs"]["digest"])

    def test_allein_ohne_leerzeichen_gehoert_zum_befehl(self):
        p = c.profil_lesen("## Skill-Profil\n\n### Checks\n- x: echo foo(allein) [src/**]\n")["checks"]["x"]
        self.assertFalse(p["allein"])

    def test_instabiler_lauf_traegt_kein_schon_gruen(self):
        self.eingaben_repo()
        self.lauf(["stand"])
        datei = Path(self.wurzel) / ".git" / c.MERKER
        daten = json.loads(datei.read_text(encoding="utf-8"))
        daten["checks"]["stand"]["input_stable"] = False
        datei.write_text(json.dumps(daten), encoding="utf-8")
        self.assertEqual(self.lauf(["stand"])["stand"]["ergebnis"], "grün")

    def test_fehlendes_artefakt_traegt_kein_schon_gruen(self):
        self.eingaben_repo()
        self.lauf(["stand"])
        (Path(self.wurzel) / ".git" / c.ARTEFAKTE / "stand.log").write_text("anders", encoding="utf-8")
        self.assertEqual(self.lauf(["stand"])["stand"]["ergebnis"], "grün")

    def test_branchwechsel_entwertet_ohne_eingaben(self):
        self.eingaben_repo()
        self.lauf(["logik"])
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "schon grün")
        (Path(self.wurzel) / "README.md").write_text("neu\n", encoding="utf-8")
        git(self.wurzel, "add", "README.md")
        git(self.wurzel, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qm", "anderer Stand")
        self.assertEqual(self.lauf(["logik"])["logik"]["ergebnis"], "grün")

    def test_datei_weg_beim_hashen(self):
        self.assertIsNone(c.datei_hash(Path(self.wurzel) / "gibtsnicht"))

    def test_rot_loescht_datensatz(self):
        self.lauf(["rot"])
        daten = json.loads((Path(self.wurzel) / ".git" / c.MERKER).read_text(encoding="utf-8"))
        self.assertNotIn("rot", daten["checks"])

    def test_genannt_und_immer_laeuft_ohne_aenderung(self):
        self.eingaben_repo()
        git(self.wurzel, "-c", "user.name=t", "-c", "user.email=t@t", "commit", "-qam", "sauber")
        profil = Path(self.tmp.name).parent / f"{Path(self.tmp.name).name}-profil.md"
        profil.write_text(PROFIL, encoding="utf-8")
        self.addCleanup(profil.unlink)
        alt = os.getcwd()
        os.chdir(self.wurzel)
        self.addCleanup(os.chdir, alt)

        def haupt(*args):
            puffer = StringIO()
            with redirect_stdout(puffer):
                c.main([*args, "--profil", str(profil), "--json"])
            return {e["name"]: e for e in json.loads(puffer.getvalue())["checks"]}

        self.assertEqual(haupt("--checks", "stand")["stand"]["ergebnis"], "übersprungen")
        self.assertEqual(haupt("--vor-commit", "--immer")["logik"]["ergebnis"], "übersprungen")
        self.assertEqual(haupt("--checks", "stand", "--immer")["stand"]["ergebnis"], "grün")
        d = json.loads((Path(self.wurzel) / ".git" / c.MERKER).read_text(encoding="utf-8"))["checks"]["stand"]
        self.assertEqual([f["path"] for f in d["inputs"]["files"]], ["pyproject.toml", "src/a.py", "tests/test_a.py"])
        self.assertTrue(d["input_stable"])

    def test_tabelle(self):
        r = c.laufen(self.wurzel, self.profil, ["logik", "doku"], c.geaendert(self.wurzel))
        text = c.tabelle(r)
        self.assertIn("| logik | 0:00 | grün |", text)
        self.assertIn("| doku | – | übersprungen – keine passende Datei |", text)


if __name__ == "__main__":
    unittest.main()
