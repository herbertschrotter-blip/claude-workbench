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
            rows = sitzungen.others(d, own={10}, is_alive=lambda pid: pid != 20)
        self.assertEqual([(r["name"], r["status"]) for r in rows], [("andere", "idle"), ("arbeitet", "busy")])


if __name__ == "__main__":
    unittest.main()
