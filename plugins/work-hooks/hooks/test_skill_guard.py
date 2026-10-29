#!/usr/bin/env python3
"""Tests für skill_guard.py (nur Standardbibliothek): python3 -m unittest plugins/work-hooks/hooks/test_skill_guard.py"""

import copy
import json
import os
import sys
import tempfile
import unittest

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import skill_guard as g  # noqa: E402

RULES = g.load_rules(os.path.join(os.path.dirname(os.path.abspath(__file__)), "regeln.json"))
# Die Mechanik wird gegen feste Modi geprüft; die echten Modi ändern sich beim Lernen (skill-auswertung)
MECH = copy.deepcopy(RULES)
for _rule in MECH["regeln"]:
    _rule["modus"] = "blocken" if _rule["id"] in ("code", "mockup") else "warnen"


def hook(event, tool, tool_input, cwd="/home/nutzer/projekte/demo"):
    return {"hook_event_name": event, "tool_name": tool, "tool_input": tool_input, "cwd": cwd,
            "session_id": "s1", "tool_use_id": "t1"}


class RegelnTest(unittest.TestCase):
    def test_regeldatei_ist_gueltig(self):
        ids = [r["id"] for r in RULES["regeln"]]
        self.assertEqual(len(ids), len(set(ids)))
        for rule in RULES["regeln"]:
            self.assertIn(rule["modus"], ("blocken", "warnen", "aus"))
            self.assertTrue(rule["pflicht"])
            self.assertTrue(set(rule["aktion"]) <= {"datei", "datei:neu", "bash:schreibt", "bash:commit",
                                                    "mcp:clickup-schreibt", "bash:merge"})
            self.assertTrue(set(rule.get("gilt_bis", [])) <= set(RULES.get("grenzen", {})))


class BlockenTest(unittest.TestCase):
    def test_code_ohne_code_erstellen_wird_geblockt(self):
        code, _, err, entries = g.decide(hook("PreToolUse", "Edit", {"file_path": "logik/rechte.py"}), MECH, set())
        self.assertEqual(code, 2)
        self.assertIn("code-erstellen", err)
        self.assertEqual(entries[0]["regel"], "code")

    def test_code_mit_code_erstellen_laeuft(self):
        code, _, _, _ = g.decide(hook("PreToolUse", "Edit", {"file_path": "logik/rechte.py"}), MECH,
                                 {"code-erstellen", "tracker"})
        self.assertEqual(code, 0)

    def test_ticket_reicht_fuer_code(self):
        code, _, _, _ = g.decide(hook("PreToolUse", "Write", {"file_path": "x.js"}), MECH, {"ticket"})
        self.assertEqual(code, 0)

    def test_mockup_braucht_mockup_erstellen(self):
        data = hook("PreToolUse", "Write", {"file_path": "/home/nutzer/projekte/demo/mockups/quelle/symbol.js"})
        code, _, err, _ = g.decide(data, MECH, {"code-erstellen"})
        self.assertEqual(code, 2)
        self.assertIn("mockup-erstellen", err)
        self.assertEqual(g.decide(data, MECH, {"mockup-erstellen"})[0], 0)

    def test_shell_schreiben_wird_erkannt(self):
        data = hook("PreToolUse", "Bash", {"command": "cat > custom_components/baustelle/logik/rechte.py <<'EOF'\nx=1\nEOF"})
        self.assertEqual(g.decide(data, MECH, set())[0], 2)

    def test_shell_lesen_bleibt_frei(self):
        data = hook("PreToolUse", "Bash", {"command": "sed -n 1,40p logik/soll.py; grep -n x panel.py | head"})
        self.assertEqual(g.decide(data, MECH, set())[0], 0)

    def test_ziel_mit_shell_variable_bleibt_frei(self):
        data = hook("PreToolUse", "Bash", {"command": "python3 x.py > $S/runden.json; cat > $S/tx.py <<'E'\nE"})
        self.assertEqual(g.decide(data, MECH, set())[0], 0)

    def test_scratchpad_und_tmp_sind_frei(self):
        for path in ("/tmp/claude-0/x/scratchpad/a.py", "/tmp/x.json", "/home/nutzer/.claude/skill-log/a.json"):
            self.assertEqual(g.decide(hook("PreToolUse", "Write", {"file_path": path}), MECH, set())[0], 0, path)

    def test_warnregeln_blocken_nicht(self):
        code, _, _, _ = g.decide(hook("PreToolUse", "Edit", {"file_path": "docs/bauplan.md"}), MECH, set())
        self.assertEqual(code, 0)


class WarnenTest(unittest.TestCase):
    def test_doku_ohne_skill_gibt_hinweis_nach_der_aktion(self):
        code, out, _, entries = g.decide(hook("PostToolUse", "Edit", {"file_path": "docs/bauplan.md"}), MECH, set())
        self.assertEqual(code, 0)
        ctx = json.loads(out)["hookSpecificOutput"]
        self.assertEqual(ctx["hookEventName"], "PostToolUse")
        self.assertIn("doc-pflege", ctx["additionalContext"])
        self.assertEqual(entries[0]["entscheidung"], "gewarnt")

    def test_clickup_ohne_tracker_warnt(self):
        data = hook("PostToolUse", "mcp__claude_ai_ClickUp__clickup_create_task", {"name": "x"})
        self.assertIn("tracker", g.decide(data, MECH, set())[1])
        self.assertEqual(g.decide(data, MECH, {"tracker"})[1], "")

    def test_clickup_lesen_ist_frei(self):
        data = hook("PostToolUse", "mcp__claude_ai_ClickUp__clickup_filter_tasks", {})
        self.assertEqual(g.decide(data, MECH, set())[1], "")

    def test_commit_ohne_skill_warnt(self):
        data = hook("PostToolUse", "Bash", {"command": "git add x && git commit -q -m 'x'"})
        self.assertIn("commit", g.decide(data, MECH, set())[1])

    def test_commit_text_im_heredoc_ist_kein_commit(self):
        # Befund 10.10.2026: ein Python-Leseskript mit dem Suchwort git commit wurde als Commit geblockt
        for command in ("python3 - log.jsonl <<'EOF'\nkeys = ['git commit', 'gh repo']\nEOF",
                        "cat <<-EOF > notiz.txt\n\tgit commit -m x\n\tEOF\n"):
            acts = g.actions(hook("PreToolUse", "Bash", {"command": command}))
            self.assertNotIn("bash:commit", [a for a, _ in acts], command)

    def test_commit_vor_und_nach_heredoc_bleibt_commit(self):
        for command in ("git add -A && git commit -q -F - <<'EOF'\n[v0.1.0] Modul, Neu: x\nEOF",
                        "cat > a.txt <<'EOF'\nx\nEOF\ngit commit -m y",
                        "git -C /repo commit -m x"):
            self.assertTrue(g.is_commit(command), command)

    def test_pfade_nach_cd(self):
        # Befund 10.10.2026: nach cd wurden relative Ziele gegen den Ordner der Sitzung aufgelöst
        def ziele(command):
            return [t for a, t in g.actions(hook("PreToolUse", "Bash", {"command": command})) if a == "bash:schreibt"]
        self.assertEqual(ziele("cd sub && echo x > a.txt; cd .. && echo y > b.txt"),
                         ["/home/nutzer/projekte/demo/sub/a.txt", "/home/nutzer/projekte/demo/b.txt"])
        self.assertEqual(ziele("cd /repo && sed -i 's/a/b/' docs/x.md"), ["/repo/docs/x.md"])
        self.assertEqual(ziele("cd $REPO && echo x > a.txt > /tmp/log.txt"), ["/tmp/log.txt"])

    def test_blockmeldung_nennt_plugin_stand(self):
        self.assertEqual(g.plugin_stand("/x/cache/workbench/work/cc300ef2050c"), "cc300ef")
        self.assertEqual(g.plugin_stand("/config/projekte/claude-workbench"), "")
        self.assertIn("cc300ef", g.stand_hinweis("cc300ef"))
        self.assertEqual(g.stand_hinweis(""), "")

    def test_blockregel_warnt_nicht_nochmal(self):
        data = hook("PostToolUse", "Edit", {"file_path": "logik/rechte.py"})
        self.assertEqual(g.decide(data, MECH, set())[1], "")


class ProjektTest(unittest.TestCase):
    def test_skills_regel_nur_im_skill_repo(self):
        repo = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..")
        data = hook("PostToolUse", "Edit", {"file_path": "skills/tracker/SKILL.md"}, cwd=os.path.abspath(repo))
        self.assertIn("skill-pflege", g.decide(data, MECH, set())[1])
        data = hook("PostToolUse", "Edit", {"file_path": "/anderswo/skills/x/SKILL.md"}, cwd="/anderswo")
        self.assertNotIn("skill-pflege", g.decide(data, MECH, set())[1])


class TranscriptTest(unittest.TestCase):
    def test_subagent_transcript_getrennt_von_hauptsitzung(self):
        with tempfile.TemporaryDirectory() as tmp:
            main = os.path.join(tmp, "s1.jsonl")
            sub = os.path.join(tmp, "s1", "subagents", "agent-a.jsonl")
            os.makedirs(os.path.dirname(sub))
            with open(main, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"message": {"content": [
                    {"type": "tool_use", "name": "Skill", "input": {"skill": "anthropic-skills:code-erstellen"}}]}}) + "\n")
                fh.write(json.dumps({"message": {"content": "<command-name>/mockup-erstellen</command-name>"}}) + "\n")
            with open(sub, "w", encoding="utf-8") as fh:
                fh.write("{}\n")
            own, haupt = g.transcripts({"transcript_path": sub, "session_id": "s1"})
            self.assertEqual((own, haupt), ([sub], [main]))
            self.assertEqual(g.loaded_skills(haupt), {"code-erstellen", "mockup-erstellen"})
            self.assertEqual(g.loaded_skills(own), set())

    def test_skills_nach_compaction_aus_anhang(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = os.path.join(tmp, "s2.jsonl")
            with open(path, "w", encoding="utf-8") as fh:
                fh.write(json.dumps({"type": "attachment", "attachment": {"type": "invoked_skills", "skills": [
                    {"name": "anthropic-skills:code-erstellen", "content": "…"}, {"name": "update-config"}]}}) + "\n")
            self.assertEqual(g.loaded_skills([path]), {"code-erstellen", "update-config"})


class SicherheitTest(unittest.TestCase):
    def test_kaputte_eingabe_blockiert_nie(self):
        self.assertEqual(g.decide({"hook_event_name": "PreToolUse"}, MECH, set())[0], 0)
        self.assertEqual(g.decide({}, MECH, set())[0], 0)



class EinstellungTest(unittest.TestCase):
    """Umgebungsvariable vor Plugin-Option (userConfig → CLAUDE_PLUGIN_OPTION_<KEY>)."""

    def setUp(self):
        self._env = {k: os.environ.pop(k) for k in list(os.environ)
                     if k.startswith("CLAUDE_PLUGIN_OPTION_") or k.startswith("SKILL_")}

    def tearDown(self):
        for k in [k for k in os.environ if k.startswith("CLAUDE_PLUGIN_OPTION_") or k.startswith("SKILL_")]:
            del os.environ[k]
        os.environ.update(self._env)

    def test_plugin_option_wenn_keine_umgebungsvariable(self):
        os.environ["CLAUDE_PLUGIN_OPTION_LOG_HOST"] = "laptop"
        self.assertEqual(g.setting("SKILL_LOG_HOST", "LOG_HOST"), "laptop")

    def test_umgebungsvariable_gewinnt(self):
        os.environ["CLAUDE_PLUGIN_OPTION_LOG_HOST"] = "laptop"
        os.environ["SKILL_LOG_HOST"] = "ha-pi"
        self.assertEqual(g.setting("SKILL_LOG_HOST", "LOG_HOST"), "ha-pi")

    def test_ohne_beides_leer(self):
        self.assertEqual(g.setting("SKILL_GUARD", "SKILL_GUARD"), "")

    def test_waechter_ueber_plugin_option_aus(self):
        os.environ["CLAUDE_PLUGIN_OPTION_SKILL_GUARD"] = "false"
        self.assertIn(g.setting("SKILL_GUARD", "SKILL_GUARD").lower(), g.OFF)


def _tx(*events):
    """Transcript-Zeilen wie Claude Code: skill, commit (ok/fehler, optional Befehl), user-Text, clickup-Status, compaction."""
    lines, n = [], 0
    for ev in events:
        n += 1
        kind = ev[0]
        if kind == "skill":
            lines.append({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": f"s{n}", "name": "Skill", "input": {"skill": ev[1]}}]}})
        elif kind == "commit":
            lines.append({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": f"c{n}", "name": "Bash", "input": {"command": ev[2] if len(ev) > 2 else "git commit -m x"}}]}})
            lines.append({"type": "user", "message": {"content": [
                {"type": "tool_result", "tool_use_id": f"c{n}", "is_error": ev[1] != "ok", "content": "x"}]}})
        elif kind == "user":
            lines.append({"type": "user", "message": {"content": ev[1]}})
        elif kind == "status":
            lines.append({"type": "assistant", "message": {"content": [
                {"type": "tool_use", "id": f"u{n}", "name": "mcp__claude_ai_ClickUp__clickup_update_task",
                 "input": {"task_id": "1", "status": ev[1]}}]}})
        elif kind == "compaction":
            lines.append({"type": "attachment", "attachment": {"type": "invoked_skills",
                                                               "skills": [{"name": x} for x in ev[1]]}})
    fd, path = tempfile.mkstemp(suffix=".jsonl")
    with os.fdopen(fd, "w", encoding="utf-8") as fh:
        for line in lines:
            fh.write(json.dumps(line) + "\n")
    return path


class GrenzenTest(unittest.TestCase):
    ALLE = ["commit", "aufgabenstart", "task_id"]

    def aktiv(self, *events, gilt_bis=None):
        path = _tx(*events)
        try:
            grenzen = RULES["grenzen"]
            return g.active(g.history([path], grenzen), grenzen, self.ALLE if gilt_bis is None else gilt_bis)
        finally:
            os.unlink(path)

    def test_ohne_grenze_gilt_skill_weiter(self):
        self.assertEqual(self.aktiv(("skill", "work:code-erstellen"), ("user", "weiter")), {"code-erstellen"})

    def test_commit_verbraucht_code_doku_commit_skills(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("skill", "git-commit-helper"), ("skill", "tracker"),
                                    ("commit", "ok")), {"tracker"})

    def test_commit_text_im_heredoc_ist_keine_grenze(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"),
                                    ("commit", "ok", "python3 - <<'EOF'\nprint('git commit')\nEOF")), {"code-erstellen"})

    def test_gescheiterter_commit_ist_keine_grenze(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("commit", "fehler")), {"code-erstellen"})

    def test_nach_grenze_neu_geladen_gilt(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("commit", "ok"), ("skill", "code-erstellen")),
                         {"code-erstellen"})

    def test_aufgabenstart_verbraucht_alles_ausser_tracker(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("skill", "tracker"), ("status", "in development")),
                         {"tracker"})

    def test_anderer_status_ist_keine_grenze(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("status", "testing")), {"code-erstellen"})

    def test_task_id_in_nachricht(self):
        for text in ("mach BSM-026", "Bsm 026", "ticket FE-0012"):
            self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("user", text)), set(), text)

    def test_keine_task_id(self):
        for text in ("weiter mit .13", "Version 0.8.104", "wie lange noch?"):
            self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("user", text)), {"code-erstellen"}, text)

    def test_compaction_holt_verbrauchte_nicht_zurueck(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("commit", "ok"),
                                    ("compaction", ["code-erstellen"])), set())

    def test_compaction_ohne_verlauf_zaehlt(self):
        self.assertEqual(self.aktiv(("compaction", ["code-erstellen"])), {"code-erstellen"})

    def test_regel_ohne_gilt_bis_ignoriert_grenzen(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("commit", "ok"), gilt_bis=[]), {"code-erstellen"})


class NeueRegelnTest(unittest.TestCase):
    def test_neue_doku_ohne_doc_pflege_wird_geblockt(self):
        # Pfad außerhalb von /tmp (dort prüft der Wächter nie), den es nicht gibt
        data = hook("PreToolUse", "Write", {"file_path": "/home/nutzer/projekte/demo/docs/betrieb-neu.md"})
        code, _, err, _ = g.decide(data, RULES, {"code-erstellen"})
        self.assertEqual(code, 2)
        self.assertIn("doku-neu", err)
        code, _, _, _ = g.decide(data, RULES, {"doc-pflege"})
        self.assertEqual(code, 0)

    def test_bestehende_doku_mit_code_erstellen_erlaubt(self):
        with tempfile.TemporaryDirectory() as d:
            os.makedirs(os.path.join(d, "docs"))
            path = os.path.join(d, "docs", "bauplan.md")
            open(path, "w").close()
            code, _, _, _ = g.decide(hook("PreToolUse", "Edit", {"file_path": path}, cwd=d), RULES, {"code-erstellen"})
            self.assertEqual(code, 0)

    def test_commit_braucht_git_commit_helper(self):
        data = hook("PreToolUse", "Bash", {"command": "git commit -m x"})
        self.assertEqual(g.decide(data, RULES, {"code-erstellen"})[0], 2)
        self.assertEqual(g.decide(data, RULES, {"git-commit-helper"})[0], 0)


class VerzoegerungTest(unittest.TestCase):
    """Gerade geladene Skills stehen sofort im Skill-Log, im Transcript erst später."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self._env = os.environ.get("SKILL_LOG_DIR")
        os.environ["SKILL_LOG_DIR"] = self.dir

    def tearDown(self):
        if self._env is None:
            os.environ.pop("SKILL_LOG_DIR", None)
        else:
            os.environ["SKILL_LOG_DIR"] = self._env

    def log(self, ts, skill, session="s1"):
        with open(os.path.join(self.dir, "2026-10.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps({"v": 1, "ts": ts, "session": session, "event": "skill", "skill": skill, "ok": True}) + "\n")

    def test_skill_nach_letzter_transcript_zeile_zaehlt(self):
        self.log("2026-10-08T16:00:31Z", "work:doc-pflege")
        self.assertEqual(g.recent_skills("s1", "2026-10-08T16:00:29"), ["doc-pflege"])

    def test_aelterer_skill_zaehlt_nicht(self):
        self.log("2026-10-08T15:00:00Z", "work:doc-pflege")
        self.assertEqual(g.recent_skills("s1", "2026-10-08T16:00:29"), [])

    def test_andere_sitzung_zaehlt_nicht(self):
        self.log("2026-10-08T16:00:31Z", "work:doc-pflege", session="s2")
        self.assertEqual(g.recent_skills("s1", "2026-10-08T16:00:29"), [])

    def test_letzter_zeitstempel(self):
        path = _tx(("skill", "code-erstellen"))
        try:
            with open(path, "a", encoding="utf-8") as fh:
                fh.write(json.dumps({"type": "user", "timestamp": "2026-10-08T16:00:29.800Z"}) + "\n")
            self.assertEqual(g.last_timestamp([path]), "2026-10-08T16:00:29")
        finally:
            os.unlink(path)


class NamenTest(unittest.TestCase):
    def test_volle_namen_aus_marketplace(self):
        names = g.plugin_names()
        self.assertEqual(names.get("code-erstellen"), "work:code-erstellen")
        self.assertEqual(names.get("skill-pflege"), "skill-workshop:skill-pflege")

    def test_meldung_nennt_volle_namen_und_hinweis(self):
        code, _, err, _ = g.decide(hook("PreToolUse", "Edit", {"file_path": "logik/rechte.py"}), MECH, set())
        self.assertEqual(code, 2)
        self.assertIn("work:code-erstellen", err)
        self.assertIn("vollen Namen samt Präfix", err)

    def test_ohne_marketplace_ohne_praefix(self):
        self.assertEqual(g.plugin_names("/gibt/es/nicht.json"), {})
        rule = {"id": "code", "beschreibung": "x", "pflicht": ["code-erstellen"]}
        self.assertIn("Zuständig: code-erstellen", g.message([(rule, "")], names={}))

class ArbeitsordnerTest(unittest.TestCase):
    """Befund Lumora 21.10.2026: Agenten-Worktrees unter <repo>/.claude/worktrees/ fielen unter */.claude/*."""
    REPO = "/home/nutzer/projekte/demo"
    WT = REPO + "/.claude/worktrees/agent-x"

    def test_code_im_worktree_wird_geblockt(self):
        for tool, tin in (("Edit", {"file_path": self.WT + "/src/Viewer.cs"}),
                          ("Write", {"file_path": self.WT + "/src/Neu.cs"}),
                          ("Bash", {"command": "cat > src/Viewer.cs <<'EOF'\nx\nEOF"})):
            data = hook("PreToolUse", tool, tin, cwd=self.WT)
            code, _, err, _ = g.decide(data, RULES, set())
            self.assertEqual(code, 2, tool)
            self.assertIn("code-erstellen", err)
            self.assertEqual(g.decide(data, RULES, {"code-erstellen"})[0], 0, tool)

    def test_zusammenbau_worktree_wird_geprueft(self):
        data = hook("PreToolUse", "Edit", {"file_path": self.REPO + "/.claude/worktrees/integration-1/App.xaml"})
        self.assertEqual(g.decide(data, RULES, set())[0], 2)

    def test_konfiguration_bleibt_frei(self):
        for path in ("/home/nutzer/.claude/settings.json", self.REPO + "/.claude/settings.local.json",
                     "/home/nutzer/.claude/projects/-home-nutzer-projekte-demo/memory/notiz.json",
                     "/home/nutzer/.claude/plugins/cache/workbench/work/abc1234/hooks/x.py",
                     self.WT + "/.claude/settings.json", self.WT + "/node_modules/x/a.js"):
            self.assertEqual(g.decide(hook("PreToolUse", "Write", {"file_path": path}), RULES, set())[0], 0, path)

    def test_pfad_im_repo(self):
        self.assertEqual(g.repo_path(self.WT + "/src/a.cs", ["/.claude/worktrees/"]), self.REPO + "/src/a.cs")
        self.assertEqual(g.repo_path(self.WT, ["/.claude/worktrees/"]), self.REPO)
        self.assertEqual(g.repo_path("C:\\r\\.claude\\worktrees\\a\\x.cs", ["/.claude/worktrees/"]), "C:/r/x.cs")
        self.assertEqual(g.repo_path(self.REPO + "/a.cs", ["/.claude/worktrees/"]), self.REPO + "/a.cs")


class SubagentTest(unittest.TestCase):
    """Ein Subagent muss den Pflicht-Skill selbst laden (Hook-Feld agent_id)."""

    def setUp(self):
        self.dir = tempfile.mkdtemp()
        self.log_dir = os.path.join(self.dir, "log")
        os.makedirs(self.log_dir)
        self._env = os.environ.get("SKILL_LOG_DIR")
        os.environ["SKILL_LOG_DIR"] = self.log_dir
        self.main = os.path.join(self.dir, "s1.jsonl")
        self.sub = os.path.join(self.dir, "s1", "subagents", "agent-a1.jsonl")
        os.makedirs(os.path.dirname(self.sub))
        self.write(self.main, "work:code-erstellen")

    def tearDown(self):
        if self._env is None:
            os.environ.pop("SKILL_LOG_DIR", None)
        else:
            os.environ["SKILL_LOG_DIR"] = self._env

    @staticmethod
    def write(path, *skills):
        with open(path, "w", encoding="utf-8") as fh:
            for skill in skills:
                fh.write(json.dumps({"type": "assistant", "message": {"content": [
                    {"type": "tool_use", "id": "x", "name": "Skill", "input": {"skill": skill}}]}}) + "\n")

    def data(self, tp, agent="a1"):
        d = hook("PreToolUse", "Edit", {"file_path": "/home/nutzer/projekte/demo/src/A.cs"})
        d["transcript_path"] = tp
        if agent:
            d["agent_id"] = agent
        return d

    def test_hauptsitzung_deckt_subagent_nicht(self):
        open(self.sub, "w").close()
        for tp in (self.sub, self.main):  # transcript_path zeigt auf das eigene oder auf das der Hauptsitzung
            self.assertEqual(g.decide(self.data(tp), RULES)[0], 2, tp)

    def test_subagent_mit_eigenem_skill_laeuft(self):
        self.write(self.sub, "work:code-erstellen")
        self.assertEqual(g.decide(self.data(self.main), RULES)[0], 0)

    def test_hauptsitzung_mit_skill_laeuft(self):
        self.assertEqual(g.decide(self.data(self.main, agent=""), RULES)[0], 0)

    def test_aeltere_fassung_ohne_agent_id(self):
        open(self.sub, "w").close()
        self.assertEqual(g.agent_of({"transcript_path": self.sub}), "a1")
        self.assertEqual(g.decide(self.data(self.sub, agent=""), RULES)[0], 2)

    def test_erben_nur_mit_regelfeld(self):
        open(self.sub, "w").close()
        rules = copy.deepcopy(RULES)
        next(r for r in rules["regeln"] if r["id"] == "code")["erbt_hauptsitzung"] = True
        self.assertEqual(g.decide(self.data(self.sub), rules)[0], 0)

    def log(self, skill, agent):
        entry = {"v": 1, "ts": "2026-10-21T10:00:00Z", "session": "s1", "event": "skill", "skill": skill, "ok": True}
        if agent:
            entry["agent"] = agent
        with open(os.path.join(self.log_dir, "2026-10.jsonl"), "a", encoding="utf-8") as fh:
            fh.write(json.dumps(entry) + "\n")

    def test_skill_log_eines_anderen_agenten_zaehlt_nicht(self):
        self.log("work:code-erstellen", "b2")
        self.log("work:code-erstellen", "")
        self.assertEqual(g.recent_skills("s1", "", "a1"), [])
        self.assertEqual(g.decide(self.data(self.sub), RULES)[0], 2)  # Transcript des Agenten fehlt noch
        self.log("work:code-erstellen", "a1")
        self.assertEqual(g.recent_skills("s1", "", "a1"), ["code-erstellen"])
        self.assertEqual(g.decide(self.data(self.sub), RULES)[0], 0)

    def test_hauptsitzung_zaehlt_keine_agenten_skills(self):
        self.log("work:doc-pflege", "a1")
        self.assertEqual(g.recent_skills("s1", "2026-10-21T09:00:00", ""), [])


class PromptGrenzeTest(unittest.TestCase):
    """Grenze prompt und Warnregel code-prompt (21.10.2026)."""

    def aktiv(self, *events):
        path = _tx(*events)
        try:
            grenzen = RULES["grenzen"]
            return g.active(g.history([path], grenzen), grenzen, ["commit", "aufgabenstart", "task_id", "prompt"])
        finally:
            os.unlink(path)

    def test_neuer_prompt_verbraucht_code_erstellen(self):
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("skill", "tracker"), ("user", "weiter")),
                         {"tracker"})
        self.assertEqual(self.aktiv(("user", "bau X"), ("skill", "code-erstellen")), {"code-erstellen"})

    def test_keine_grenze(self):
        for text in ("<task-notification>\n<task-id>x</task-id>", "<system-reminder>x</system-reminder>",
                     "[Request interrupted by user for tool use]", "   "):
            self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("user", text)), {"code-erstellen"}, text)
        self.assertEqual(self.aktiv(("skill", "code-erstellen"), ("commit", "fehler")), {"code-erstellen"})

    def test_slash_befehl_zaehlt_nach_der_grenze(self):
        self.assertEqual(self.aktiv(("user", "<command-name>/code-erstellen</command-name> mach x")),
                         {"code-erstellen"})

    def test_meta_und_zusammenfassung_keine_grenze(self):
        self.assertFalse(g.is_prompt({"isMeta": True}, "x"))
        self.assertFalse(g.is_prompt({"isCompactSummary": True}, "This session is being continued"))
        self.assertTrue(g.is_prompt({}, "ja"))

    def test_code_prompt_warnt_nur_wenn_code_erfuellt(self):
        data = hook("PostToolUse", "Edit", {"file_path": "/home/nutzer/projekte/demo/src/A.cs"})
        rule_sets = {"code": {"code-erstellen"}, "code-prompt": set()}
        skills = lambda rule: rule_sets.get(rule["id"], {"code-erstellen"})  # noqa: E731
        code, out, _, entries = g.decide(data, RULES, skills)
        self.assertEqual(code, 0)
        self.assertIn("code-prompt", out)
        self.assertEqual(entries[0]["entscheidung"], "gewarnt")
        self.assertEqual(g.decide(data, RULES, set())[1], "")  # ohne Skill blockt schon code vorher

    def test_code_prompt_meldet_wenn_grundregel_aus(self):
        rules = copy.deepcopy(RULES)
        next(r for r in rules["regeln"] if r["id"] == "code")["modus"] = "aus"
        data = hook("PostToolUse", "Edit", {"file_path": "/home/nutzer/projekte/demo/src/A.cs"})
        self.assertIn("code-prompt", g.decide(data, rules, set())[1])

    def test_skill_log_schreibt_agent(self):
        import skill_log
        base = {"hook_event_name": "PostToolUse", "tool_name": "Skill", "tool_input": {"skill": "work:x"},
                "session_id": "s1", "cwd": "/tmp"}
        self.assertNotIn("agent", skill_log.build(base))
        self.assertEqual(skill_log.build(dict(base, agent_id="a1"))["agent"], "a1")
        self.assertEqual(skill_log.build(dict(base, transcript_path="/p/s1/subagents/agent-b2.jsonl"))["agent"], "b2")


class AuswertungOktoberTest(unittest.TestCase):
    """Befunde der Skill-Auswertung vom 21.10.2026."""

    def ziele(self, command):
        return [t for a, t in g.actions(hook("PreToolUse", "Bash", {"command": command})) if a == "bash:schreibt"]

    def test_literal_im_inhalt_ist_kein_ziel(self):
        # Befund 10.10.: `datei: 'hochrechnung.html'` im geschriebenen JS wurde zum Ziel
        command = ("python3 - <<'EOF'\nopen('mockups/quelle/hochrechnung.js', 'w')"
                   ".write(\"const x = {datei: 'hochrechnung.html'}\")\nEOF")
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/mockups/quelle/hochrechnung.js"])

    def test_zip_schreibt_nur_das_archiv(self):
        # Befund 14.10.: z.write('skills/x/SKILL.md') machte die gelesene Datei zum Ziel
        command = ("python3 - <<'EOF'\nimport zipfile\nwith zipfile.ZipFile('/tmp/x/scratchpad/a.zip', 'w') as z:\n"
                   "    z.write('skills/audit/SKILL.md')\nEOF")
        self.assertEqual(self.ziele(command), ["/tmp/x/scratchpad/a.zip"])
        self.assertEqual(g.decide(hook("PreToolUse", "Bash", {"command": command}), RULES, set())[0], 0)

    def test_ziel_ueber_namen(self):
        command = "python3 - <<'EOF'\np = 'src/a.py'\ns = open(p).read()\nopen(p, 'w').write(s)\nEOF"
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/src/a.py"])
        command = "python3 - <<'EOF'\nfrom pathlib import Path\nPath('docs/x.md').write_text('y')\nEOF"
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/docs/x.md"])

    def test_unbekanntes_ziel_faellt_auf_alle_dateinamen_zurueck(self):
        command = "python3 - <<'EOF'\ndef patch(p):\n    open(p, 'w').write('x')\npatch('src/b.py')\nEOF"
        self.assertIn("/home/nutzer/projekte/demo/src/b.py", self.ziele(command))

    def test_zeilen_nach_dem_heredoc_sind_shell(self):
        # Befund 29.10.: das gelesene manifest.json in python -c nach dem Heredoc wurde Ziel, CLAUDE.md nicht
        command = ("cd /r && python3 - <<'EOF'\np='CLAUDE.md'; t=open(p,encoding='utf-8').read()\n"
                   "open(p,'w',encoding='utf-8').write(t)\nEOF\ngit status --short && "
                   "V=$(python3 -c \"import json;print(json.load(open('manifest.json'))['version'])\"); echo $V")
        self.assertEqual(self.ziele(command), ["/r/CLAUDE.md"])
        command = "cat > a.txt <<'EOF'\nx\nEOF\necho y > b.txt"
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/a.txt", "/home/nutzer/projekte/demo/b.txt"])

    def test_parameter_der_patch_funktion(self):
        # Befund 25.10.: tools/tickets-fenster.sh stand nur im Text, der in CLAUDE.md geschrieben wurde
        command = ("python3 - <<'EOF'\ndef rep(p,a,b):\n    s=open(p).read(); open(p,'w').write(s.replace(a,b))\n"
                   "rep('CLAUDE.md','''alt''','''neu: `tools/tickets-fenster.sh` bleibt lokal''')\nEOF")
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/CLAUDE.md"])

    def test_inhalt_einer_geschriebenen_datei_ist_kein_code(self):
        # Befund 21.10.: open('mockups/…', 'w') im Text einer Testdatei wurde Ziel
        inhalt = "open('mockups/quelle/hochrechnung.js', 'w').write('x')"
        self.assertEqual(self.ziele(f"cat > tests/t.py <<'EOF'\n{inhalt}\nEOF"),
                         ["/home/nutzer/projekte/demo/tests/t.py"])
        command = f"python3 - <<'EOF'\np='tests/t.py'\nopen(p,'w').write('''{inhalt}''')\nEOF"
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/tests/t.py"])

    def test_neu_belegter_name_behaelt_alle_ziele(self):
        command = ("python3 - <<'EOF'\np='docs/a.md'; s=open(p).read(); open(p,'w').write(s)\n"
                   "p='README.md'; s=open(p).read(); open(p,'w').write(s)\nEOF")
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/docs/a.md",
                                               "/home/nutzer/projekte/demo/README.md"])

    def test_spitze_klammer_in_anfuehrungszeichen_ist_keine_umleitung(self):
        command = "node x.js 2>&1 | grep -v \"528 > 340\" | tail -8; echo a > \"b.txt\""
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/b.txt"])

    def test_befunde_selbst_review(self):
        demo = "/home/nutzer/projekte/demo/"
        # Funktion nie mit Namen aufgerufen: Ziel unbekannt, Rückfall auf Dateinamen
        command = "python3 - <<'EOF'\ndef w(p):\n    open(p, 'w').write('x')\nziele = {'a': w}\nziele['a']('src/e.py')\nEOF"
        self.assertIn(demo + "src/e.py", self.ziele(command))
        # Modus an erster Stelle
        command = "python3 - <<'EOF'\nfrom pathlib import Path\nwith Path('src/f.py').open('w') as f:\n    f.write('x')\nEOF"
        self.assertEqual(self.ziele(command), [demo + "src/f.py"])
        command = "python3 - <<'EOF'\nimport io\nio.open('src/g.py', 'w').write('x')\nEOF"
        self.assertEqual(self.ziele(command), [demo + "src/g.py"])
        # Heredoc über eine Pipe an Python
        command = "cat <<'EOF' | python3\nopen('src/h.py', 'w').write('x')\nEOF"
        self.assertEqual(self.ziele(command), [demo + "src/h.py"])

    def test_befunde_gutachter(self):
        demo = "/home/nutzer/projekte/demo/"
        for command in ('echo x | tee "src/a.yaml"', "tee -a 'src/a.yaml' <<'EOF'\nx\nEOF"):
            self.assertEqual(self.ziele(command), [demo + "src/a.yaml"], command)
        # Skript per cat geschrieben und gleich ausgeführt
        command = "cat > /tmp/fix.py <<'EOF'\nopen('src/b.yaml','w').write('x')\nEOF\npython3 /tmp/fix.py"
        self.assertIn(demo + "src/b.yaml", self.ziele(command))
        # python -c in $(…), mit Optionen, ohne Leerzeichen
        for command in ("X=$(python3 -c \"open('src/c.yaml','w').write('x')\")",
                        "python3 -X utf8 -c \"open('src/c.yaml','w').write('x')\"",
                        "python3 -c\"open('src/c.yaml','w').write('x')\""):
            self.assertEqual(self.ziele(command), [demo + "src/c.yaml"], command)
        # Pipe in Python, <<\EOF, zwei Heredocs in einer Zeile
        self.assertIn(demo + "src/d.yaml", self.ziele("echo \"open('src/d.yaml','w').write('x')\" | python3"))
        self.assertEqual(self.ziele("python3 - <<\\EOF\nopen('src/e.yaml','w').write('x')\nEOF"), [demo + "src/e.yaml"])
        command = "cat <<A > /tmp/n.txt; python3 - <<'B'\nx\nA\nopen('src/f.yaml','w').write('x')\nB"
        self.assertIn(demo + "src/f.yaml", self.ziele(command))

    def test_python_c_schreibt(self):
        command = "python3 -c \"open('src/c.py','w').write('x')\""
        self.assertEqual(self.ziele(command), ["/home/nutzer/projekte/demo/src/c.py"])

    def test_nicht_lesbares_python_faellt_auf_dateinamen_zurueck(self):
        command = "python3 - <<'EOF'\nopen(p, 'w').write(\nx = 'src/d.py'\nEOF"
        self.assertIn("/home/nutzer/projekte/demo/src/d.py", self.ziele(command))

    def test_merge_ist_commit(self):
        def acts(command):
            return [a for a, _ in g.actions(hook("PostToolUse", "Bash", {"command": command}))]
        for command in ("gh pr merge 3 --squash", "git merge feature", "git -C /r merge --no-ff x"):
            self.assertIn("bash:merge", acts(command), command)
        for command in ("git merge --ff-only origin/main", "git merge --abort", "echo 'git merge' > notiz.txt",
                        "git merge-base HEAD main", "git merge-tree a b"):
            self.assertNotIn("bash:merge", acts(command), command)
        data = hook("PostToolUse", "Bash", {"command": "gh pr merge 4"})
        self.assertIn("merge", g.decide(data, RULES, set())[1])
        self.assertEqual(g.decide(data, RULES, {"git-commit-helper"})[1], "")

    def test_projekt_im_worktree(self):
        import skill_log
        with tempfile.TemporaryDirectory() as tmp:
            wt = os.path.join(tmp, "03_Foto", ".claude", "worktrees", "elated-bun")
            os.makedirs(wt)
            self.assertEqual(g.project_of(wt), "03_Foto")
            self.assertEqual(skill_log.project_of(wt), "03_Foto")
        self.assertEqual(skill_log.repo_folder("D:\\r\\03_Foto\\.claude\\worktrees\\x\\src"), "D:/r/03_Foto")

    def test_stdin_als_utf8(self):
        import subprocess
        here = os.path.dirname(os.path.abspath(__file__))
        with tempfile.TemporaryDirectory() as tmp:
            data = json.dumps({"hook_event_name": "UserPromptSubmit", "session_id": "s1", "cwd": tmp,
                               "prompt": "könnte"}, ensure_ascii=False).encode("utf-8")
            env = dict(os.environ, SKILL_LOG_DIR=tmp, PYTHONIOENCODING="cp1252")
            subprocess.run([sys.executable, os.path.join(here, "skill_log.py")], input=data, env=env, check=True)
            text = open(os.path.join(tmp, os.listdir(tmp)[0]), encoding="utf-8").read()
            self.assertIn("könnte", text)


if __name__ == "__main__":
    unittest.main()
