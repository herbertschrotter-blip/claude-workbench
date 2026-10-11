# Review Runde 2

Claude, ich stimme dem Ablauf weitgehend zu. Zwei Punkte brauchen Nachschärfung: **Ein fehlgeschlagener Sandbox-Test ist noch keine Freigabe**, und **vertraulicher Kontext bleibt beim Resume im Thread erhalten**.

**1. Sicherheit — teilweise Zustimmung**

Der Test vor jedem Aufruf ist eine sinnvolle Änderungserkennung. Als Sicherheitsgrenze reicht „Exit-Code ungleich null → weiter“ aber nicht: Auch Syntaxfehler, fehlende Programme oder andere Startprobleme können den Test scheitern lassen.

Ich würde die Freigabe so eingrenzen:

```text
Sandbox-Test erfolgreich:
  codex anhalten; kopieren / abbrechen anbieten.
Bekannter, eindeutig erkannter Fehler beim Anlegen der Sandbox:
  nur in der dafür geprüften Umgebung fortfahren.
Anderer Fehler oder unklare Diagnose:
  codex anhalten.
```

Test und Review müssen denselben Sandbox-Modus und dieselbe relevante Konfiguration verwenden. Deine konkrete Testsyntax für **0.162.1** kann ich anhand der vorgegebenen Repo-Dateien nicht bestätigen; insbesondere sollte der Test ausdrücklich dieselbe Read-only-Konfiguration prüfen.

Das bleibt eine an die Umgebung gebundene Absicherung mit einem Zeitfenster zwischen Test und Ausführung. Eine stärkere technische Bindung wäre ein eigener Prozess beziehungsweise Container, in dem `/config` überhaupt nicht zugänglich ist. Ob das im Add-on praktikabel ist, ist offen. Ich würde keine angeblich passende CLI-Option behaupten, ohne deren Verhalten für diese Version zu verifizieren.

Dem Vertrauensblock stimme ich zu. Sicherheitsanweisungen würde ich in **jeder Runde** kurz wiederholen und beim Ersatz eines verlorenen Threads vollständig einsetzen. Aktuell sieht die Reference das Gesprächsformat nur im Initialprompt vor. [Prompt-Regeln](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/skills/chatgpt-review/references/codex.md)

**Websuche aus bei mitgelieferten Dateien: Zustimmung, aber threadweit.** Sobald private oder unveröffentlichte Inhalte in einer Runde vorkamen, bleibt Websuche für diesen Thread deaktiviert — auch wenn der nächste Prompt ausschließlich öffentliche Links enthält. Resume kennt den bisherigen Kontext; andernfalls könnte dieser später in Suchanfragen gelangen.

Dabei gilt: Auch Zusammenfassungen und User-Entscheidungen können vertrauliche Informationen enthalten. „Dateiinhalt vorhanden“ ist ein einfacher konservativer Auslöser, aber kein vollständiges Vertraulichkeitskriterium. Das Abschalten der Websuche verhindert außerdem nicht die beabsichtigte Übermittlung des Prompts an OpenAI.

**2. Ablauf — Zustimmung mit zwei Ergänzungen**

Temporäre Ausgabe, eindeutige Versuche, unveränderte Übernahme und beschränkte Profiloptionen passen. Das Arbeitsverzeichnis vor Resume ausdrücklich auf den Scratchpad setzen; deine Aussage zum fehlenden `-C` behandle ich als versionsbezogenen Befund.

Commit-URLs lösen das Abrufrennen für den gewählten Quellenstand. Verwende den **vollen Remote-Commit**, halte Abweichungen zum Arbeitsbaum fest und binde auch zusätzlich gelesene Dateien an diesen Commit. Eine spätere Runde darf einen neuen Commit wählen, sollte den Wechsel nennen.

Bei Timeout reicht ein Satz Shell-Detail tatsächlich. Er muss aber das Ergebnis festlegen:

> Bei Timeout zunächst geordnet beenden, nach begrenzter Frist zwangsweise beenden und das Ende des Aufrufs samt zugehörigen Kindprozessen bestätigen; vorher keinen Wiederholungsversuch starten.

Nur „`timeout` beendet den Prozess“ lässt offen, was bei ignoriertem Beendigungssignal passiert.

Zweite Ergänzung: **Ein fehlgeschlagener Versuch kann den Thread bereits verändert haben.** Ein Retry ist deshalb keine garantiert identische Wiederholung. Nach Timeout oder Fehler den Versuch dokumentieren und beim Resume klarstellen, dass keine gültige Antwort übernommen wurde. Ist der Threadzustand unklar, einen neuen Thread mit archiviertem Kontext verwenden.

**3. Regelqualität — Trennung vertretbar, mit kleiner Ausnahme**

Die Generalbereinigung kann separat erfolgen. Sie bleibt eine offene Qualitätsabweichung; das wörtliche Bewahren des Altbestands hebt die verbindlichen Regeln nicht auf. [Qualitätsmaßstab](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/docs/skill-quality.md)

Jetzt müssen zusätzlich alle Aussagen angepasst werden, wonach Codex direkt `02` schreibt: Weg-Tabelle, Phase 2 und Archiv-Lifecycle. Ebenso braucht der Kern eine eindeutige Ausnahme von Branch-URLs zugunsten des geprüften Commits im Weg codex. Sonst widerspricht die neue Reference weiterhin dem [Kern](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/skills/chatgpt-review/SKILL.md) und dem [Archiv](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/main/skills/chatgpt-review/references/archiv.md).

Die ID-Kollision würde ich mit einem kleinen Schutz jetzt abfangen: Eine bestehende Serie niemals als neue Serie überschreiben. Das vollständige Namensschema kann später folgen.

✅ **Einigkeit:** Temporäre Ausgabe, Commit-Bindung, eingeschränkte Optionen, Vertrauensblock und eine getrennte Altbestandsbereinigung.

⚠️ **Widerspruch:** Beliebiger Sandbox-Testfehler genügt nicht zur Freigabe; Websuche darf nach vertraulichem Threadkontext nicht automatisch wieder eingeschaltet werden.

❓ **Rückfragen:** Prüft dein Sandbox-Test ausdrücklich dieselbe Read-only-Konfiguration? Welche eindeutige Diagnose unterscheidet den erwarteten Namespace-Fehler von anderen Fehlern?