# Review Runde 2

Claude, der Ergebnisvertrag lässt sich jetzt festlegen. **Beim Grün-Speicher gibt es allerdings einen entscheidenden Widerspruch: Er bindet den Lauf derzeit nur an passende *geänderte* Dateien, nicht an sämtliche Eingaben des Tests.** Deshalb kann audit ihn noch nicht als vollständigen Ausführungsnachweis übernehmen.

## 1. Ergebnisvertrag — Text für die Reference

**Anwendbarkeit**

Je Modul zunächst die deklarierte höchste Ausbaustufe feststellen und mit den tatsächlich vorhandenen Bestandteilen vergleichen. Eine belegte höhere Mindeststufe darf nicht durch eine niedrigere Deklaration ausgeblendet werden. Bei ungeklärter Stufe belegbare Prüfungen fortsetzen; stufenabhängige Entscheidungen offenlassen.

Eine Regel gilt, wenn ihre Mindeststufe erreicht und ihr Gegenstand vorhanden ist. Fehlende vorgeschriebene Bestandteile sind ein Befund, kein Grund für „nicht anwendbar“.

**Nachweisarten**

- **Statisch:** Implementierung oder Vertrag gelesen; Suchtreffer anschließend im Kontext geprüft.
- **Test vorhanden:** Testinhalt und Assertions decken den betreffenden Prüffall ab.
- **Ausführung:** zugeordneter Test erfolgreich ausgeführt; Ergebnis gilt für die aktuellen relevanten Eingaben und die erforderliche Umgebung.
- **Urteil:** begründete fachliche Bewertung anhand benannter Belege.

Je Regel erforderliche Teilnachweise getrennt bewerten. Nicht jede Regel benötigt alle vier Arten.

| Ergebnis | Eindeutige Bedeutung |
|---|---|
| ✅ | Alle für diese Regel erforderlichen Teilnachweise erfüllt; kein belegter Verstoß. |
| ⚠️ | Belegte Inkonsistenz ohne bereits nachgewiesene Verletzung einer verbindlichen Regel; Korrektur empfohlen. |
| ❌ | Konkrete Verletzung einer anwendbaren Pflicht nachgewiesen. |
| Nachweis offen | Erforderlicher Nachweis fehlt, ist unzureichend, veraltet oder nicht geprüft; kein belegter Verstoß. |
| Nicht anwendbar | Mindeststufe oder Gegenstand trifft nachweislich nicht zu. |

**Aggregation:** ❌ hat Vorrang vor ⚠️, danach „Nachweis offen“, danach ✅. Offene Teilnachweise bleiben auch neben einem ❌ sichtbar. Ein ungeklärter Suchtreffer ist „Nachweis offen“, keine belegte Inkonsistenz.

Verlangt die Regel ausdrücklich einen Test und dieser fehlt nach vollständiger Suche im festgelegten Testbereich, ist das ❌. Ein vorhandener geeigneter Test ohne gültiges Laufergebnis bedeutet dagegen „Ausführung offen“.

**Pflichtbelege**

Regelnummer, Modul, Stufe samt Herkunft, betroffener Bestandteil, Teilnachweis, Datei und Zeile beziehungsweise Abschnitt, Begründung. Bei Ausführung zusätzlich Check/Test-Zuordnung und überprüfbarer Standbezug. Bei fehlenden Dateien den erwarteten Pfad und den untersuchten Bereich nennen. Geheimniswerte niemals zitieren.

**Budgetabbruch**

Nach zehn Tool-Aufrufen endet das Teilaudit. Report kennzeichnen: **„Teilprüfung – Nachweise offen“**. Geprüfte Bereiche, offene Regeln und nächster erforderlicher Nachweis werden genannt. Nicht gelesene Bereiche erhalten kein ✅.

```text
G-15 | Nachweis offen | Modul haus, Stufe 2
Statisch: Entladepfad und Ressourcenfreigabe nachvollzogen — Datei:Zeile.
Test vorhanden: Einrichten → Entladen → Neu laden geprüft — Testdatei:Zeile.
Ausführung: Standbezug unzureichend.
Nächster Nachweis: gültiger Lauf des zugeordneten Profil-Checks.
```

## 2. Manifest-Pflichtfelder

Deinen Vorschlag übernehme ich mit zwei Änderungen: **UI und Adapter werden anhand vorhandener Bestandteile verlangt**, nicht allein anhand der höchsten Stufe. Außerdem braucht `failure_policy` auch für manuelle Aktionen eine Bedingung.

Die folgende Tabelle ist eine **vorgeschlagene normative Präzisierung** des bisher beschreibenden Schemas. [Manifest v1](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/ha-grundsatz/module-yaml.md)

| Feld | Pflicht | Bedingung / zulässiger Inhalt |
|---|---|---|
| `schema` | Immer | Ganzzahl `1`. |
| `module.id` | Immer | Nichtleere fachliche Modulkennung. |
| `module.level` | Immer | Ganzzahl 0–5; höchste tatsächlich eingesetzte Stufe. |
| `module.type` | Immer | Nichtleerer Bestandteiltyp; zulässige Typen explizit definieren. |
| `owns` | Immer | Objekt; `{}` erlaubt, wenn nichts Eigenes existiert. |
| `owns.settings` | Bedingt | Eigene Einstellungen vorhanden; je Eintrag `key`, `storage`; `exposure`, wenn veröffentlicht. |
| `owns.data` | Bedingt | Eigene persistente Fachdaten vorhanden; je Eintrag `key`, `storage`. |
| `owns.entities` | Bedingt | Eigene Ergebnisentitäten vorhanden; je Eintrag `key`, `domain`. |
| `owns.actions` | Bedingt | Eigene Aktionen vorhanden; eindeutige Aktionsnamen. |
| `depends_on.integrations` | Bedingt | Erforderliche Integrationen vorhanden. |
| `sources` | Bedingt | Fremde Eingänge vorhanden; je Quelle `key`, `owner`, `interface`; `domain`, wenn zur Auswahl nötig. |
| `sources[].outage` | Bedingt | Ab Stufe 2, wenn ein eigenes Ergebnis oder eine Aktion von der Quelle abhängt. |
| `outage.critical_for` | Bedingt | Bei vorhandenem `outage`; nichtleere Liste auflösbarer Ergebnis-/Aktionsreferenzen. |
| `outage.on_unavailable` | Bedingt | Bei vorhandenem `outage`: `block`, `fallback` oder `ignore`; fachlich begründet. |
| `outage.recovery` | Bedingt | Bei vorhandenem `outage`: `re_evaluate`. |
| `outage.max_age` | Bedingt | Nur bei fachlichem Frischebedarf; positive Dauer. |
| `database` | Bedingt | Eigene Datenbank vorhanden, auch wenn ihre Deklaration unter `owns.data` fehlt. |
| `database.schema_versioned`, `database.backup_hooks` | Bedingt | Bei `database`; boolesch. `false` ist gegebenenfalls ein Regelverstoß, kein Typfehler. |
| `adapters` | Bedingt | Herstelleradapter vorhanden; je Eintrag `id`, konkrete fachliche `reason`; höchste Stufe dann 5. |
| `ui` / `ui.type` | Bedingt | Eigene Oberfläche vorhanden; UI-Typ benennen. |
| `interfaces.websocket` | Bedingt | Eigene WebSocket-Schnittstellen vorhanden. |
| `failure_policy.scheduled` | Bedingt | Zeitabhängige Aufträge vorhanden; `strategy` und `on_recovery`. |
| `failure_policy.manual` | Bedingt | Eigene manuelle Aktionen vorhanden; `strategy: fail`. |
| `quality.unload_reload` | Bedingt | Eigene Config-Entry-Integration vorhanden. |
| `quality.diagnostics`, `quality.repairs` | Bedingt | Entsprechende Qualitätsanforderung anwendbar; Anwendbarkeit im Steckbrief begründen. |

Bedingungen immer **gegen den Code prüfen**. Sonst könnte ein fehlendes `owns.data` die Datenbankpflicht umgehen.

Zwei Details brauchen Ergänzungen im Schema:

- `critical_for` muss eindeutig auflösbar sein, etwa über `entities:<key>` und `actions:<name>`. Die vorhandenen Kategorien für Einstellungen und Ergebnisse berücksichtigen.
- Bei `fallback` muss eine konkrete Ersatzregel im Steckbrief auffindbar sein. `ignore` darf keine tatsächlich notwendige Abhängigkeit verdecken.

**Eigentum ohne Eigentümerfeld:** Jeder Eintrag unter `owns` behauptet implizit `owner = module.id`. audit verfolgt diesen Anspruch bis zur Implementierung: Wer validiert Änderungen, wer schreibt den maßgeblichen Speicher, wer registriert die Entität beziehungsweise Aktion? Eine fremde Entität wird durch Lesen oder Anzeigen nicht zu Eigentum. Ein Schema prüft Struktur und Referenzen; tatsächliches Eigentum braucht Codeabgleich und gegebenenfalls Tests.

Für Stufe 0–1 bleibt das Manifest freiwillig. Bei freiwilliger Verwendung gilt seine Struktur, aber keine nachträglich erfundene Integrationspflicht.

## 3. Grün-Speicher: derzeit nur eingeschränkt brauchbar

`geaendert()` liefert Git-Statusdateien; `passende()` filtert diese. `fingerabdruck()` hasht Befehle und deren aktuellen Arbeitsbaum-Inhalt. Unveränderte Testdateien, Abhängigkeiten und Konfiguration fehlen. Der Merker speichert nur Checkname → Hash; der Hash entsteht vor dem Lauf. **Ein Treffer beweist deshalb keinen vollständigen aktuellen Teststand.** [checks.py, insbesondere Zeilen 123–151 und 192–235](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/skills/git-commit-helper/scripts/checks.py)

Ein Gegenbeispiel: Gleiche Änderung an Datei A auf zwei unterschiedlichen Basisständen; unveränderte Datei B beeinflusst den Test. B fehlt im Hash, sodass ein alter grüner Merker wieder passen kann.

Für einen belastbaren Nachweis schlage ich vor:

- Änderungsmuster nur zur **Auswahl** verwenden; getrennte Eingabemuster erfassen sämtliche relevanten Dateien einschließlich Tests, Fixtures, Konfiguration und Lockfiles.
- Vorher/nachher denselben Eingabestand prüfen; bei Änderungen während des Laufs keinen gültigen Merker speichern.
- Strukturierten Datensatz speichern: Checkdefinition, Eingabeliste und Hash, Umgebungsversionen, Zeitpunkt, Exitcode, Ergebnisartefakt und Testumfang einschließlich übersprungener Fälle.
- Check → Regelteilnachweis explizit zuordnen; ein grüner Sammelbefehl beweist nicht automatisch jeden Prüffall.

Bis dahin: **„früherer grüner Lauf vermerkt; Ausführung für aktuellen Gesamtstand offen“**. In `/config` ohne Git braucht audit einen separaten Nachweisweg.

## 4. Prüftabelle für die HA-Reference

Die Mindeststufen stammen aus der Regelquelle; die übrigen Spalten sind vorgeschlagene Prüfverfahren. „—“ bedeutet: kein eigener Laufnachweis zwingend, soweit der konkrete Regeltext ihn nicht verlangt. [G-01 … G-22](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/ha-grundsatz/README.md)

| Regel | ab | Kandidaten (Suche) | Kontext (Urteil) | Test-/Ausführungsnachweis |
|---|---:|---|---|---|
| G-01 | 0 | Schreibwege, Speicher | Ein Eigentümer | Validierung aller Schreibwege |
| G-02 | 0 | Bestandsanalyse | HA-Fähigkeiten ausreichend? | — |
| G-03 | 0 | Stufenbegründung | Niedrigste ausreichende Stufe | — |
| G-04 | 1 | UI-Berechnungen | Darstellung oder Fachentscheidung? | Fachlogik getrennt |
| G-05 | 2 | Imports, Speicherpfade | Fremdmodulzugriff? | Grenzprüfung |
| G-06 | 2 | Herstellerverzweigungen | Fähigkeit oder Hersteller? | Fähigkeitsvarianten |
| G-07 | 2 | Vertrag, Entitäten | Ergebnis sinnvoll darstellbar? | Vertragsabgleich |
| G-08 | 1 | Aktionen, Buttons, Zustandsänderungen | Befehl oder Zustand? | Befehlswirkung |
| G-09 | 1 | Speicher, `RestoreEntity` | Matrix, Zweitquelle | Persistenz, Schreibwege |
| G-10 | 2 | Tabellen, Historien | Fachlicher Speichergrund | — |
| G-11 | 2 | Attribute, Listen | Wachstum, Schnittstelle | Nutzlastbegrenzung |
| G-12 | 2 | HA-Imports im Fachkern | Determinismus | Fachtests ohne HA |
| G-13 | 2 | IDs, Namen, Übersetzungen | Vererbung, UI-ID-Auflösung | Registry-/Drifttest |
| G-14 | 2 | Schema, Schreibzugriffe, Backup | Kontrollierte Persistenz | Sicherung/Wiederherstellung |
| G-15 | 2 | Unload, Listener, Tasks | Vollständige Freigabe | Einrichten/Entladen/Neuladen |
| G-16 | 2 | Optionslistener, Einspielanleitung | Passender Aktivierungsweg | Optionsreload, Kurztest |
| G-17 | 2 | Diagnostics, Repairs | Größe, benutzerlösbarer Fehler | Redaktion, Issue-Lebenszyklus |
| G-18 | 0 | Geheimnisse, Ressourcenpfade | Echtwert, Veröffentlichung, extern? | Schutz-/Redaktionstests |
| G-19 | 2 | Manifest, Steckbrief | Eigentum, Konsistenz | Schema-/Vertragsprüfung |
| G-20 | 0 | Änderung, Entscheidungen | Reihenfolge, gemeinsame Pflege | Vor-Einspielen-Nachweis |
| G-21 | 1¹ | Ersatzwerte, Verfügbarkeit | Sperre, Frische, Erholung | Ausfallfälle je Quelle |
| G-22 | 3 | Lit, HTML-Zuweisungen, Build | Tatsächliche UI-Implementierung | Bundleprüfung |

¹ Voller Ausfallvertrag ab Stufe 2. Tests nur für fachlich relevante Fälle verlangen; beispielsweise Alterung nur bei entsprechendem Frischebedarf. Zusätzliche Tests in dieser Tabelle sind mögliche Belege, keine automatisch neuen Pflichten.

**✅ Einigkeit:** Höchste Modulstufe, bedingte Manifestfelder, getrennte Teilnachweise, begrenztes Audit und zehn Aufrufe.

**⚠️ Widerspruch:** Der bestehende Grün-Speicher reicht nicht als aktueller Gesamtnachweis. UI-Pflicht folgt dem Bestandteil; manuelle Aktionen benötigen ebenfalls eine Ausfallstrategie.

**❓ Rückfragen:** Übernehmen wir getrennte Auswahl-/Eingabemuster für Checks und eindeutige Referenzen in `critical_for` als verbindliche Ergänzungen?