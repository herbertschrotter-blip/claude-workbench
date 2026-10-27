# Doku-Validierung – Prüflisten

Prüflisten für audit, Modul 6 („Formale Doc-Prüfung nach Profil“, `../SKILL.md#Modul 6 — Formale Doc-Prüfung nach
Profil`): was bei der Doku-Validierung eines Projekts geprüft wird. Vorrang hat `Doku.Validierungsregeln` des
Skill-Profils (ohne Skill-Profil: Feld „Validierung“ des Doku-Profils); diese Listen gelten nur, wenn ein Projekt dort
keine Regeln führt. Bei `none` entfällt die Prüfung. Passt keine der Listen zum Projekt, fragt audit
`Doku.Validierungsregeln` nach „Fehlende Werte“ (`docs/skill-profile-v1.md`) ab; eine fremde Liste gilt nicht.

Befunde als Tabelle (Doc, Stelle, Befund, Vorschlag); bei mehreren Lösungen Auswahlfrage. Nichts stillschweigend
korrigieren, was eine Entscheidung des Users ist (Status, Freigaben).

## Heidi-Prüfliste (aus dem Doku-Profil)

Stufe A — Blocker:
- Statusliste (Bauplan Abschnitt 1) ↔ ClickUp-Status (DX-Aufgaben) ↔ Code: fertig nur, wenn Code, Tests und Commit da sind
- Statusliste ohne Lücken
- Jede Abweichung von v1 hat einen PD-Eintrag in 10a mit Status `freigegeben`
- Abschnitt 4 (Entitäts-Vertrag) ↔ `contract.ts`: gleiche Entitäten, gleiche Dienste
- HANDOFF Abschnitt 3e nennt den letzten abgeschlossenen Bauschritt und die aktuelle Version
- Nichts Verbotenes im Repo (Token, GPS, `.storage`, Datenbanken, Laufprotokolle)

Stufe B — Warnung:
- ⚠️ Notiz in Abschnitt 10 ohne Datum, Aufgabe, Art oder Schwere; Entscheidung Herbert fehlt bei Widerspruch/Wunsch
- ⚠️ Aufgabenkarte ohne eines der Felder Voraussetzung, Ziel, Nicht ändern, Akzeptanz, oder ohne Tests
- ⚠️ PD-Tabelle (10a) nicht vollständig gefüllt
- ⚠️ Offene Punkte (HANDOFF Abschnitt 4) ohne Gegenstück in ClickUp
- ⚠️ Plan-Doc (GERAETEPROFIL, PLANER-NACHHOLEN, UX-TRANSITIONS) ohne Stand-Datum
- ⚠️ Version in package.json, Lock und Ressourcen-`?v=` uneinheitlich

## BPM-Prüfliste: Frontmatter + Quickload

### Stufe A — Formal (Blocker)

- Frontmatter vorhanden bei Kern/, Module/, Referenz/?
- Alle Pflichtfelder?
- doc_id eindeutig?
- Enums korrekt?
- Quickload bei source_of_truth/secondary?
- Quickload Kapitel-Feld stimmt mit H2s?
- Kapitelreihenfolge nach Vorlage?
- Pflichtlesen verweist auf existierende Kapitel?
- Fachliche Invarianten max 5?
- INDEX referenziert nur Docs mit gültigem Frontmatter?

### Stufe B — Semantisch (Warnung)

- ⚠️ Quickload Kapitel stimmt nicht mit H2s
- ⚠️ historical als Primary im Router
- ⚠️ related_docs nicht existent
- ⚠️ Kapitelvorlage nicht eingehalten
- ⚠️ Fachliche Invarianten leer bei großem Modul
- ⚠️ Pflichtlesen leer bei source_of_truth Modul
- ⚠️ Fachliche Invarianten widersprüchlich zwischen Docs
