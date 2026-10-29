#!/usr/bin/env python3
"""Skill-Wächter v1: prüft vor bzw. nach einer Aktion, ob der zuständige Skill geladen ist (docs/skill-guard-v1.md).

Hook für Claude Code:
- PreToolUse  → Regeln mit modus "blocken": fehlt der Pflicht-Skill, wird die Aktion abgelehnt (Exit 2, Begründung
  auf stderr; Claude sieht sie und lädt den Skill nach).
- PostToolUse → Regeln mit modus "warnen": fehlt der Pflicht-Skill, bekommt Claude nach der Aktion einen Hinweis
  (additionalContext).
Ein Subagent (Hook-Feld agent_id) zählt nur seine eigenen Skills, außer eine Regel setzt erbt_hauptsitzung. Pfade in
Arbeitsordnern (Worktrees, regeln.json → arbeitsordner) werden wie der entsprechende Pfad im Repo geprüft.
Die Regeln stehen in regeln.json neben diesem Skript; skill-auswertung schärft sie nach. Jede Entscheidung landet als
Ereignis "guard" im Skill-Log (<SKILL_LOG_DIR>/<JJJJ-MM>.jsonl).

Ein Fehler im Skript blockiert nie: Exit 0 ohne Ausgabe. Abschalten: Umgebungsvariable SKILL_GUARD=aus.

Einstellungen (optional) – Umgebungsvariable oder Plugin-Option (/plugin configure); die Umgebungsvariable gewinnt:
  SKILL_GUARD       / skill_guard  "aus", "off", "0" oder "false" = nichts prüfen
  SKILL_GUARD_RULES / guard_rules  Pfad zur Regeldatei (Standard: regeln.json neben dem Skript)
  SKILL_LOG_DIR     / log_dir      Ablage des Skill-Logs (Standard: ~/.claude/skill-log)
  SKILL_LOG_HOST    / log_host     Name des Rechners im Log (Standard: Hostname)
"""

import ast
import datetime
import fnmatch
import glob
import json
import os
import re
import shlex
import socket
import sys
import warnings

HERE = os.path.dirname(os.path.abspath(__file__))

OFF = ("aus", "off", "0", "false", "no", "nein")


def setting(env, option):
    """Wert aus der Umgebungsvariable, sonst aus der Plugin-Option (userConfig → CLAUDE_PLUGIN_OPTION_<KEY>)."""
    return os.environ.get(env) or os.environ.get("CLAUDE_PLUGIN_OPTION_" + option) or ""


FILE_TOOLS = {"Edit", "Write", "MultiEdit", "NotebookEdit"}
WORKTREES = "/.claude/worktrees/"  # Arbeitsordner von Claude Code (Standard für regeln.json → arbeitsordner)
_CLICKUP_WRITE = re.compile(r"^mcp__.*clickup.*__clickup_(create|update|delete|merge|move|add|remove|attach|set)",
                            re.I)
_GIT_COMMIT = re.compile(r"\bgit\b(?:\s+-C\s+\S+)?\s+commit\b")
_QUOTED = re.compile(r"'[^']*'|\"[^\"]*\"")  # Text in Anführungszeichen ist kein Befehl
_MERGE = re.compile(r"\bgh\s+pr\s+merge\b|\bgit\b(?:\s+-C\s+\S+)?\s+merge\b(?!-)(?![^\n;&|]*--(?:ff-only|abort|quit|continue)\b)")
_HEREDOC = re.compile(r"(?<!<)<<(?!<)(-?)\s*\\?(['\"]?)([A-Za-z_][\w.-]*)\2")
_REDIRECT = re.compile(r"(?:^|[^0-9&<>])>>?\s*([^\s;|&<>()]+)")
_TARGET_BEFORE = re.compile(r"(?:>|\btee(?:\s+-a)?)\s*$")
_TEE = re.compile(r"\btee\s+(?:-a\s+)?([^\s;|&<>()]+)")
_SED_I = re.compile(r"\bsed\s+(?:-[^i\s]*\s+)*-i\S*\s+(.*)")
_CP_MV = re.compile(r"^\s*(?:cp|mv|install)\s+(.*)")
_PY_WRITE = re.compile(r"open\([^)]*['\"][wax]b?['\"]|\.write_text\(|\.write\(|shutil\.(?:copy|move)")
_QUOTED_FILE = re.compile(r"['\"]([\w./~-]*[\w-]\.[A-Za-z0-9]{1,5}|[\w./~-]*/mockups/[\w./-]+)['\"]")
_FILE_NAME = re.compile(r"[\w./~-]*[\w-]\.[A-Za-z0-9]{1,5}|[\w./~-]*/mockups/[\w./-]+")
_OPEN_MODULES = ("io", "os", "tarfile", "gzip", "bz2", "lzma", "codecs", "zipfile", "webbrowser")
_PY_COMMAND = re.compile(r"(?:^|[\s/(;&|`=])python[\d.]*\b")
_PY_INLINE = re.compile(r"(?:^|[\s/(;&|`=])python[\d.]*(?:\s+-[XWm]\s+\S+|\s+-[A-Za-z]+)*\s+-c\s*"
                        r"(?:'([^']*)'|\"((?:[^\"\\]|\\.)*)\")")
# Schreibaufrufe in Skripten: das Ziel ist ein Literal oder ein Name, der vorher ein Literal bekam
_ARG = r"\s*(?:(['\"])([^'\"\n]+)\1|([A-Za-z_]\w*))\s*"
_WRITE_CALLS = [
    re.compile(r"\b(?:open|ZipFile|TarFile\.open|tarfile\.open)\(" + _ARG + r",\s*(?:mode\s*=\s*)?['\"][wax]"),
    re.compile(r"\bPath\(" + _ARG + r"\)\.write_(?:text|bytes)\("),
    re.compile(r"\bshutil\.(?:copy\w*|move)\([^,\n]+," + _ARG + r"[,)]"),
]
_WRITE_NAME = re.compile(r"\b([A-Za-z_]\w*)\.write_(?:text|bytes)\(")
_ASSIGN = re.compile(r"^\s*([A-Za-z_]\w*)\s*=\s*(['\"])([^'\"\n]+)\2\s*$", re.M)
_SEGMENT = re.compile(r"\s*(?:;|&&|\|\||\||\n)\s*")
_CD = re.compile(r"^\s*(cd|pushd|popd)\b\s*(.*)$")
_COMMAND_NAME = re.compile(r"<command-name>/?([\w:.-]+)</command-name>")
_TIMESTAMP = re.compile(r'"timestamp":\s*"(\d{4}-\d\d-\d\dT\d\d:\d\d:\d\d)')
_PROJECT_ID = re.compile(r"^\s*-\s*Projekt-ID:\s*(\S+)", re.M)


def short(name):
    return (name or "").split(":")[-1]


def load_rules(path=None):
    path = path or setting("SKILL_GUARD_RULES", "GUARD_RULES") or os.path.join(HERE, "regeln.json")
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def project_of(cwd):
    """Projekt-ID aus dem Skill-Profil der nächsten CLAUDE.md ab cwd nach oben, sonst der Ordnername."""
    path = os.path.abspath(cwd or os.getcwd())
    start = path
    while True:
        claude_md = os.path.join(path, "CLAUDE.md")
        if os.path.isfile(claude_md):
            try:
                with open(claude_md, encoding="utf-8") as fh:
                    match = _PROJECT_ID.search(fh.read())
                if match:
                    return match.group(1)
            except OSError:
                pass
        parent = os.path.dirname(path)
        if parent == path:
            # im Worktree (<repo>/.claude/worktrees/<name>) zählt der Ordner des Repos, nicht der des Worktrees
            repo = repo_path(start, [WORKTREES])
            return os.path.basename(repo.rstrip("/\\")) or start
        path = parent


def agent_of(data):
    """Kennung des Subagenten, der die Aktion ausführt (Hook-Feld agent_id; ältere Fassungen: Transcript unter
    subagents/agent-<id>.jsonl); '' = Hauptsitzung."""
    if data.get("agent_id"):
        return str(data["agent_id"])
    tp = (data.get("transcript_path") or "").replace("\\", "/")
    match = re.search(r"/subagents/agent-([^/]+)\.jsonl$", tp)
    return match.group(1) if match else ""


def transcripts(data):
    """Transcripts der Aktion als (eigene, hauptsitzung): beim Subagenten sein eigenes Transcript und getrennt das der
    Hauptsitzung (zählt nur für Regeln mit erbt_hauptsitzung), sonst das der Sitzung und keins."""
    tp = data.get("transcript_path")
    if not tp:
        return [], []
    session = data.get("session_id")
    agent = agent_of(data)
    norm = tp.replace("\\", "/")
    root = tp[:norm.index("/subagents/")] if "/subagents/" in norm else os.path.splitext(tp)[0]
    folder = os.path.dirname(root)
    main = os.path.join(folder, (session or os.path.basename(root)) + ".jsonl")
    if not agent:
        own = [tp] + ([main] if main != tp else [])
        return [p for p in own if os.path.isfile(p)], []
    sub = os.path.join(folder, session or os.path.basename(root), "subagents", f"agent-{agent}.jsonl")
    own = [sub] + ([tp] if "/subagents/" in norm and tp != sub else [])
    return [p for p in own if os.path.isfile(p)], [p for p in [main] if os.path.isfile(p)]


def loaded_skills(paths):
    """Alle in den Transcripts geladenen Skills: Skill-Aufrufe, Slash-Befehle, Anhang invoked_skills (Compaction)."""
    found = set()
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if '"Skill"' not in line and "command-name" not in line and "invoked_skills" not in line:
                        continue
                    try:
                        msg = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    attachment = msg.get("attachment")
                    if isinstance(attachment, dict) and attachment.get("type") == "invoked_skills":
                        # nach einer Compaction legt Claude Code die geladenen Skills als Anhang ab
                        found.update(short(s.get("name")) for s in attachment.get("skills") or [])
                        continue
                    content = (msg.get("message") or {}).get("content")
                    if isinstance(content, str):
                        found.update(short(m) for m in _COMMAND_NAME.findall(content))
                    elif isinstance(content, list):
                        for block in content:
                            if block.get("type") == "tool_use" and block.get("name") == "Skill":
                                found.add(short((block.get("input") or {}).get("skill")))
                            elif block.get("type") == "text":
                                found.update(short(m) for m in _COMMAND_NAME.findall(block.get("text") or ""))
        except OSError:
            continue
    found.discard("")
    return found


def _user_text(content):
    """Text einer Nutzer-Nachricht (ohne Tool-Ergebnisse); None, wenn die Nachricht nur Tool-Ergebnisse enthält."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        texts = [b.get("text") or "" for b in content if b.get("type") == "text"]
        return "\n".join(texts) if texts else None
    return None


def events(lines, grenzen):
    """Verlauf aus Transcript-Zeilen: liefert (zeilennummer, ("skill", name) | ("grenze", id)) in Sitzungsreihenfolge.

    Grenzen (regeln.json → "grenzen"): commit = erfolgreicher git commit (Tool-Ergebnis ohne Fehler); aufgabenstart =
    ClickUp-Schreibaufruf mit einem der Status; task_id = Nutzer-Nachricht passt auf das Muster. Ein Anhang
    invoked_skills (Compaction) zählt nur Skills, die der Verlauf noch nicht kennt – verbrauchte kommen nicht zurück.
    """
    task = re.compile(grenzen["task_id"]["muster"]) if "task_id" in grenzen else None
    prompt = "prompt" in grenzen
    statuses = {x.lower() for x in (grenzen.get("aufgabenstart") or {}).get("status", [])}
    seen, commits = set(), set()
    for index, line in enumerate(lines):
        try:
            msg = json.loads(line)
        except json.JSONDecodeError:
            continue
        attachment = msg.get("attachment")
        if isinstance(attachment, dict) and attachment.get("type") == "invoked_skills":
            for s in attachment.get("skills") or []:
                name = short(s.get("name"))
                if name and name not in seen:
                    seen.add(name)
                    yield index, ("skill", name)
            continue
        content = (msg.get("message") or {}).get("content")
        if msg.get("type") == "user":
            text = _user_text(content)
            if text is not None:
                if prompt and is_prompt(msg, text):
                    yield index, ("grenze", "prompt")
                for name in _COMMAND_NAME.findall(text):
                    seen.add(short(name))
                    yield index, ("skill", short(name))
                if task and not msg.get("isMeta") and task.search(text):
                    yield index, ("grenze", "task_id")
            if isinstance(content, list):
                for block in content:
                    if block.get("type") == "tool_result" and block.get("tool_use_id") in commits \
                            and not block.get("is_error"):
                        yield index, ("grenze", "commit")
            continue
        if not isinstance(content, list):
            continue
        for block in content:
            if block.get("type") != "tool_use":
                continue
            name, tin = block.get("name") or "", block.get("input") or {}
            if name == "Skill":
                skill = short(tin.get("skill"))
                seen.add(skill)
                yield index, ("skill", skill)
            elif name == "Bash" and is_commit(tin.get("command") or "") and "commit" in grenzen:
                commits.add(block.get("id"))
            elif statuses and _CLICKUP_WRITE.match(name) and str(tin.get("status", "")).lower() in statuses:
                yield index, ("grenze", "aufgabenstart")


# Nachrichten vom Typ user, die keine Eingabe des Nutzers sind (Benachrichtigungen, Hinweise, Abbruch)
_NOT_PROMPT = ("<task-notification", "<system-reminder", "[Request interrupted", "<local-command-", "Caveat:")


def is_prompt(msg, text):
    """Echte Eingabe des Nutzers (Grenze prompt): kein Meta-Eintrag, keine Zusammenfassung, keine Benachrichtigung."""
    if msg.get("isMeta") or msg.get("isCompactSummary") or msg.get("isSidechain"):
        return False
    stripped = text.lstrip()
    return bool(stripped) and not stripped.startswith(_NOT_PROMPT)


def history(paths, grenzen):
    """Verlauf je Transcript (Liste je Datei), siehe events()."""
    out = []
    for path in paths:
        try:
            with open(path, encoding="utf-8") as fh:
                out.append([event for _, event in events(fh, grenzen)])
        except OSError:
            continue
    return out


def last_timestamp(paths):
    """Jüngster Zeitstempel in den Transcripts (nur das Dateiende wird gelesen)."""
    latest = ""
    for path in paths:
        try:
            with open(path, "rb") as fh:
                fh.seek(0, os.SEEK_END)
                fh.seek(max(0, fh.tell() - 65536))
                tail = fh.read().decode("utf-8", "ignore")
        except OSError:
            continue
        for ts in _TIMESTAMP.findall(tail):
            latest = max(latest, ts)
    return latest


def recent_skills(session, since, agent=""):
    """Skills, die das Skill-Log für die Sitzung nach `since` verzeichnet.

    Claude Code schreibt das Transcript verzögert; ein gerade geladener Skill steht dort oft erst Sekunden später. Das
    Skill-Log schreibt ihn sofort (PostToolUse). Nur Ereignisse nach der letzten Transcript-Zeile zählen – sie liegen
    sicher hinter jeder Grenze, die das Transcript schon kennt. Sekundengenau: dieselbe Sekunde zählt mit. Es zählen
    nur Ereignisse desselben Agenten (Feld agent; '' = Hauptsitzung).
    """
    if not session:
        return []
    directory = setting("SKILL_LOG_DIR", "LOG_DIR") or os.path.join(os.path.expanduser("~"), ".claude", "skill-log")
    since = since[:19]
    found = []
    for path in sorted(glob.glob(os.path.join(directory, "????-??.jsonl")))[-2:]:
        try:
            with open(path, encoding="utf-8") as fh:
                for line in fh:
                    if session not in line or '"skill"' not in line:
                        continue
                    try:
                        entry = json.loads(line)
                    except json.JSONDecodeError:
                        continue
                    if entry.get("event") == "skill" and entry.get("session") == session and entry.get("ok", True) \
                            and (entry.get("agent") or "") == agent and (entry.get("ts") or "")[:19] >= since:
                        found.append(short(entry.get("skill")))
        except OSError:
            continue
    return [s for s in found if s]


def active(histories, grenzen, gilt_bis):
    """Skills, die für eine Regel mit diesen Grenzen gelten: geladen und seither von keiner Grenze verbraucht."""
    result = set()
    for events in histories:
        current = set()
        for kind, value in events:
            if kind == "skill":
                current.add(value)
            elif value in gilt_bis:
                spec = grenzen.get(value) or {}
                used = spec.get("verbraucht", [])
                if used == "*":
                    current = {s for s in current if s in spec.get("ausser", [])}
                else:
                    current -= set(used)
        result |= current
    result.discard("")
    return result


def without_heredocs(command):
    """Shell-Befehl ohne den Inhalt seiner Heredocs: Text darin (Skripte, Commit-Messages) ist kein Befehl."""
    kept, ends = [], []
    for line in command.split("\n"):
        if ends:
            dash, end = ends[0]
            if (line.lstrip("\t") if dash else line) == end:
                ends.pop(0)
            continue
        kept.append(line)
        ends = [(m.group(1) == "-", m.group(3)) for m in _HEREDOC.finditer(line)]
    return "\n".join(kept)


def is_commit(command):
    return bool(_GIT_COMMIT.search(without_heredocs(command)))


def is_merge(command):
    """Merge, der einen Commit erzeugt: gh pr merge, git merge (nicht --ff-only, --abort, --quit, --continue)."""
    return bool(_MERGE.search(_QUOTED.sub("''", without_heredocs(command))))


def _cd(base, segment):
    """Verzeichnis nach einem cd/pushd/popd-Teilbefehl, relativ zum Ausgangsordner ('' = dort); None = unbekannt."""
    match = _CD.match(segment)
    if not match:
        return base
    try:
        args = [a for a in shlex.split(match.group(2)) if not a.startswith("-")]
    except ValueError:
        return None
    if match.group(1) == "popd" or not args or "$" in args[0]:
        return None
    target = os.path.expanduser(args[0])
    if os.path.isabs(target):
        return target
    return None if base is None else os.path.join(base, target)


def heredocs(command):
    """Heredocs eines Shell-Befehls als (shell_davor, öffnende_zeile, stelle, inhalt); shell_davor ist der Shell-Text
    ohne Heredoc-Inhalte bis vor die öffnende Zeile, stelle die Spalte des << in der Zeile."""
    result, kept, ends, open_docs = [], [], [], []
    for line in command.split("\n"):
        if ends:
            dash, end = ends[0]
            if (line.lstrip("\t") if dash else line) == end:
                ends.pop(0)
                result.append(open_docs.pop(0))
            else:
                open_docs[0][3].append(line)
            continue
        found = list(_HEREDOC.finditer(line))
        if found:
            ends = [(m.group(1) == "-", m.group(3)) for m in found]
            open_docs = [("\n".join(kept), line, m.start(), []) for m in found]
        kept.append(line)
    result += open_docs  # Heredoc ohne Ende: Rest gilt als Inhalt
    return [(before, opener, at, "\n".join(body)) for before, opener, at, body in result]


def _interpreter(opener, at):
    """Wohin der Heredoc an Spalte at geht: 'python', 'skript' (anderer Interpreter) oder 'inhalt' (cat > datei)."""
    command = _SEGMENT.split(opener[:at])[-1]
    piped = re.match(r"[^|;&]*\|(?!\|)([^|;&]*)", opener[at:])  # cat <<EOF | python3
    if _PY_COMMAND.search(command) or (piped and _PY_COMMAND.search(" " + piped.group(1))):
        return "python"
    if _REDIRECT.search(command) or re.match(r"\s*(?:cat|tee)\b", command):
        return "inhalt"
    return "skript"


def _runs_with_python(opener, shell):
    """Führt der Befehl die Datei, in die der Heredoc geschrieben wird, mit Python aus?"""
    for target in _REDIRECT.findall(opener) + _TEE.findall(opener):
        name = re.escape(os.path.basename(target.strip("\"'")))
        if name and re.search(r"python[\d.]*(?:\s+-\S+)*\s+\S*" + name + r"\b", shell):
            return True
    return False


def _base_after(shell):
    base = ""
    for segment in _SEGMENT.split(shell):
        base = _cd(base, segment)
    return base


def bash_targets_at(command):
    """Dateien, die ein Shell-Befehl schreibt, als (verzeichnis, ziel): Umleitungen, tee, sed -i, Ziel von cp/mv,
    Schreiben in Skripten (Heredoc an einen Interpreter, python -c). verzeichnis folgt den cd davor
    ('' = Ausgangsordner, None = unbekannt).

    Befund Auswertung 29.10.2026: Früher galt alles ab dem ersten << als Skript – auch Shell-Zeilen nach dem Ende des
    Heredocs (ein gelesenes manifest.json wurde Ziel) und der Inhalt von cat > datei <<EOF (ein open(…, 'w') im Text
    einer Testdatei wurde Ziel)."""
    found = []
    shell = without_heredocs(command)
    base = ""
    for segment in _SEGMENT.split(shell):
        base = _cd(base, segment)
        # Text in Anführungszeichen ist keine Umleitung (grep -v "528 > 340"), außer er ist selbst das Ziel (> "a b")
        unquoted = _QUOTED.sub(lambda m: m.group(0) if _TARGET_BEFORE.search(segment[:m.start()]) else "''", segment)
        targets = _REDIRECT.findall(unquoted) + _TEE.findall(unquoted)
        match = _SED_I.search(segment)
        if match:
            try:
                args = shlex.split(match.group(1))
            except ValueError:
                args = match.group(1).split()
            targets += [a for a in args[1:] if not a.startswith("-")]
        match = _CP_MV.match(segment)
        if match:
            try:
                args = [a for a in shlex.split(match.group(1)) if not a.startswith("-")]
            except ValueError:
                args = []
            if len(args) >= 2:
                targets.append(args[-1])
        found += [(base, t) for t in targets]
    scripts = False
    for before, opener, at, body in heredocs(command):
        kind = _interpreter(opener, at)
        where = _base_after(before + "\n" + opener[:at])
        if kind == "inhalt" and _runs_with_python(opener[:at], shell):
            kind = "python"  # cat > fix.py <<EOF … python3 fix.py
        if kind == "python":
            scripts = True
            found += [(where, t) for t in python_targets(body)]
        elif kind == "skript" and _PY_WRITE.search(body):
            found += [(where, t) for t in script_targets(body)]
    for m in _PY_INLINE.finditer(shell):
        scripts = True
        code = m.group(1) if m.group(1) is not None else m.group(2).replace('\\"', '"')
        found += [(_base_after(shell[:m.start()]), t) for t in python_targets(code)]
    if not scripts and _PY_COMMAND.search(shell) and _PY_WRITE.search(shell):
        found += [(base, t) for t in script_targets(shell)]  # echo "…" | python3, python3 <<< "…"
    clean = []
    for where, target in found:
        target = target.strip("\"'")
        # Ziele mit Shell-Variablen ($S/…) sind hier nicht auflösbar; lieber auslassen als falsch blocken – ebenso
        # relative Ziele nach einem cd, dessen Ziel unbekannt ist
        if not target or target.startswith(("/dev/", "&", "-")) or "://" in target or "$" in target:
            continue
        if where is None and not os.path.isabs(os.path.expanduser(target)):
            continue
        if (where, target) not in clean:
            clean.append((where, target))
    return clean


def script_targets(body):
    """Ziele der Schreibaufrufe in einem Skript (open(…, 'w'), Path(…).write_text, shutil.copy/move, ZipFile(…, 'w')).

    Befund Auswertung 21.10.2026: Früher zählte jeder Dateiname in Anführungszeichen, sobald das Skript irgendwo
    schrieb – Literale im Inhalt (`datei: 'x.html'`) oder Dateien in einem Zip wurden zu Zielen. Ist ein Ziel ein Name,
    gilt das Literal, das ihm zugewiesen wurde; bleibt ein Ziel unbekannt (Ausdruck, Parameter), zählen wie früher alle
    Dateinamen im Skript – lieber ein Fehlalarm als eine Lücke."""
    names = {m.group(1): m.group(3) for m in _ASSIGN.finditer(body)}
    found, unknown = [], False
    for pattern in _WRITE_CALLS:
        for m in pattern.finditer(body):
            literal, name = m.group(2), m.group(3)
            if literal:
                found.append(literal)
            elif name in names:
                found.append(names[name])
            else:
                unknown = True
    for m in _WRITE_NAME.finditer(body):
        if m.group(1) in names:
            found.append(names[m.group(1)])
        elif m.group(1) not in ("sys", "self"):
            unknown = True
    if unknown:
        found += _QUOTED_FILE.findall(body)
    return list(dict.fromkeys(found))


def _literal(node):
    """Pfad als Text aus 'x' oder Path('x'); sonst None."""
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if (isinstance(node, ast.Call) and len(node.args) == 1 and not node.keywords
            and _call_name(node) in ("Path", "PurePath")):
        return _literal(node.args[0])
    return None


def _call_name(call):
    func = call.func
    return func.id if isinstance(func, ast.Name) else func.attr if isinstance(func, ast.Attribute) else ""


def _mode(call, index):
    arg = call.args[index] if len(call.args) > index else next(
        (k.value for k in call.keywords if k.arg == "mode"), None)
    return arg.value if isinstance(arg, ast.Constant) and isinstance(arg.value, str) else None


def python_targets(code):
    """Ziele der Schreibaufrufe in Python-Code, über den Syntaxbaum: Text im Inhalt (Strings, die geschrieben werden)
    ist nie ein Ziel. Ein Name gilt mit allen Literalen, die ihm zugewiesen werden; ein Parameter mit den Literalen, mit
    denen die Funktion aufgerufen wird. Bleibt ein Ziel unbekannt, zählen alle Strings, die ganz ein Dateiname sind –
    lieber ein Fehlalarm als eine Lücke. Nicht lesbarer Code geht an script_targets."""
    try:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")  # ungültige Escapes im Skript (re.compile("\d")) nicht auf stderr
            tree = ast.parse(code)
    except (SyntaxError, ValueError):
        return script_targets(code) if _PY_WRITE.search(code) else []
    names, params, scope, calls = {}, {}, {}, []
    for func in [n for n in ast.walk(tree) if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]:
        params[func.name] = [a.arg for a in func.args.args]
        for node in ast.walk(func):
            scope.setdefault(id(node), func.name)  # innerste Funktion gewinnt nicht, reicht für Patch-Skripte
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign) and len(node.targets) == 1 and isinstance(node.targets[0], ast.Name):
            value = _literal(node.value)
            if value is not None:
                names.setdefault(node.targets[0].id, []).append(value)  # alle Werte: p wird oft neu belegt
        elif isinstance(node, ast.Call):
            calls.append(node)

    def resolve(expr, func, depth=0):
        value = _literal(expr)
        if value is not None:
            return [value]
        if not isinstance(expr, ast.Name) or depth > 3:
            return None
        if expr.id in names:
            return names[expr.id]
        if func and expr.id in params.get(func, []):
            index, values = params[func].index(expr.id), []
            for call in calls:
                if isinstance(call.func, ast.Name) and call.func.id == func:
                    arg = call.args[index] if len(call.args) > index else next(
                        (k.value for k in call.keywords if k.arg == expr.id), None)
                    got = None if arg is None else resolve(arg, scope.get(id(call)), depth + 1)
                    if got is None:
                        return None
                    values += got
            return values or None  # nie mit dem Namen aufgerufen: Ziel unbekannt
        return None

    found, unknown = [], False
    for call in calls:
        name, func, dest = _call_name(call), scope.get(id(call)), None
        owner = call.func.value if isinstance(call.func, ast.Attribute) else None
        if name == "open" and owner is not None and not (isinstance(owner, ast.Name) and owner.id in _OPEN_MODULES):
            mode = _mode(call, 0)  # Path('x').open('w'), p.open('w')
            if mode and any(c in mode for c in "wax+"):
                dest = owner
        elif name in ("open", "ZipFile", "TarFile") and call.args:
            mode = _mode(call, 1)
            if mode and any(c in mode for c in "wax+"):
                dest = call.args[0]
        elif name in ("write_text", "write_bytes") and isinstance(call.func, ast.Attribute):
            dest = call.func.value
            if isinstance(dest, ast.Name) and dest.id in ("sys", "self"):
                continue
        elif name in ("copy", "copy2", "copyfile", "copytree", "move", "replace", "rename") and len(call.args) >= 2:
            owner = call.func.value if isinstance(call.func, ast.Attribute) else None
            if isinstance(owner, ast.Name) and owner.id in ("shutil", "os"):
                dest = call.args[1]
        if dest is None:
            continue
        got = resolve(dest, func)
        if got is None:
            unknown = True
        else:
            found += got
    if unknown:
        found += [n.value for n in ast.walk(tree) if isinstance(n, ast.Constant) and isinstance(n.value, str)
                  and _FILE_NAME.fullmatch(n.value)]
    return list(dict.fromkeys(found))


def bash_targets(command):
    """Dateien, die ein Shell-Befehl schreibt (ohne Verzeichnis, siehe bash_targets_at)."""
    return [target for _, target in bash_targets_at(command)]


def actions(data):
    """Was die Aktion tut: Liste von (aktion, ziel). Ziel ist ein absoluter Pfad oder ''."""
    tool = data.get("tool_name") or ""
    tin = data.get("tool_input") or {}
    cwd = data.get("cwd") or os.getcwd()
    result = []
    if tool in FILE_TOOLS:
        path = tin.get("file_path") or tin.get("notebook_path") or ""
        if path:
            full = os.path.normpath(os.path.join(cwd, os.path.expanduser(path)))
            result.append(("datei", full))
            if tool == "Write" and not os.path.exists(full):
                result.append(("datei:neu", full))
    elif tool == "Bash":
        command = tin.get("command") or ""
        if is_commit(command):
            result.append(("bash:commit", ""))
        if is_merge(command):
            result.append(("bash:merge", ""))
        for where, target in bash_targets_at(command):
            full = os.path.join(cwd, os.path.expanduser(where or ""), os.path.expanduser(target))
            result.append(("bash:schreibt", os.path.normpath(full)))
    elif _CLICKUP_WRITE.match(tool):
        result.append(("mcp:clickup-schreibt", ""))
    return result


def _match(path, patterns):
    return any(fnmatch.fnmatch(path, p.replace("**", "*")) for p in patterns)


def repo_path(path, workdirs):
    """Pfad in einem Arbeitsordner (z. B. Worktree unter <repo>/.claude/worktrees/<name>/) als Pfad im Repo; die Regeln
    gelten dort wie im Repo selbst. workdirs: Ordner-Marker aus regeln.json → arbeitsordner."""
    norm = path.replace("\\", "/")
    for marker in workdirs:
        index = norm.find(marker)
        if index >= 0:
            rest = norm[index + len(marker):].split("/", 1)
            return norm[:index] + ("/" + rest[1] if len(rest) > 1 else "")
    return path


def _applies(rule, act, target, workdirs, always_except):
    """Trifft die Regel diese Aktion auf dieses Ziel (Aktion, Pfad, Ausnahmen; Arbeitsordner wie im Repo)?"""
    if act not in rule.get("aktion", []):
        return False
    if not rule.get("pfad"):
        return True
    where = repo_path(target, workdirs) if target else target
    if not where or not _match(where, rule["pfad"]):
        return False
    return not (_match(where, always_except) or _match(where, rule.get("ausser", [])))


def violations(rules, acts, project, skills, mode):
    """Regeln im gegebenen modus, deren Pflicht-Skill fehlt: Liste von (regel, ziel).

    skills ist eine Menge (gilt für alle Regeln) oder eine Funktion regel → Menge (Grenzen je Regel)."""
    out = []
    always_except = rules.get("ausser_immer", [])
    workdirs = rules.get("arbeitsordner", [])
    for rule in rules.get("regeln", []):
        if rule.get("modus") != mode:
            continue
        if rule.get("projekt", "*") not in ("*", project):
            continue
        have = skills(rule) if callable(skills) else skills
        if any(p in have for p in rule.get("pflicht", [])):
            continue
        base = next((r for r in rules.get("regeln", []) if r.get("id") == rule.get("ergaenzt")
                     and r.get("modus") in ("blocken", "warnen") and r.get("projekt", "*") in ("*", project)), None)
        base_missing = base is not None and not any(
            p in (skills(base) if callable(skills) else skills) for p in base.get("pflicht", []))
        for act, target in acts:
            if not _applies(rule, act, target, workdirs, always_except):
                continue
            # ergänzende Regel: schweigt, wo die Grundregel für dieses Ziel schon meldet
            if base_missing and _applies(base, act, target, workdirs, always_except):
                continue
            out.append((rule, target))
            break
    return out


def log(entries, data, project):
    if not entries:
        return
    directory = setting("SKILL_LOG_DIR", "LOG_DIR") or os.path.join(os.path.expanduser("~"), ".claude", "skill-log")
    now = datetime.datetime.now(datetime.timezone.utc)
    os.makedirs(directory, exist_ok=True)
    agent = agent_of(data)
    with open(os.path.join(directory, now.strftime("%Y-%m") + ".jsonl"), "a", encoding="utf-8") as fh:
        for entry in entries:
            if agent:
                entry = dict(entry, agent=agent)
            fh.write(json.dumps(dict({
                "v": 1, "ts": now.strftime("%Y-%m-%dT%H:%M:%SZ"),
                "host": setting("SKILL_LOG_HOST", "LOG_HOST") or socket.gethostname(),
                "session": data.get("session_id"), "event": "guard", "project": project,
                "tool": data.get("tool_name"), "tool_use_id": data.get("tool_use_id"),
            }, **entry), ensure_ascii=False) + "\n")


def plugin_names(path=None):
    """Skill → Name mit Plugin-Präfix (work:code-erstellen) aus der marketplace.json des Plugins. Als work-hooks gibt es
    keine (die Skills kommen dann aus claude.ai) – dann bleibt der Name ohne Präfix."""
    path = path or os.path.join(HERE, "..", "..", "..", ".claude-plugin", "marketplace.json")
    try:
        with open(path, encoding="utf-8") as fh:
            data = json.load(fh)
    except (OSError, json.JSONDecodeError):
        return {}
    names = {}
    for entry in data.get("plugins", []):
        for skill in entry.get("skills", []) if isinstance(entry.get("skills"), list) else []:
            names[os.path.basename(str(skill).rstrip("/"))] = f"{entry.get('name')}:{os.path.basename(str(skill).rstrip('/'))}"
    return names


def message(found, names=None):
    names = plugin_names() if names is None else names
    lines = []
    for rule, target in found:
        where = f" ({target})" if target else ""
        lines.append(f"- Regel „{rule['id']}“{where}: {rule.get('beschreibung', '')}. "
                     f"Zuständig: {', '.join(names.get(p, p) for p in rule['pflicht'])}")
    return "\n".join(lines)


def plugin_stand(root=None):
    """Stand des Plugins, aus dem Wächter und Regeln kommen: im Plugin-Cache der Ordnername (Commit), sonst ''."""
    name = os.path.basename(os.path.abspath(root or os.path.join(HERE, "..", "..", "..")))
    return name[:7] if re.fullmatch(r"[0-9a-f]{7,40}", name) else ""


def stand_hinweis(stand=None):
    stand = plugin_stand() if stand is None else stand
    if not stand:
        return ""
    return (f"Die Regeln stammen aus dem Plugin-Stand {stand}. Ist der Skill geladen und die Blockade trotzdem da, "
            "läuft die Sitzung womöglich mit einem alten Stand: `/plugin update` und Claude neu starten. ")


# Ohne Präfix ordnet Claude Code den Namen womöglich einer abgeschalteten Kopie zu (skillOverrides, z. B. die Fassung
# aus claude.ai) – Befund 09.10.2026: „Skill code-erstellen is disabled for model invocation“.
NAME_HINWEIS = ("Den Skill mit dem vollen Namen samt Präfix laden, wie er in der Skill-Liste steht (z. B. "
                "work:code-erstellen) – ohne Präfix kann eine abgeschaltete Kopie getroffen werden. ")


def decide(data, rules=None, skills=None):
    """Gibt (exit_code, stdout, stderr, log_entries) zurück. Reine Funktion für Tests."""
    rules = rules if rules is not None else load_rules()
    event = data.get("hook_event_name")
    mode = {"PreToolUse": "blocken", "PostToolUse": "warnen"}.get(event)
    acts = actions(data)
    if not mode or not acts:
        return 0, "", "", []
    project = project_of(data.get("cwd"))
    if skills is None:
        grenzen = rules.get("grenzen", {})
        agent = agent_of(data)
        own, main = transcripts(data)
        hist = history(own, grenzen)
        # ein Subagent ohne eigenes Transcript (noch nicht geschrieben): alle seine Skill-Ereignisse im Log zählen
        if own or agent:
            recent = recent_skills(data.get("session_id"), last_timestamp(own) if own else "", agent)
            if recent:
                hist = hist + [[("skill", name) for name in recent]]
        inherited = history(main, grenzen)
        skills = lambda rule: active(hist + (inherited if rule.get("erbt_hauptsitzung") else []),  # noqa: E731
                                     grenzen, rule.get("gilt_bis", []))
    found = violations(rules, acts, project, skills, mode)
    if not found:
        return 0, "", "", []
    entries = [{"regel": r["id"], "entscheidung": "geblockt" if mode == "blocken" else "gewarnt",
                "ziel": t[-200:], "pflicht": r["pflicht"],
                "aktiv": sorted(skills(r) if callable(skills) else skills)} for r, t in found]
    text = message(found)
    if mode == "blocken":
        err = ("Skill-Wächter: Diese Änderung braucht einen geladenen Skill, der dafür zuständig ist.\n" + text +
               "\nLade den passenden Skill mit dem Skill-Werkzeug und wiederhole dann die Aktion – auch wenn er früher in "
               "der Sitzung schon geladen war: Nach einem Commit, einem Aufgabenstart oder einer neuen Aufgaben-ID gilt "
               "er als verbraucht, und ein Subagent muss ihn selbst laden (die Hauptsitzung zählt für ihn nicht). " +
               NAME_HINWEIS + stand_hinweis() +
               "Ist die Regel hier falsch, sag es dem Nutzer (wird bei der Skill-Auswertung nachgeschärft).")
        return 2, "", err, entries
    ctx = ("Skill-Wächter (Hinweis): Diese Aktion lief ohne den zuständigen Skill.\n" + text +
           "\nLade den passenden Skill, bevor du weitermachst, damit sein Ablauf (Profil, Tests, Commit) gilt. " + NAME_HINWEIS)
    out = json.dumps({"hookSpecificOutput": {"hookEventName": "PostToolUse", "additionalContext": ctx}},
                     ensure_ascii=False)
    return 0, out, "", entries


def main():
    if setting("SKILL_GUARD", "SKILL_GUARD").lower() in OFF:
        return 0
    try:
        # Claude Code schickt UTF-8; unter Windows wäre sys.stdin sonst cp1252 (Befund desktop-pc 21.10.2026)
        raw = sys.stdin.buffer.read().decode("utf-8", "replace")
        data = json.loads(raw) if raw.strip() else {}
        code, out, err, entries = decide(data)
        try:
            log(entries, data, project_of(data.get("cwd")))
        except Exception as exc:  # noqa: BLE001 – das Protokoll darf die Entscheidung nicht verhindern
            sys.stderr.write(f"skill_guard log: {exc}\n") if code == 0 else None
        if out:
            sys.stdout.write(out)
        if err:
            sys.stderr.write(err)
        return code
    except Exception:  # noqa: BLE001 – ein Fehler im Wächter darf nie blockieren
        return 0


if __name__ == "__main__":
    sys.exit(main())
