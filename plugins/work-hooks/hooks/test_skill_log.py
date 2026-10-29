#!/usr/bin/env python3
"""Tests für skill_log.py (nur Standardbibliothek): python3 -m unittest plugins/work-hooks/hooks/test_skill_log.py"""

import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_log  # noqa: E402


class PluginInfoTest(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        base = self.tmp.name
        self.config = os.path.join(base, "config")
        self.work = os.path.join(base, "cache", "workbench", "work", "abc123")
        self.script = os.path.join(self.work, "plugins", "work-hooks", "hooks", "skill_log.py")
        os.makedirs(os.path.dirname(self.script))
        open(self.script, "w").close()
        os.makedirs(os.path.join(self.config, "plugins"))

    def tearDown(self):
        self.tmp.cleanup()

    def write(self, plugins):
        with open(os.path.join(self.config, "plugins", "installed_plugins.json"), "w", encoding="utf-8") as fh:
            json.dump({"version": 2, "plugins": plugins}, fh)

    def test_eintrag_des_eigenen_plugins(self):
        self.write({
            "work@workbench": [{"installPath": self.work, "version": "abc123", "lastUpdated": "2026-10-28T18:56:17Z"}],
            "andere@x": [{"installPath": os.path.join(self.tmp.name, "anderes"), "version": "1.0"}],
        })
        self.assertEqual(skill_log.plugin_info(self.script, self.config),
                         {"plugin": "work@workbench", "plugin_version": "abc123",
                          "plugin_updated": "2026-10-28T18:56:17Z"})

    def test_ohne_passenden_eintrag_leer(self):
        self.write({"andere@x": [{"installPath": os.path.join(self.tmp.name, "anderes"), "version": "1.0"}]})
        self.assertEqual(skill_log.plugin_info(self.script, self.config), {})

    def test_ohne_datei_leer(self):
        self.assertEqual(skill_log.plugin_info(self.script, self.config), {})

    def test_kaputte_datei_leer(self):
        with open(os.path.join(self.config, "plugins", "installed_plugins.json"), "w") as fh:
            fh.write("{kaputt")
        self.assertEqual(skill_log.plugin_info(self.script, self.config), {})

    def test_unerwarteter_aufbau_leer(self):
        self.write(["liste"])
        self.assertEqual(skill_log.plugin_info(self.script, self.config), {})
        self.write({"work@workbench": ["kein dict", None]})
        self.assertEqual(skill_log.plugin_info(self.script, self.config), {})

    def test_nur_session_bekommt_plugin_felder(self):
        prompt = skill_log.build({"hook_event_name": "UserPromptSubmit", "prompt": "hallo", "cwd": self.tmp.name})
        self.assertNotIn("plugin", prompt)


if __name__ == "__main__":
    unittest.main()
