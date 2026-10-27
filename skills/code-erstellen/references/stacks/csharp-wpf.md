# Stack: csharp-wpf — C# / .NET / WPF

Stack-Referenz für `code-erstellen`. Wird geladen, wenn das Skill-Profil des Projekts
`Code.Stacks: csharp-wpf` enthält. Projektspezifisches (Pfade, Pflicht-Docs, Deploy) steht
im Skill-Profil, nicht hier. Doc- und Dateinamen unten stammen aus BPM und sind Beispiele.

---

## Schichten und Kopplungsregeln

- View (XAML) → ViewModel prüfen; kein Code-Behind mit Fachlogik
- Neuer Service → Interface + DI-Registrierung (`App.xaml.cs`)
- Neuer Dialog → Theme-/Dialog-Referenz laden, bestehende Dialoge als Muster
- DB-Änderung → Datenbank-Klasse + Schema-Doku (Beispiel BPM: `ProjectDatabase.cs` + `DB-SCHEMA.md`)
- Externe Kommunikation → DSGVO-/DataClassification-Doc zuerst

## Modus-Eskalation (Beispiele)

| Standard | Deep |
|----------|------|
| neue Methode in öffentlichem Service/ViewModel | neues Interface / Service-Implementierung |
| neuer Dialog / View / Commands | neue Tabelle / Schemaänderung |
| Persistenzlogik ohne neue Tabelle | externe API / Import / Export |
| mehrere Dateien in einem Projekt | mehrere Schichten / Projekte, neuer Benutzerfluss |
| neue Validierungs-/Statuslogik | DSGVO / DataClassification; DI betroffen und nicht rein lokal |

## Impact-Check-Zeilen (Stack-Lesart)

- UI / XAML / Theme-Tokens
- ViewModel / Commands / Bindings
- Domain-Modell / Interface
- Infrastructure / SQLite / Dateisystem
- DI-Registrierung
- Externe Kommunikation; DSGVO / DataClassification
- Settings / Konfiguration; App-Lebenszyklus; Logging / Fehlerbehandlung

## Blocking: welche Doc zuerst

| Betroffen | Zuerst laden |
|-----------|--------------|
| DI | `App.xaml.cs` |
| Externe Kommunikation | Datenschutz-Doku (Beispiel BPM: `DSGVO-Architektur.md`) |
| UI | UI-/Theme-Doc |
| DB | Schema-Doku (Beispiel BPM: `DB-SCHEMA.md`) |

## Tests

- xUnit/NUnit laut Projekt; Testprojekt neben dem Produktivprojekt
- Befehl aus dem Skill-Profil (`Code.Tests`, z.B. `dotnet test`); im Cowork-Chat liefert der Skill den Befehl, der User führt aus

## Ausgabe (Cowork-Chat)

- Neue Datei → komplett · < 600 Zeilen und > 30 % geändert → komplett · ≥ 600 Zeilen → SUCHE/ERSETZE · XAML → Download

## Typische Fehler

- Migration bauen statt „Daten löschen, neu anlegen“ (Frühphasen-Prinzip laut Architekturregeln des Projekts, Beispiel BPM: INDEX.md)
- Service ohne Interface registrieren; Bindings ohne `INotifyPropertyChanged`
- Theme-Farben hart statt aus Ressourcen
