# Vorlage Modul-Steckbrief

Eine Datei je Modul, für Herbert lesbar (G-19). Ab Stufe 2 Pflicht zusammen mit `module.yaml`
([`module-yaml.md`](./module-yaml.md)); in Stufe 0–1 ist der Steckbrief das Ergebnis des kurzen Wegs
([`wege.md`](./wege.md)) – dort reichen die Abschnitte 1–9, 12 und 14. Abschnitte ohne Inhalt bleiben mit „–“ stehen.

```markdown
# Modul <Name>

## 1 Zweck
Was das Modul für wen leistet.

## 2 Nicht-Ziele
Was es ausdrücklich nicht tut.

## 3 Ausbaustufe
Stufe 0–4 und warum keine niedrigere reicht (G-03).

## 4 Abhängigkeiten
Integrationen und Module, die vorhanden sein müssen.

## 5 Quellen
Eingänge mit Eigentümer; je Quelle das Ausfallverhalten (G-21).

## 6 Fachlogik
Was das Modul berechnet und entscheidet (G-04, G-12).

## 7 Eigentumsregister
Je Wert: Eigentümer, Speicherort, Schreibwege (G-01).

## 8 Entitäten
Eigene Ergebnis-Entitäten mit Domain und Bedeutung (G-07, G-13).

## 9 Einstellungen
Je Einstellung: Art laut Einstellungsmatrix, Speicher, bevorzugter Bedienort (G-09).

## 10 Aktionen, Ereignisse, WebSocket
Öffentliche Befehle und Schnittstellen der eigenen Oberfläche (G-08, G-11).

## 11 Speicherung und Verlauf
Eigene Daten, Schema-Version, Sicherung; was der Recorder übernimmt (G-10, G-14).

## 12 Oberfläche
Karten, Panels, Dashboards (G-22).

## 13 Fehler, Diagnose, Reparatur-Hinweise
Ausfälle, Diagnosedaten, benutzerlösbare Fehler (G-17, G-21).

## 14 Tests
Fachlogik-Tests, Ausfalltests, Einrichten → Entladen → Neu laden (G-15).

## 15 Einspielen
Wie eine Änderung aktiv wird (G-16).

## 16 Entscheidungen
Getroffene Entscheidungen mit Datum und Begründung.
```
