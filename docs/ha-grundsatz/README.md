# HA-Grundsatz

Grundsatzregeln für alle Home-Assistant-Projekte von Herbert: wie ein Gerät, ein Modul oder ein Dashboard aufgebaut wird –
vom Konzept bis zum fertigen Dashboard. Für Herbert verständlich, für Claude eindeutig prüfbar.

**Wer sie nutzt:** `projekt-anlegen` beim Anlegen von HA-Projekten (Profilfeld `Modul.Grundsatzregeln`,
`skills/projekt-anlegen/references/stacks/home-assistant.md`), `code-erstellen` über die Architekturregeln im Code-Profil
eines HA-Repos, `audit` beim Prüfen dagegen. Einen eigenen Skill dafür gibt es nicht.

**Herkunft:** erarbeitet im Review `CGR-2026-09-23-ha-grundsatz` (`docs/chatgpt-reviews/CGR-2026-09-23-ha-grundsatz/`,
Runden 1–4), Endfassungen aus Runde 3 und 4; G-22 direkt von Herbert. Referenzfall ist der Roboter Heidi (Repo
`HA_Dash_DreameX60`), der nach diesen Regeln neu gebaut wird – ohne Migration.

## Inhalt

- Dateien
- Leitsätze
- Ausbaustufen
- HA-Grundsatzregeln
- Erläuterungen
- Begriffe

## Dateien

| Datei | Inhalt |
|---|---|
| `README.md` | Leitsätze, Ausbaustufen, die Regeln G-01 … G-22, Begriffe |
| [`einstellungen.md`](./einstellungen.md) | Einstellungsmatrix: wo welche Einstellung liegt und wie sie bedient wird (G-09) |
| [`wege.md`](./wege.md) | Kurzer Weg (Stufe 0–1), voller Weg (ab Stufe 2), Reihenfolge beim Planen, Einspielen |
| [`module-yaml.md`](./module-yaml.md) | `module.yaml` Schema v1 mit Ausfallverhalten und Beispielen (G-19, G-21) |
| [`steckbrief-vorlage.md`](./steckbrief-vorlage.md) | Vorlage Modul-Steckbrief (G-19) |
| `recherche-2026-09-23.md` | Recherche: offizielle HA-Vorgaben und bewährte Praxis, mit Quellen |

## Leitsätze

1. **Ein fachlicher Eigentümer je Wert.** Mehrere Bedienwege (Karte, Automation, Sprache) sind erlaubt; sie enden alle
   beim Eigentümer, der prüft und speichert.
2. **Eine Schnittstelle ist kein Speicherort.** Entität, Aktion (Action) und WebSocket sind Zugänge; Speicher sind
   Einrichtung (Config Entry), Integrations-Speicher (Store), Recorder und Modul-Datenbank.
3. **Nichts Veraltetes als aktuell ausgeben.** Fällt eine Quelle aus, zeigt das Modul den Ausfall statt alter Werte.
4. **Erst fragen, was Home Assistant schon kann**, dann auf der niedrigsten ausreichenden Stufe bauen.

## Ausbaustufen

Ein Problem wird auf der niedrigsten ausreichenden Stufe gelöst (G-03). Die Stufe steht im Steckbrief mit Begründung.

| Stufe | Was | Beispiel |
|---|---|---|
| 0 | Vorhandene HA-Funktion direkt benutzen | Entität einer Integration im Dashboard |
| 1 | Helfer, Vorlage (Template), Automation, Skript, Blueprint | Pool-Sensor aus zwei Werten, Benachrichtigung |
| 2 | Eigenes Fachmodul als eigene Integration (`custom_components`) | Haus-Modul `haus` |
| 3 | Eigene Karte (Custom Card) | Karte des Roboters |
| 4 | Eigenes Panel bzw. eigener App-Bereich | Seiten-App in der Seitenleiste |
| 5 | Herstelleradapter, nur wenn HA eine benötigte Fähigkeit nicht vereinheitlicht (G-06) | Raumreinigung je Raum beim Roboter |

Der Adapter kommt zuletzt – nicht automatisch mit der Integration, sondern erst, wenn feststeht, welche Fähigkeit HA fehlt.

## HA-Grundsatzregeln

„ab“ = gilt ab Ausbaustufe. „Prüfbar durch“ ist das, woran Claude die Regel nachweist.

| Nr. | Regel | Prüfbar durch | ab |
|---|---|---|---|
| **G-01 Eigentum** | Jeder fachliche Wert hat genau einen Eigentümer und einen Speicherort; jede Änderung wird vom Eigentümer geprüft (validiert). | Eigentumsregister im Steckbrief; keine dauerhafte Zweitquelle. | 0 |
| **G-02 HA zuerst** | Vor Eigenbau wird geprüft, ob HA die benötigte Fähigkeit bereits ausreichend standardisiert. | Bestandsanalyse nennt vorhandene Entitäten, Aktionen, Helfer. | 0 |
| **G-03 Niedrigste Stufe** | Ein Problem wird auf der niedrigsten ausreichenden Ausbaustufe gelöst. | Steckbrief begründet die Stufe. | 0 |
| **G-04 Fachlogik** | Fachliche Berechnung und Entscheidung liegen im zuständigen Modul, nicht in Karte oder Dashboard. | Keine konkurrierende Fachberechnung in der Oberfläche. | 1 |
| **G-05 Modulgrenzen** | Module sprechen nur über öffentliche HA-Schnittstellen miteinander. | Keine fremden Datenbank- oder Dateizugriffe, keine direkten Modul-Importe. | 2 |
| **G-06 Fähigkeiten** | Fachlogik prüft Fähigkeiten statt Hersteller oder Modell; Herstellerspezifisches endet im Adapter. | Hersteller- und Modellnamen außerhalb des Adapters werden geprüft. | 2 |
| **G-07 Zustände** | Aktuelle, für HA relevante Ergebnisse eines Moduls werden als Entitäten veröffentlicht, sofern sie sich sinnvoll als Zustand darstellen lassen. | `module.yaml` ↔ umgesetzte Entitäten. | 2 |
| **G-08 Befehle** | Vorgänge werden als Aktion (Action) oder Taste (Button) gebaut, nicht als künstliche Zustände. | Der Vertrag trennt Zustand und Befehl. | 1 |
| **G-09 Einstellungen** | Einrichtung, Optionen, Einstellungs-Entität, Liste oder Objekt der eigenen Oberfläche, Fachobjekt und Darstellung werden nach der Einstellungsmatrix getrennt ([`einstellungen.md`](./einstellungen.md)). | Jede Einstellung hat genau eine Art, einen Eigentümer und einen Speicher. | 1 |
| **G-10 Historie** | Den normalen Verlauf von Entitäten speichert der Recorder; eigene Speicherung braucht einen fachlichen Grund. | Datenbank-Schema ohne unbegründete Spiegelung des Verlaufs. | 2 |
| **G-11 Große Daten** | Große oder strukturierte Daten stehen nicht in Entitäts-Attributen, sondern laufen über eine passende Schnittstelle (WebSocket, eigene Abfrage). | Vertrag und Größenprüfung. | 2 |
| **G-12 Reine Fachlogik** | Berechnung und Entscheidung sind soweit möglich unabhängig von HA und deterministisch testbar. | Fachlogik-Tests laufen ohne HA. | 2 |
| **G-13 Entitäts-Vertrag** | Eigene Entitäten haben `unique_id`, `has_entity_name` und bei benannten Rollen einen festen `translation_key`; die eigene Oberfläche baut keine Entitäts-IDs zusammen. | Test gegen das Entitätsregister (Registry, Drift). | 2 |
| **G-14 Persistenz** | Eigene Datenbanken haben eine Schema-Version, kontrollierte Schreibzugriffe und eine passende Sicherung und Wiederherstellung. | Schema- und Sicherungstest. | 2 |
| **G-15 Lebenszyklus** | Eine Einrichtung (Config Entry) lässt sich sauber entladen und neu laden; Ressourcen werden beim Entladen freigegeben. | Test Einrichten → Entladen → Neu laden. | 2 |
| **G-16 Einspielen** | Eine Optionsänderung lädt den Eintrag neu; Python-Code wird per HA-Neustart aktiv, Oberflächen-Code per Neuladen im Browser. | Kurztest nach dem Einspielen. | 2 |
| **G-17 Diagnose** | Größere Module bieten Diagnosedaten (Diagnostics) und für dauerhafte, vom Benutzer lösbare Fehler einen Reparatur-Hinweis (Repairs). | Qualitätsprüfung. | 2 |
| **G-18 Sicherheit** | Geheimnisse und private Daten – auch Koordinaten, Gerätekennungen und Personennamen – liegen weder im Repo noch ungeschützt unter `/local`. | Prüfung auf Geheimnisse und Pfade. | 0 |
| **G-19 Vertrag** | Ab Stufe 2 hat jedes Modul einen Steckbrief und eine `module.yaml`; Fremdeigentum steht darin nur als Abhängigkeit oder Quelle. | Schema-Test und Prüfung der Eigentümer. | 2 |
| **G-20 Arbeitsweise** | Vertrag vor Mockup, Tests vor dem Einspielen, Doku und Entscheidungen zusammen mit der Änderung. | Prüfung bei Commit und Abnahme. | 0 |
| **G-21 Ausfall** | Ein Modul erkennt fehlende, deaktivierte, nicht verfügbare oder unzulässig alte Quellen und verwendet sie nicht stillschweigend als aktuelle Daten. Für benötigte Quellen sind Sperr- oder Ersatzverhalten und Wiederanlauf festgelegt; betroffene Zustände zeigen den Ausfall richtig, und benutzerlösbare dauerhafte Fehler erhalten einen Reparatur-Hinweis. | Ausfalltest je kritischer Quelle: Quelle fehlt, ist deaktiviert, `unavailable` oder veraltet → keine unzulässige Aktion und richtiger sichtbarer Zustand; Quelle zurück → automatische Neubewertung und Erholung ohne Neustart. | 1; voller Vertrag ab 2 |
| **G-22 Oberfläche mit Lit** | Eigene Oberflächen in HA (Karten, Panels, Dialoge) werden mit **Lit** als Web Components gebaut und zu einer ausgelieferten Datei gebündelt; kein HTML als Text mit `innerHTML`. Die Sprache folgt dem Stack des Projekts (TypeScript oder JavaScript); für Code gilt die Stack-Referenz `typescript-lit` von code-erstellen. Bestehende Oberflächen ohne Lit werden schrittweise umgestellt, nicht nebenbei. | Code-Profil führt den Stack; keine `innerHTML`-Vorlagen. | 3 |

## Erläuterungen

**G-13:** `has_entity_name` ist für neue Integrationen von HA vorgeschrieben; ein übersetzter Name braucht
`translation_key` und dafür eine `unique_id`. Dass benannte Rollen immer einen festen `translation_key` tragen, ist
**unsere Konvention**, keine Garantie von HA.

**G-16:** Python-Code einer Integration wird erst mit einem HA-Neustart aktiv, und den löst nur Herbert aus. Deshalb:
Änderungen sammeln, vorher am Pi testen, ein Neustart je Lieferung ([`wege.md`](./wege.md), Abschnitt Einspielen).

**G-21** regelt das fachliche Verhalten bei ausgefallenen Eingängen; G-07 (wie Zustände erscheinen), G-15 (technische
Erholung) und G-17 (Diagnose, Reparatur-Hinweis) bleiben eigene Regeln. Vier Unterregeln:

1. **Aktualität:** Aktuelle Werte nicht aus veralteten Daten vortäuschen; Werte, die ausdrücklich Vergangenheit
   beschreiben („letzte Reinigung“), dürfen bestehen bleiben.
2. **Frische:** Keine globale Ausfallzeit; ein Höchstalter (`max_age`) nur je Quelle, wenn es fachlich nötig ist.
3. **Reparatur-Hinweis:** nur für Probleme, die der Benutzer lösen kann – nie als Offline-Wecker. Das ist feste Regel,
   kein Feld in `module.yaml`.
4. **Aufträge:** je zeitabhängigem Auftrag `drop`, `defer`, `retry` oder `fail` festlegen; nach der Rückkehr einer Quelle
   wird bei fachlichen Entscheidungen grundsätzlich mit aktuellen Daten neu bewertet.

Verhalten je Entität nach ihrer Bedeutung:

| Lage | Verhalten |
|---|---|
| Aktueller Wert hängt von der ausgefallenen Quelle ab | `unavailable` |
| Quelle antwortet, ein einzelner Wert fehlt | `unknown` |
| Ergebnis hängt von der Quelle nicht ab | normal verfügbar |
| Wert beschreibt Vergangenheit (z. B. „letzte Reinigung“) | letzten gültigen Wert behalten |
| Ergebnis ist ein bekannter Ausfallzustand (z. B. „Automatik blockiert“) | verfügbar, `blocked` mit Grund |
| Entscheidung braucht eine ausgefallene kritische Quelle | kein positives Ergebnis, Aktion sperren |
| Es gibt eine ausdrücklich festgelegte sichere Ersatzregel | Ersatzregel anwenden und erkennbar machen |

Ab Stufe 1 heißt das mindestens: Eine Automation oder Vorlage darf `unavailable` oder `unknown` nie als `0` oder `false`
deuten – etwa durch `| float(0)` in einer Vorlage. Eine manuell aufgerufene Aktion, die gerade nicht ausführbar ist,
schlägt mit verständlichem Fehler fehl.

## Begriffe

| Deutsch | HA-Fachwort |
|---|---|
| Einrichtung | Config Entry (`data`), eingerichtet im Config Flow |
| Optionen, Optionsdialog | Config Entry `options`, Options Flow |
| Integrations-Speicher | Store (`.storage/` der Integration) |
| Einstellungs-Entität | Entität mit `EntityCategory.CONFIG` (z. B. `switch`, `number`, `select`) |
| Aktion | Action (früher Service) |
| Taste | Button-Entität |
| Reparatur-Hinweis | Repairs-Issue |
| Diagnosedaten | Diagnostics |
| Verlauf | Recorder-Historie |
| Vorlage | Template |
| Eigene Karte, eigenes Panel | Custom Card, Custom Panel |
