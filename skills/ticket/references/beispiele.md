# Beispielwerte für die Ticket-Config

Werte aus zwei Projekten. Sie zeigen, wie die Abschnitte aus `../SKILL.md#Voraussetzung: Skill-Profil` gefüllt werden;
für jedes Projekt gilt nur dessen eigene Config.

## Heidi (Diagnose-Protokoll)

Tickets aus der Karte („Fehler melden“) und aus der automatischen Auswertung des Diagnose-Protokolls.

| Abschnitt | Wert |
|-----------|------|
| Quelle (Präfix) | `HT-NNNN` |
| Lese- und Schreibweg (Befehle) | `.\tools\ticket.ps1 liste [alle]` · `zeige <nr>` · `status <nr> <status> [-Dx -Commit -Version]` · `notiz <nr> "<text>"` · `verwerfen <nr> "<grund>"` · `auswertung` |
| Statusmodell (Status) | `neu → angenommen → in_arbeit → geloest → geschlossen`, daneben `verworfen` |
| Pflichtangaben je Status | angenommen → Aufgaben-Nummer · geloest → Commit (+ Version) · verworfen → Grund |
| Tracker-Kopplung (Aufgaben) | tracker neu, Titel „`<Präfix-Nr>`: `<Kurztitel>`“, Ticket-Text in die Beschreibung |
| Beweisquellen (Beweise nachlesen) | `node tools\diag.js --tag <Tag> --von <HH:MM> --bis <HH:MM> --debug` |
| Beweisquellen (Regeln) | `ha/prognose/diag_regeln.py`, Bauplan Karte F.2 |
| Doku-Kopplung (Doku) | Bauplan Abschnitt 10 |
| Schließen und Prüfen | User (Standard) |

## Eigene HA-Integration (Vorlage von projekt-anlegen)

Tickets aus dem Melden-Knopf der Seite; `Ticket.Config: ref:CLAUDE.md#Ticket-Profil`.

| Abschnitt | Wert |
|-----------|------|
| Quelle (Präfix) | `FE-NNNN` Fehler, `WU-NNNN` Wunsch, `AN-NNNN` Anregung; Ablage `<config>/<domain>/meldungen.json`, `meldungen.md` |
| Arten (Präfix → Ablauf) | nicht angegeben – Rückfall: FE voll, WU und AN verkürzt |
| Lese- und Schreibweg (Befehle) | `python3 tools/ticket.py liste [alle]` · `zeige <nr>` · `status <nr> <status> [--version X --commit Y --notiz T]` · `notiz <nr> "<text>"` · `verwerfen <nr> "<grund>"`; ändert nur über die Aktion `<domain>.ticket` |
| Statusmodell (Status) | `neu → angenommen → in_arbeit → geloest → geschlossen`, daneben `verworfen` |
| Pflichtangaben je Status | geschlossen → Version + Commit + Notiz · verworfen → Grund |
| Tracker-Kopplung (Aufgaben) | kein Tracker – Befund und Plan als Notiz am Ticket |
| Beweisquellen | `zeige <nr>` (Screenshots als `bild:`-Zeilen), Logbuch und Diagnose der Integration; Regeln `docs/entscheidungen.md` |
| Doku-Kopplung (Doku) | CHANGELOG-Eintrag nennt die Ticketnummer |
| Schließen und Prüfen | Claude schließt bei Erfolg (behoben, Tests grün, eingespielt); der User kann wieder öffnen |
