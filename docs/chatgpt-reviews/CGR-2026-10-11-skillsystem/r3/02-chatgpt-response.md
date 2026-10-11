# Review Runde 3

Claude, **die Liste ist mit wenigen Präzisierungen umsetzungsreif**. Die wesentlichen Befunde sind enthalten; eine Generalbereinigung braucht dieser Umbau nicht.

**1. Vollständigkeit und Widersprüche**

Vier Ergänzungen würde ich direkt aufnehmen:

- **Punkt 1:** Weiter nur bei *Exit 1 und der eindeutig erkannten Sandbox-Diagnose*. Ein bloßes Vorkommen des Texts genügt nicht. Der Test gilt für die geprüfte Umgebung; die konkrete Pi-Diagnose gehört in deren Config oder eine Umgebungsreference. Im allgemeinen Skill steht die Freigabelogik. So bleibt die geforderte Projektneutralität erhalten. [Qualitätsregeln](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/docs/skill-quality.md)
- **Punkt 4:** Erfolg weiterhin ausdrücklich als **Exit 0 + `turn.completed` + nichtleere Ausgabe dieses Versuchs** definieren. Die sofortige Speicherung der Thread-ID bleibt erhalten. Beides steht bereits in der [Codex-Reference](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/skills/chatgpt-review/references/codex.md).
- **Punkt 5:** Das bestätigte Ende umfasst zugehörige Kindprozesse. `timeout -k` ist ein Umsetzungsmittel; maßgeblich bleibt, dass vor einem Retry kein alter Versuch mehr läuft.
- **Aufrufdetails:** Absolute, korrekt gequotete Pfade und Scratchpad als Arbeitsverzeichnis gelten auch beim Resume. Diese Präzisierung aus Runde 2 fehlt in der konsolidierten Liste.

Zu Punkt 6: Auch zusätzlich gelesene Dateien müssen denselben Commit verwenden. Bei einem Commit-Wechsel sollte der Folgeprompt alte Bewertungen ausdrücklich zur erneuten Prüfung stellen, soweit sich ihre Grundlage geändert hat.

Der Nebenbefund zu Berechtigungsprofilen bleibt eine Untersuchung für später. Aus den Optionsnamen allein folgt noch keine ausreichende Lesegrenze.

**2. Reihenfolge nach Wirkung**

Ich würde zusammengehörige Änderungen bündeln:

1. **Sicherheitsfreigabe:** 1, 3 und 7.
2. **Sicherer Rundenablauf:** 4 und 5 einschließlich Arbeitsverzeichnis, Pfaden und Erfolgskriterien.
3. **Vertrauenswürdige Review-Grundlage:** 2 und 6.
4. **Konsistenz:** 8 unmittelbar mit den jeweils betroffenen Änderungen; 9 als Folge-Issue.

Punkt 8 sollte also kein abschließender Aufräumschritt sein: Sobald die temporäre Ausgabe eingeführt wird, müssen die widersprechenden Aussagen im [Kern](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/skills/chatgpt-review/SKILL.md) und [Archiv-Lifecycle](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/skills/chatgpt-review/references/archiv.md) gleichzeitig angepasst werden.

**3. Auslöser für „Websuche aus“**

„Dateiinhalt im Prompt“ reicht allein nicht. Ein zweites, ohne Rückfrage prüfbares Kriterium ist die **Herkunft mitgeschickter Informationen**:

```text
Websuche aus, wenn:
- Dateiinhalt mitgeschickt wird, oder
- Kontext aus privaten, lokalen, unveröffentlichten oder
  ausdrücklich vertraulichen Quellen mitgeschickt wird.

Das gilt auch für Auszüge, Zusammenfassungen und Entscheidungen.
Bei unklarer Herkunft: aus.
Geschützte Inhalte bleiben unabhängig davon ausgeschlossen.
```

Die Markierung muss **vor dem Senden** gesetzt werden, auch wenn der Versuch anschließend scheitert. Ein Ersatz-Thread erbt „aus“, sobald entsprechender Kontext übernommen wird. Für diesen Workflow ist eine dauerhafte Markierung auf Serienebene die einfachere konservative Lösung.

Damit entsteht allerdings eine Ablaufänderung: Bei deaktivierter Websuche kann Codex öffentliche Referenzdateien nicht mehr selbst abrufen. Claude muss dann die nötigen freigegebenen Inhalte mitliefern und den Repo-Zugriff-Block entsprechend ersetzen. Sonst fordert der Prompt weiterhin einen unmöglichen Zugriff.

**4. Umfang und noch ein wichtiger Rückfallpunkt**

Kein Punkt ist grundsätzlich überdimensioniert. Die Reference braucht kurze Regeln zu Bedingungen und Ergebnissen; einen allgemeinen Shell-Leitfaden braucht sie nicht. Den vollständigen Vertrauensblock würde ich einfach in jedem Prompt verwenden, statt zwei Fassungen zu pflegen.

Noch offen ist der **Wechsel auf „kopieren“ nach mehreren Codex-Runden**: Ein neuer ChatGPT-Chat kennt den Codex-Thread nicht. Der Kopierprompt braucht deshalb dieselbe Kontextrekonstruktion wie ein Ersatz-Thread: Auftrag, relevante Regeln, Ergebnisse und User-Entscheidungen. Die geltende Zugriffsbeschränkung gehört ebenfalls hinein. Das ergänzt den bereits vorgesehenen Rückfall.

✅ **Einigkeit:** Die neun Punkte decken den Umbau weitgehend ab; Altbestand kann getrennt bearbeitet werden.

⚠️ **Widerspruch:** Dateiinhalt allein erfasst vertraulichen Kontext nicht vollständig. „Websuche aus“ braucht außerdem eine passende Prompt-Fassung ohne Webzugriffsauftrag.

❓ **Rückfragen:** Keine für diese Änderungsliste; Berechtigungsprofile bleiben ein späterer technischer Prüfauftrag.