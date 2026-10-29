#!/usr/bin/env python3
"""Tests für sitzungen.py: python3 -m unittest skills/neustart/scripts/test_sitzungen.py"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import sitzungen  # noqa: E402


class OthersTest(unittest.TestCase):
    def test_eigene_und_tote_sitzungen_fallen_weg(self):
        with tempfile.TemporaryDirectory() as d:
            for pid, name, status in [(10, "ich", "busy"), (20, "tot", "busy"), (30, "andere", "idle"),
                                      (40, "arbeitet", "busy")]:
                with open(os.path.join(d, f"{pid}.json"), "w") as fh:
                    json.dump({"pid": pid, "name": name, "status": status, "cwd": "/x"}, fh)
            with open(os.path.join(d, "kaputt.json"), "w") as fh:
                fh.write("{")
            rows = sitzungen.others(d, own={10}, is_alive=lambda pid: pid != 20, count=lambda pid: 0)
        self.assertEqual([(r["name"], r["frei"]) for r in rows], [("andere", True), ("arbeitet", False)])

    def test_ruhende_sitzung_mit_laufendem_befehl_ist_belegt(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "30.json"), "w") as fh:
                json.dump({"pid": 30, "name": "hintergrund", "status": "idle"}, fh)
            rows = sitzungen.others(d, own=set(), is_alive=lambda pid: True, count=lambda pid: 1)
        self.assertFalse(rows[0]["frei"])

    def test_befehle_zaehlt_nur_shells_von_claude(self):
        cmds = {1: "/bin/bash -c source /h/.claude/shell-snapshots/snap.sh && make test", 2: "uvx ha-mcp@7.11.0"}
        self.assertEqual(sitzungen.befehle(0, kids=lambda pid: [1, 2], cmd=cmds.get), 1)


if __name__ == "__main__":
    unittest.main()
