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
