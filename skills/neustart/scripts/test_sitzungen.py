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

    def test_wartende_sitzung_ist_frei(self):
        with tempfile.TemporaryDirectory() as d:
            with open(os.path.join(d, "30.json"), "w") as fh:
                json.dump({"pid": 30, "name": "frage", "status": "waiting"}, fh)
            rows = sitzungen.others(d, own=set(), is_alive=lambda pid: True, count=lambda pid: 0)
        self.assertTrue(rows[0]["frei"])

    def test_warten_dieses_skripts_zaehlt_nicht(self):
        cmds = {1: "/bin/bash -c source /h/.claude/shell-snapshots/s.sh && python3 x/sitzungen.py --warten 900"}
        self.assertEqual(sitzungen.befehle(0, kids=lambda pid: [1], cmd=cmds.get), 0)


class WarteschlangeTest(unittest.TestCase):
    A = {"sessionId": "a", "pid": 10, "name": "chat-1", "cwd": "/p1"}
    B = {"sessionId": "b", "pid": 20, "name": "chat-2", "cwd": "/p2"}

    def test_beide_wollen_neu_starten_einer_erledigt_beide(self):
        with tempfile.TemporaryDirectory() as q:
            uhr = [100.0]
            now = lambda: uhr[0]  # noqa: E731
            sitzungen.eintragen(self.A, "home-assistant", "neue Integration", q, now)
            uhr[0] = 101.0
            sitzungen.eintragen(self.B, "home-assistant", "Karte", q, now)
            uhr[0] = 105.0
            ok_b, _ = sitzungen.sperre_nehmen(self.B, "home-assistant", q, lambda pid: True, now)
            ok_a, wer = sitzungen.sperre_nehmen(self.A, "home-assistant", q, lambda pid: True, now)
            self.assertTrue(ok_b)
            self.assertFalse(ok_a)
            self.assertEqual(wer["name"], "chat-2")
            uhr[0] = 200.0
            letzter = sitzungen.fertig(self.B, q, lambda pid: True, now)
            self.assertEqual(sorted(letzter["erledigt"]), ["a", "b"])
            self.assertEqual(sitzungen.wuensche(q, lambda pid: True), [])
            self.assertIsNotNone(sitzungen.erledigt_fuer("a", 100.0, q))
            self.assertIsNone(sitzungen.sperre_lesen(q, lambda pid: True, lambda: 200.0))

    def test_wunsch_nach_beginn_bleibt_offen(self):
        with tempfile.TemporaryDirectory() as q:
            sitzungen.sperre_nehmen(self.B, "home-assistant", q, lambda pid: True, lambda: 100.0)
            sitzungen.eintragen(self.A, "home-assistant", "spaet", q, lambda: 150.0)
            letzter = sitzungen.fertig(self.B, q, lambda pid: True, lambda: 200.0)
            self.assertEqual(letzter["erledigt"], [])
            self.assertEqual([w["sitzung"] for w in sitzungen.wuensche(q, lambda pid: True)], ["a"])
            self.assertIsNone(sitzungen.erledigt_fuer("a", 150.0, q))

    def test_liegen_gebliebene_sperre_wird_ersetzt(self):
        with tempfile.TemporaryDirectory() as q:
            sitzungen.sperre_nehmen(self.B, "home-assistant", q, lambda pid: True, lambda: 100.0)
            ok, s = sitzungen.sperre_nehmen(self.A, "home-assistant", q, lambda pid: pid != 20, lambda: 110.0)
            self.assertTrue(ok)
            self.assertEqual(s["sitzung"], "a")
            ok, _ = sitzungen.sperre_nehmen(self.B, "home-assistant", q, lambda pid: True,
                                            lambda: 110.0 + sitzungen.SPERRE_MAX)
            self.assertTrue(ok)

    def test_wuensche_beendeter_sitzungen_fallen_weg(self):
        with tempfile.TemporaryDirectory() as q:
            sitzungen.eintragen(self.A, "home-assistant", "", q, lambda: 1.0)
            self.assertEqual(sitzungen.wuensche(q, lambda pid: False), [])
            self.assertFalse(os.listdir(os.path.join(q, "wuensche")))


if __name__ == "__main__":
    unittest.main()
