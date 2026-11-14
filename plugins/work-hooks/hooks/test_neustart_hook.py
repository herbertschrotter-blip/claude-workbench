#!/usr/bin/env python3
"""Tests für neustart_hook.py: python3 -m unittest discover -s plugins/work-hooks/hooks -p 'test_*.py'"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import neustart_hook as h  # noqa: E402

LEBT = lambda pid: True  # noqa: E731


def schreibe(q, name, data):
    path = os.path.join(q, name)
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(data, fh)


class HookTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.q = self.tmp.name

    def tearDown(self):
        self.tmp.cleanup()

    def ruf(self, event, sid="b", now=lambda: 1000.0, **extra):
        return h.handle(dict({"hook_event_name": event, "session_id": sid}, **extra), self.q, LEBT, now)

    def test_ohne_warteschlange_still(self):
        self.assertEqual(h.handle({"hook_event_name": "Stop", "session_id": "b"}, os.path.join(self.q, "x"), LEBT),
                         (0, "", ""))

    def test_stop_haelt_einmal_je_wunsch_an(self):
        self.ruf("SessionStart")
        schreibe(self.q, "wuensche/a.json", {"sitzung": "a", "pid": 10, "name": "chat-1", "ordner": "/p",
                                             "ziel": "home-assistant", "grund": "Integration", "seit": 900.0})
        code, out, _ = self.ruf("Stop")
        self.assertEqual(code, 0)
        antwort = json.loads(out)
        self.assertEqual(antwort["decision"], "block")
        self.assertIn("chat-1", antwort["reason"])
        self.assertEqual(self.ruf("Stop"), (0, "", ""))
        self.assertEqual(self.ruf("Stop", stop_hook_active=True), (0, "", ""))

    def test_stop_ignoriert_eigenen_wunsch_und_laufende_sperre(self):
        self.ruf("SessionStart")
        schreibe(self.q, "wuensche/b.json", {"sitzung": "b", "pid": 20, "ziel": "home-assistant", "seit": 900.0})
        self.assertEqual(self.ruf("Stop"), (0, "", ""))
        schreibe(self.q, "wuensche/a.json", {"sitzung": "a", "pid": 10, "ziel": "home-assistant", "seit": 900.0})
        schreibe(self.q, "sperre.json", {"sitzung": "c", "pid": 30, "ziel": "home-assistant", "seit": 990.0})
        self.assertEqual(self.ruf("Stop"), (0, "", ""))

    def test_sperre_lehnt_ha_aufrufe_anderer_ab(self):
        schreibe(self.q, "sperre.json", {"sitzung": "a", "pid": 10, "name": "chat-1", "ziel": "home-assistant",
                                         "seit": 990.0})
        self.ruf("SessionStart")
        code, _, err = self.ruf("PreToolUse", tool_name="mcp__home-assistant__ha_search")
        self.assertEqual(code, 2)
        self.assertIn("startet gerade neu", err)
        self.assertEqual(self.ruf("PreToolUse", sid="a", tool_name="mcp__home-assistant__ha_restart")[0], 0)
        self.assertEqual(self.ruf("PreToolUse", tool_name="mcp__clickup__x")[0], 0)
        self.assertEqual(self.ruf("PreToolUse", now=lambda: 990.0 + h.SPERRE_MAX,
                                  tool_name="mcp__home-assistant__ha_search")[0], 0)

    def test_hinweis_nach_neustart_einmal(self):
        self.ruf("SessionStart")
        schreibe(self.q, "letzter.json", {"zeit": 1500.0, "sitzung": "a", "name": "chat-1", "ziel": "home-assistant",
                                          "erledigt": ["b"]})
        code, out, _ = self.ruf("PostToolUse", tool_name="AskUserQuestion")
        text = json.loads(out)["hookSpecificOutput"]["additionalContext"]
        self.assertIn("neu gestartet", text)
        self.assertIn("eigener Neustart-Wunsch", text)
        self.assertEqual(self.ruf("UserPromptSubmit"), (0, "", ""))

    def test_neue_sitzung_bekommt_alten_neustart_nicht(self):
        schreibe(self.q, "letzter.json", {"zeit": 1500.0, "sitzung": "a", "name": "chat-1"})
        self.ruf("SessionStart")
        self.assertEqual(self.ruf("UserPromptSubmit"), (0, "", ""))

    def test_eigener_neustart_ohne_hinweis(self):
        self.ruf("SessionStart")
        schreibe(self.q, "letzter.json", {"zeit": 1500.0, "sitzung": "b", "name": "ich"})
        self.assertEqual(self.ruf("UserPromptSubmit"), (0, "", ""))


if __name__ == "__main__":
    unittest.main()
