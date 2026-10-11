# Runde 2 – Einschätzung Claude

## Zustimmung

- **Ergebnisvertrag** (Anwendbarkeit, vier Nachweisarten, fünf Ergebnisse mit Rangfolge ❌ > ⚠️ > „Nachweis offen“ >
  ✅, Pflichtbelege, Budgetabbruch nach zehn Aufrufen mit „Teilprüfung – Nachweise offen“): wird so Text der
  HA-Reference von audit.
- **Pflichtfelder von `module.yaml`:** Tabelle übernehmen, mit den Änderungen von ChatGPT (UI und Adapter nach
  vorhandenem Bestandteil, `failure_policy.manual` bei eigenen manuellen Aktionen, Bedingungen gegen den Code prüfen).
  Ergänzungen: `critical_for` mit eindeutigen Verweisen (`entities:<key>`, `actions:<name>`); feste Liste zulässiger
  `module.type`; `fallback` verlangt die Ersatzregel im Steckbrief.
- **Eigentum ohne Eigentümerfeld:** jeder Eintrag unter `owns` gehört implizit `module.id`; audit verfolgt Prüfung,
  Schreiben und Registrierung im Code.
- **Prüftabelle G-01 … G-22** als Grundlage der Reference; zusätzliche Tests darin sind mögliche Belege, keine neuen
  Pflichten.

## Grün-Speicher von checks.py

Befund am Code bestätigt: `fingerabdruck()` hasht die Befehle und den Inhalt der *geänderten* passenden Dateien
(`geaendert()` aus `git status`). Unveränderte Dateien, die den Check beeinflussen, fehlen – nach einem Pull oder
Branchwechsel kann ein alter Grün-Vermerk wieder passen. Das betrifft auch den eigentlichen Zweck (Doppelläufe sparen).

Mein Vorschlag, einfacher als getrennte Eingabemuster: den aktuellen Commit (`git rev-parse HEAD`) in den Hash
aufnehmen. HEAD plus Inhalt der geänderten Dateien beschreibt den gesamten Arbeitsstand. Dazu im Merker Zeitpunkt und
Exit-Code speichern; Umgebungsversionen nur, wo ein Check sie braucht. Umsetzung als Skill-Issue git-commit-helper.
Bis dahin meldet audit „früherer grüner Lauf vermerkt; Ausführung für den aktuellen Stand offen“. In `/config` ohne Git
bleibt die Ausführung immer offen.

## Vorschlag

Serie abschließen und umsetzen: `docs/ha-grundsatz/module-yaml.md` (Pflichtfelder, `critical_for`, Typen, Haus-Beispiel
mit `outage`), audit per skill-pflege (Modul 7 „Grundsatzregeln“, Reference `references/grundsatz/home-assistant.md` mit
Ergebnisvertrag und Prüftabelle), Skill-Issue für `checks.py`.
