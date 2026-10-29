# Skill-Wächter v1

Skills zünden auf den Wortlaut des Prompts. Bei „weiter“, „ja“ oder „passt“ steht dort nichts, woran ein Skill
erkennen könnte, dass er gebraucht wird; die Entscheidung fällt erst bei der Aktion. Der Skill-Wächter prüft deshalb an
der Aktion: Ändert Claude Code, Mockups, Doku, Skills, ClickUp oder committet, muss der zuständige Skill in der Sitzung
geladen sein. Die Regeln dafür sind lernbar: skill-auswertung schärft sie anhand des Skill-Logs nach. Werkzeuge:
`plugins/work-hooks/hooks/`.

## Inhalt

- Ablauf
- Regeln
- Grenzen für geladene Skills
- Lernen
- Einrichtung
- Grenzen

## Ablauf

| Hook | Regeln | Wenn der Pflicht-Skill fehlt |
|---|---|---|
| `PreToolUse` | `modus: blocken` | Aktion wird abgelehnt (Exit 2); Claude sieht die Begründung, lädt den Skill und wiederholt die Aktion |
| `PostToolUse` | `modus: warnen` | Aktion läuft; Claude bekommt danach einen Hinweis (`additionalContext`) und lädt den Skill für die weiteren Schritte |

- Geladene Skills liest der Wächter aus dem Transcript der Sitzung (Skill-Aufrufe, Slash-Befehle und nach einer
  Compaction der Anhang `invoked_skills`). Ein geladener Skill gilt bis zur nächsten Grenze, die ihn verbraucht
  (Abschnitt „Grenzen für geladene Skills“), sonst bis zum Sitzungsende. Claude Code schreibt das Transcript mit
  einigen Sekunden Verzögerung; deshalb zählen zusätzlich die Skill-Ereignisse dieser Sitzung aus dem Skill-Log, die
  neuer sind als die letzte Transcript-Zeile (Befund Auswertung 08.10.2026: drei Fehlalarme 4–7 s nach dem Laden).
  Seit 21.10.2026 (Befund Lumora/PhotoViewer V3: Agenten lieferten fast allen Code, code-erstellen war nur zweimal
  am Anfang der Hauptsitzung geladen) erben Subagenten die Skills der Hauptsitzung **nicht** mehr: Ein Agent muss den
  Pflicht-Skill selbst laden. Erkannt wird er am Hook-Feld `agent_id` (ältere Fassungen: Transcript
  `<sitzung>/subagents/agent-<id>.jsonl`); gezählt werden dann nur sein eigenes Transcript und Skill-Log-Ereignisse
  mit seiner `agent`. Eine Regel mit `erbt_hauptsitzung: true` zählt die Hauptsitzung mit; heute setzt keine Regel das.
- Pfade in Arbeitsordnern (`regeln.json` → `arbeitsordner`, heute `/.claude/worktrees/`: Agenten- und
  Zusammenbau-Worktrees) prüft der Wächter wie den entsprechenden Pfad im Repo:
  `<repo>/.claude/worktrees/agent-x/src/A.cs` gilt als `<repo>/src/A.cs`. So fallen Worktrees nicht unter die
  Ausnahme `*/.claude/*`, die für Einstellungen, Memory, Plugin-Cache und Skill-Log bleibt.
- Die Meldung nennt die zuständigen Skills mit Plugin-Präfix (`work:code-erstellen`, aus der `marketplace.json` des
  Plugins). Ohne Präfix kann Claude Code eine per `skillOverrides` abgeschaltete Kopie treffen (Befund 09.10.2026).
- Jede Entscheidung landet als Ereignis `guard` im Skill-Log (`docs/skill-log-v1.md`): `regel`, `entscheidung`
  (`geblockt`/`gewarnt`), `tool`, `tool_use_id`, `ziel`, `pflicht`, `aktiv`.
- Ein Fehler im Wächter blockiert nie (Exit 0). `SKILL_GUARD=aus` oder die Plugin-Option `skill_guard` schaltet ihn ab.

## Regeln

Datei `plugins/work-hooks/hooks/regeln.json`, für alle Rechner gleich (kommt mit dem Plugin-Update). Felder je Regel:

| Feld | Inhalt |
|---|---|
| `id` | eindeutiger Name |
| `beschreibung` | Satz, den Claude in der Meldung sieht |
| `aktion` | `datei` (Edit/Write), `datei:neu` (Write auf eine Datei, die es noch nicht gibt), `bash:schreibt` (Umleitung, `tee`, `sed -i`, Ziel von `cp`/`mv`, Schreiben im Heredoc an einen Interpreter und in `python -c`), `bash:commit` (Text in Heredocs zählt nicht), `bash:merge` (`gh pr merge`, `git merge` außer `--ff-only`/`--abort`; Text in Heredocs und Anführungszeichen zählt nicht), `mcp:clickup-schreibt` |
| `pfad` / `ausser` | Muster wie `*.py`, `*/mockups/*` (fnmatch auf den absoluten Pfad, in Arbeitsordnern auf den Pfad im Repo; `*` passt auch über `/`). Dazu gilt `ausser_immer` für alle Regeln (Scratchpad, `/tmp`, `.claude/`, `.git/`) |
| `projekt` | `*` oder eine Projekt-ID aus dem Skill-Profil der `CLAUDE.md` |
| `pflicht` | Skills, von denen einer geladen sein muss |
| `modus` | `blocken`, `warnen` oder `aus` |
| `gilt_bis` | Grenzen, nach denen ein vorher geladener Skill für diese Regel nicht mehr zählt (`commit`, `aufgabenstart`, `task_id`, `prompt`) |
| `ergaenzt` | optional: `id` einer Grundregel; die Regel meldet nur, wenn die Grundregel erfüllt ist (sonst meldet schon diese) |
| `erbt_hauptsitzung` | optional, Standard `false`: Skills der Hauptsitzung zählen auch für Subagenten |
| `herkunft` | Befund oder Entscheidung, aus der die Regel stammt |
| `stand` | `seit`, `treffer`, `fehlalarm`, `zuletzt` – nachgerechnet von skill-auswertung; `rueckblick` = Abspielen der Regeln gegen alte Transcripts |

Startregeln (07.10.2026): `code` und `mockup` blocken; `skills`, `doku`, `clickup`, `commit` warnen. Nach dem Rückblick
über 29.09.–07.10. (erste Lernrunde): `doku` blockt (89 Treffer, 0 Fehlalarme), `clickup` erlaubt auch projekt-anlegen
und skill-neu (Fehlalarm beim Anlegen von Issue-Listen). Der Rückblick steht je Regel unter `stand.rueckblick`.

## Grenzen für geladene Skills

Seit 08.10.2026 (Entscheidung Herbert, Befund ha-baustelle `bc267f1c`: sechs Aufgaben mit nur einem code-erstellen am
Anfang, alle Commits ohne git-commit-helper, neue Docs ohne doc-pflege) gilt ein Skill nicht mehr bis Sitzungsende.
`regeln.json` → `grenzen` legt fest, was eine Grenze ist und welche Skills sie verbraucht:

| Grenze | Erkannt an | verbraucht |
|---|---|---|
| `commit` | erfolgreicher `git commit` (Bash, Tool-Ergebnis ohne Fehler) | code-erstellen, doc-pflege, git-commit-helper, skill-pflege, skill-neu, skill-auswertung |
| `aufgabenstart` | ClickUp-Schreibaufruf setzt eine Aufgabe auf `in development` bzw. `in progress` | alle außer tracker |
| `task_id` | Nutzer-Nachricht nennt eine Aufgabe oder ein Ticket (`BSM-026`, `Bsm 026`, `FE-0012`; Muster in `regeln.json`) | alle außer tracker |
| `prompt` | neue Eingabe des Nutzers; nicht: Tool-Ergebnisse, `isMeta`, Zusammenfassung nach Compaction, `<task-notification>`, `<system-reminder>`, „[Request interrupted…“ | code-erstellen, ticket, skill-neu, skill-pflege, projekt-anlegen |

Die Grenze `prompt` (seit 21.10.2026) nutzt nur die Warnregel `code-prompt`: dieselben Pfade wie `code`, `ergaenzt:
code`, Start `warnen`. Sie meldet, wenn Code nach einer neuen Eingabe geändert wird, ohne dass code-erstellen danach neu
geladen wurde – gegen Aufgabenwechsel ohne neuen Durchlauf. Fehlalarm-Risiko hoch: auch jedes „weiter“ in derselben
Aufgabe zählt als neue Eingabe. Hochstufen erst nach Auswertung (mindestens 10 Treffer ohne Fehlalarm).

Für eine Regel zählen nur Skills, die nach der letzten Grenze aus ihrem `gilt_bis` geladen wurden. Ein nach der Grenze
neu geladener Skill gilt wieder. Eine Compaction holt verbrauchte Skills nicht zurück: Der Anhang `invoked_skills`
zählt nur Skills, die der Verlauf der Datei noch nicht kennt. Die Meldung bei einer Blockade sagt Claude, dass ein früher
geladener Skill nach einer Grenze neu geladen werden muss.

Dazu seit 08.10.2026: Regel `doku-neu` (neue Datei unter `docs/` braucht doc-pflege bzw. einen Skill, der Doku selbst
anlegt; code-erstellen reicht nicht – Änderungen an bestehender Doku wie Bauplan oder CHANGELOG bleiben unter `doku`
mit code-erstellen erlaubt) und `commit` blockt: git-commit-helper oder ticket, dazu skill-pflege, skill-neu und
skill-auswertung, die laut ihrem Ablauf selbst committen.

Rückblick 08.10.2026 (alle Transcripts seit 29.09., nach jeder Blockade gilt der Skill als nachgeladen): Prüffall
`bc267f1c` 0 → 43 Blockaden (20 Commit, 21 Code nach Commit, 1 doku, 1 doku-neu); ha-baustelle gesamt rund 300,
/config 69, Skill-Repo-Sitzungen 47 (davon diese Sitzung 6).

## Lernen

Bei „skills auswerten“ (Skill skill-auswertung) kommen die `guard`-Ereignisse dazu. Vorschläge – jeweils nur mit
Freigabe von Herbert in `regeln.json` übernehmen:

| Befund | Vorschlag |
|---|---|
| Lücke: Aktion ohne zuständigen Skill, die keine Regel erfasst (Transcript, Report „aktiv“) | neue Regel, Start `warnen` |
| Fehlalarm: Regel griff, der Skill war nicht nötig (Herbert widerspricht, Claude lädt den Skill nicht, Aufgabe gehört klar zu einem anderen Skill) | Ausnahme in `ausser`, weiterer Skill in `pflicht` oder `modus` zurückstufen |
| bewährt: mindestens 10 Treffer ohne Fehlalarm | `warnen` → `blocken` |
| tot: 30 Tage kein Treffer | prüfen, ggf. `aus` |

Nach jeder Auswertung `stand` aktualisieren und `regeln.json` mit der Auswertung committen.

## Einrichtung

Über das Plugin `work` aus dem Marketplace `workbench` (dieses Repo), je Rechner einmal:

```
claude plugin marketplace add herbertschrotter-blip/claude-workbench
claude plugin install work@workbench
```

Das Plugin bringt die Hooks für Skill-Log und Wächter mit (eingetragen im Plugin-Eintrag `work` in `.claude-plugin/marketplace.json`, Skripte unter `plugins/work-hooks/hooks/`). Den Rechnernamen im Log setzt
die Plugin-Option `log_host` (`/plugin configure work@workbench` oder `--config log_host=<name>` bei der Installation)
oder `env` in `~/.claude/settings.json`: `"env": { "SKILL_LOG_HOST": "<name>" }`; die Variable hat Vorrang. Ohne beides
steht der Hostname im Log, im HA-Add-on eine Container-ID. Abschalten je Rechner: Optionen `skill_log` bzw.
`skill_guard` oder `SKILL_LOG=0` bzw. `SKILL_GUARD=0`. Einrichten in einem Zug: `tools/install.sh` bzw. `tools/install.ps1`
(README, Abschnitte „Schnellstart“ und „Installation im Detail“). Updates:
`claude plugin marketplace update workbench`, dann `claude plugin update work@workbench`, oder Auto-Update einschalten. Rechner, auf denen die Skills aus claude.ai kommen und `skillOverrides` nicht greift (Claude-Desktop-App), installieren statt `work` und `skill-workshop` nur `work-hooks@workbench` (Hooks ohne Skills); nie `work` und `work-hooks` zusammen.

Ohne Plugin (alter Weg) trägt man die Hooks von Hand in `~/.claude/settings.json` ein; Block `hooks`, neben den Hooks des
Skill-Logs. `<befehl>`:
- Linux: `SKILL_LOG_HOST=<name> python3 <repo>/plugins/work-hooks/hooks/skill_guard.py`
- Windows (PowerShell): `$env:SKILL_LOG_HOST='<name>'; python <repo>\plugins\work-hooks\hooks\skill_guard.py`, dazu im Hook
  `"shell": "powershell"`

```json
"PreToolUse":  [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }],
"PostToolUse": [{ "matcher": "Edit|Write|MultiEdit|NotebookEdit|Bash|mcp__.*[Cc]lick[Uu]p.*", "hooks": [{ "type": "command", "command": "<befehl>", "timeout": 10 }] }]
```

Beides nie zugleich: Hooks von Hand und Plugin würden doppelt prüfen und loggen. Auf dem Smartphone nichts – dort läuft Claude Code
nicht selbst, sondern steuert per Remote Control die Sitzung auf dem HA. Im Cowork-Chat und auf claude.ai gibt es keine
Hooks.

Tests: `python3 -m unittest plugins/work-hooks/hooks/test_skill_guard.py` (die Mechanik läuft gegen feste Modi, die echte
`regeln.json` wird nur auf Gültigkeit geprüft – so bricht kein Test, wenn eine Regel hochgestuft wird)

## Grenzen

- Schreiben per Shell erkennt der Wächter über Muster. Ziele mit Shell-Variablen (`$S/datei`) lässt er aus. Relative
  Ziele löst er gegen das Verzeichnis nach dem letzten `cd`/`pushd` davor auf; ist dessen Ziel unbekannt (`cd $X`,
  `cd -`, `popd`), lässt er sie aus. Im Python-Heredoc zählen alle genannten Dateien, auch gelesene, sobald das Skript
  schreibt. Seit 21.10.2026 (Auswertung: Fehlalarme bei Zip-Skripten und Literalen im geschriebenen Inhalt) zählen im
  Skript nur die Ziele von Schreibaufrufen (`open(…, 'w')`, `Path(…).write_text`, `shutil.copy`/`move`,
  `ZipFile(…, 'w')`), bei einem Namen das ihm zugewiesene Literal; bleibt ein Ziel unbekannt (Ausdruck, Parameter),
  zählen wie früher alle Dateinamen im Skript. Seit 29.10.2026 (Auswertung: Fehlalarme durch gelesene Dateien nach dem
  Heredoc und durch Text im geschriebenen Inhalt): Shell-Zeilen nach dem Ende eines Heredocs zählen als Shell, Text in
  Anführungszeichen ist keine Umleitung; der Inhalt von `cat > datei <<EOF` ist kein Code. Python-Heredocs und
  `python -c` liest der Wächter über den Syntaxbaum: Strings im Inhalt sind nie ein Ziel, ein Name gilt mit allen ihm
  zugewiesenen Literalen, ein Funktionsparameter mit den Literalen der Aufrufe (`rep('CLAUDE.md', …)`); bleibt ein
  Ziel unbekannt, zählen alle Strings, die ganz ein Dateiname sind. Nicht lesbarer Python-Code und andere
  Interpreter laufen weiter über die Muster. Ein Skript, das im selben Befehl per `cat > x.py <<EOF` geschrieben und mit
  `python3 x.py` ausgeführt wird, liest er wie einen Python-Heredoc. Bekannte Lücke: Ein einzelner Apostroph ohne
  Anführungszeichen (`echo it\'s > a.yaml 'z'`) paart sich mit einem späteren und blendet die Umleitung dazwischen aus.
- Ein Skript, das per Write im Scratchpad liegt und dann mit `python3 <datei>` läuft, sieht der Wächter nicht
  (Auswertung 21.10.2026, belegt; Regel dafür vorerst nicht umgesetzt).
- Hooks lesen ihre Eingabe als UTF-8 (unter Windows sonst cp1252: Umlaute im Log doppelt kodiert, Befund desktop-pc
  21.10.2026; ältere Einträge repariert die Auswertung beim Lesen). Die Projekt-ID im Worktree kommt aus dem Repo, nicht
  aus dem Ordnernamen des Worktrees.
- Die Blockmeldung nennt den Plugin-Stand (Commit aus dem Ordnernamen im Plugin-Cache). Blockt der Wächter, obwohl der
  Skill geladen ist, läuft die Sitzung womöglich mit einem alten Stand: `/plugin update` und Claude neu starten.
- Dateien, die ein Build-Skript erzeugt (z. B. ein gebündeltes Mockup), sieht der Wächter nicht.
- Hooks feuern laut Doku von Claude Code auch in Subagenten und tragen dann `agent_id` und `agent_type`. Ob
  `transcript_path` dort auf die Hauptsitzung oder den Agenten zeigt, ist nicht beschrieben; der Wächter baut den Pfad
  zum Transcript des Agenten deshalb selbst. Ohne `agent_id` und ohne Agenten-Pfad ist ein Subagent nicht von der
  Hauptsitzung zu unterscheiden.
- Der Wächter prüft, ob der Skill geladen ist, nicht, ob sein Ablauf befolgt wurde (Impact Check, Selbst-Review,
  Commit-Profil).
- Warnen geht nur nach der Aktion (`PostToolUse`); vor der Aktion kann ein Hook Claude keinen Hinweis geben.
