"""Tests für versionen.py: python3 -m unittest discover -s skills/projekt-anlegen/scripts/tests"""

import io
import json
import sys
import unittest
import urllib.error
from pathlib import Path
from unittest import mock

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))
import versionen as v  # noqa: E402

PYPI = {"ruff": "0.17.0", "pytest": "9.1.1", "homeassistant": "2026.10.1"}


class VergleichTest(unittest.TestCase):
    def test_neuer_aktuell_und_nicht_pruefbar(self):
        zeilen = v.vergleichen({"ruff": "0.16.10", "pytest": "9.1.1", "mypy": "2.4.0"}, PYPI.get)
        stand = {z["paket"]: z["stand"] for z in zeilen}
        self.assertEqual(stand, {"ruff": "neuer", "pytest": "aktuell", "mypy": "nicht prüfbar"})

    def test_zahlen_statt_text_vergleichen(self):
        # 0.16.10 ist neuer als 0.16.9 – als Text wäre es umgekehrt
        self.assertEqual(v.vergleichen({"ruff": "0.16.10"}, {"ruff": "0.16.9"}.get)[0]["stand"], "aktuell")

    def test_vorabversion_gegen_aelteren_stand(self):
        # 1.2.0rc1 ist neuer als 1.1.9: kein „neuer“, nur weil sich der Text unterscheidet
        self.assertEqual(v.vergleichen({"x": "1.2.0rc1"}, {"x": "1.1.9"}.get)[0]["stand"], "aktuell")
        self.assertEqual(v.vergleichen({"x": "1.2.0rc1"}, {"x": "1.2.0"}.get)[0]["stand"], "neuer")

    def test_calver_mit_beta(self):
        self.assertEqual(v.vergleichen({"x": "2026.10.0b3"}, {"x": "2026.10.0"}.get)[0]["stand"], "neuer")
        self.assertEqual(v.vergleichen({"x": "2026.10.0"}, {"x": "2026.10.0b3"}.get)[0]["stand"], "aktuell")

    def test_nicht_lesbar_ist_unklar(self):
        self.assertEqual(v.vergleichen({"x": "1.0-foo"}, {"x": "1.1"}.get)[0]["stand"], "unklar")
        self.assertEqual(v.vergleichen({"x": "1.0"}, {"x": "xyz"}.get)[0]["stand"], "unklar")

    def test_endnullen_lokal_und_epoche(self):
        self.assertEqual(v.vergleichen({"x": "1.0"}, {"x": "1.0.0"}.get)[0]["stand"], "aktuell")
        self.assertEqual(v.vergleichen({"x": "1.0+local"}, {"x": "1.0"}.get)[0]["stand"], "aktuell")
        self.assertEqual(v.vergleichen({"x": "1!1.0"}, {"x": "2.0"}.get)[0]["stand"], "aktuell")

    def test_reihenfolge_der_vorstufen(self):
        reihe = ["1.0.dev1", "1.0a1.dev1", "1.0a1", "1.0b2", "1.0rc1", "1.0", "1.0.post1.dev1", "1.0.post1", "1.0-2",
                 "1.1.dev0"]
        self.assertEqual(sorted(reihe, key=v.schluessel), reihe)

    def test_gekoppelte_pakete_im_hinweis(self):
        text = v.tabelle(v.vergleichen({"homeassistant": "2026.9.4"}, PYPI.get))
        self.assertIn("nur zusammen mit pytest-homeassistant-custom-component", text)

    def test_ohne_netz_kein_fehler(self):
        with mock.patch.object(v.urllib.request, "urlopen", side_effect=urllib.error.URLError("offline")):
            self.assertIsNone(v.neueste("ruff"))

    def test_antwort_von_pypi(self):
        antwort = io.BytesIO(json.dumps({"info": {"version": "1.2.3"}}).encode())
        with mock.patch.object(v.urllib.request, "urlopen", return_value=antwort):
            self.assertEqual(v.neueste("ruff"), "1.2.3")


if __name__ == "__main__":
    unittest.main()
