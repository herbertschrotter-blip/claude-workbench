# Grundsatzregeln Home Assistant – Prüfverfahren

Wie audit ein Home-Assistant-Projekt gegen die Grundsatzregeln prüft (Modul 7, `../../SKILL.md#Modul 7 — Grundsatzregeln`).
Die Regeln selbst stehen im Regelwerk, auf das `Modul.Grundsatzregeln` zeigt (G-01 … G-23 mit „Prüfbar durch“ und
„ab“ Stufe); diese Datei beschreibt nur, **wie** Claude sie nachweist. Sie erfindet keine zusätzlichen Pflichten.
Ergebnisse und Belege folgen dem Ergebnisvertrag (`../../SKILL.md#Ergebnisvertrag`).

## Inhalt

- Umfang
- Ausbaustufe ermitteln
- Vertrag (`module.yaml`)
- Prüftabelle
- Suchtreffer im Kontext
- Ausführungsnachweise
- Sonderfall Konfigurationsordner
- Geheimnisse

## Umfang

- Projekt-Repo (eigene Integration, Karte, Panel, Adapter): das Repo; je Manifest aus `Modul.Manifest` ein eigener
  Block mit Stufe und Ergebnissen.
- Konfigurationsordner von Home Assistant: nur die Positivliste aus `Modul.Prüfumfang` (Abschnitt „Sonderfall
  Konfigurationsordner“). Fehlt sie dort, Auswahlfrage „Umfang nennen / abbrechen“ – nie den ganzen Ordner lesen.

## Ausbaustufe ermitteln

Die Stufe entscheidet, welche Regeln gelten (Spalte „ab“).

1. Manifest vorhanden → `module.level` und `components` lesen und mit dem Bestand vergleichen.
2. Aus dem Bestand die **belegte Mindeststufe** ableiten: YAML-Pakete, Automationen, Helfer → 1;
   `custom_components/<name>/` → 2; eigene Karte (gebündeltes JS, `customCards`) → 3; eigenes Panel → 4;
   herstellerspezifischer Adapter → 5. Mehrere Bestandteile zählen zusammen; maßgeblich ist die höchste Stufe.
3. Eine niedrigere Deklaration blendet einen belegten Bestandteil nicht aus: Er wird geprüft, die Abweichung ist ein
   Befund zu G-19.
4. Eigene Integration ohne Manifest → ❌ G-19 (Vertrag fehlt); die übrigen belegbaren Prüfungen laufen weiter,
   vertragsabhängige bleiben „Nachweis offen“.
5. Im Report steht die Stufe mit Herkunft: „deklariert“ oder „abgeleitet“.

## Vertrag (`module.yaml`)

Schema und Pflichtfelder stehen im Regelwerk (`module-yaml.md` neben den Grundsatzregeln). Prüfen:

- Pflichtfelder ab Stufe 2; bedingte Felder **gegen den Code** (eine Datenbank im Code verlangt `database`, auch wenn
  `owns.data` fehlt)
- `components` enthält `module.type`; `module.level` = höchste Mindeststufe der Bestandteile; `card`/`panel` → `ui.types`,
  `adapter` → `adapters` mit konkretem `reason`
- Verweise in `critical_for` (`entities:`, `actions:`, `settings:`) lösen im selben Manifest auf
- Eigentum: jeder Eintrag unter `owns` gehört `module.id`; belegt im Code (wer prüft, wer schreibt, wer registriert).
  Fremde Werte nur unter `sources`/`depends_on`.
- Ein freiwilliges Manifest in Stufe 0–1 wird nur auf Struktur gelesen, nicht gegen die Pflichtfelder geprüft.

## Prüftabelle

Je Regel: Kandidaten finden, im Kontext beurteilen, Nachweis zuordnen. „—“ = kein eigener Laufnachweis nötig.

| Regel | ab | Kandidaten (Suche) | Kontext (Urteil) | Test- / Ausführungsnachweis |
|---|---:|---|---|---|
| G-01 Eigentum | 0 | Schreibwege, Speicher, doppelte Werte | ein Eigentümer, der prüft | Validierung aller Schreibwege |
| G-02 HA zuerst | 0 | Bestandsanalyse im Steckbrief | reicht eine HA-Fähigkeit? | — |
| G-03 Niedrigste Stufe | 0 | Stufenbegründung im Steckbrief | niedrigste ausreichende Stufe? | — |
| G-04 Fachlogik | 1 | Berechnungen in Karte, Dashboard, Vorlagen | Darstellung oder Fachentscheidung? | Fachlogik getrennt getestet |
| G-05 Modulgrenzen | 2 | fremde Imports, fremde DB-/Dateipfade | Zugriff auf ein anderes Modul? | Grenzprüfung |
| G-06 Fähigkeiten | 2 | Verzweigungen nach `manufacturer`/Modell außerhalb des Adapters | Fähigkeit oder Hersteller? | Fähigkeitsvarianten |
| G-07 Zustände | 2 | Vertrag ↔ registrierte Entitäten | sinnvoll als Zustand darstellbar? | Vertragsabgleich |
| G-08 Befehle | 1 | Aktionen, Tasten, Zustände, die Befehle auslösen | Befehl oder Zustand? | Befehlswirkung |
| G-09 Einstellungen | 1 | Speicherorte, `RestoreEntity`, Einstellungen in der Datenbank, `null`/`[]` | Art laut Einstellungsmatrix, keine Zweitquelle | Persistenz, Schreibwege |
| G-10 Historie | 2 | Tabellen mit Verlauf | fachlicher Speichergrund? | — |
| G-11 Große Daten | 2 | wachsende Listen/Objekte in `extra_state_attributes` | Wachstum, Begrenzung, passende Schnittstelle | Nutzlastbegrenzung |
| G-12 Reine Fachlogik | 2 | HA-Imports im Fachkern | deterministisch, ohne HA testbar? | Fachtests ohne HA |
| G-13 Entitäts-Vertrag | 2 | `unique_id`, `has_entity_name`, `translation_key`, IDs in der Oberfläche | Vererbung aus Basisklassen beachten | Registry-/Drift-Test |
| G-14 Persistenz | 2 | Schema-Version, Schreibzugriffe, Sicherung | kontrolliert? | Sicherung/Wiederherstellung |
| G-15 Lebenszyklus | 2 | `async_unload_entry`, Listener, Tasks | vollständige Freigabe? | Einrichten → Entladen → Neu laden |
| G-16 Einspielen | 2 | Options-Listener, Einspielanleitung | passender Aktivierungsweg? | Optionsreload, Kurztest |
| G-17 Diagnose | 2 | `diagnostics.py`, Repairs | Größe, benutzerlösbare Dauerfehler? | Redaktion, Lebenszyklus des Hinweises |
| G-18 Sicherheit | 0 | Geheimnisse, Koordinaten, Gerätekennungen, Personennamen, `/local`, externe Ressourcen in Oberflächen | echter Wert? veröffentlicht? | Schutz-/Redaktionstests |
| G-19 Vertrag | 2 | Manifest, Steckbrief | vollständig, Eigentum stimmig? | Schema-/Vertragsprüfung |
| G-20 Arbeitsweise | 0 | Commit mit Doku, Entscheidungen | gemeinsam gepflegt? | Nachweis vor dem Einspielen |
| G-21 Ausfall | 1¹ | Ersatzwerte (`\| float(0)`, `\| int(0)`), Verfügbarkeitsprüfungen, `outage` | Sperre, Frische, Erholung | Ausfallfälle je kritischer Quelle |
| G-22 Lit | 3 | Lit-Import, `innerHTML`, Bündelung | tatsächliche Umsetzung der Oberfläche | Bundle-Prüfung |
| G-23 Tickets | 2; Knopf ab 3 | Ticket-Config (`Ticket.Config`), `tools/ticket.py`, Aktion `<domain>.ticket`, `meldungen.json`, Melden-Knopf | Bilder kommen an, Rückmeldung nennt sie | Test über den ganzen Weg |

¹ Ab Stufe 1 mindestens: `unavailable`/`unknown` nie als `0` oder `false` deuten; voller Ausfallvertrag ab Stufe 2.
Tests in der Tabelle sind mögliche Belege, keine neuen Pflichten.

## Suchtreffer im Kontext

Ein Treffer ist ein Kandidat, kein Befund. Erst der Kontext entscheidet; ein ungeklärter Treffer ist „Nachweis offen“.

- **G-06:** Doku, Übersetzungen und Abhängigkeitsangaben zählen nicht; ein Verstoß ist eine fachliche Entscheidung nach
  Hersteller statt nach Fähigkeit.
- **G-11:** keine feste Byte-Grenze; verdächtig ist unbegrenztes Wachstum (z. B. eine Verlaufsliste), nicht eine Handvoll
  fester Werte.
- **G-13:** Eigenschaften können aus einer Basisklasse kommen; fehlender Text in der konkreten Klasse allein ist kein ❌.
- **G-17:** fehlendes `diagnostics.py` oder fehlende Repairs nicht pauschal beanstanden; erst die Anwendbarkeit klären.
- **G-21:** bei `float(0)` den Eingabewert und eine vorgeschaltete Verfügbarkeitsprüfung verfolgen; nicht jeder
  Zahlenfilter verarbeitet einen HA-Zustand.

## Ausführungsnachweise

- Zuordnung Check/Testfall → Teilnachweis (z. B. `G-15.lifecycle`) steht in der Config aus `Modul.Nachweise`; sie
  behauptet keinen Erfolg. audit liest Testinhalt und Assertions selbst.
- „Ausführung“ gilt nur, wenn ein Laufergebnis eindeutig zum geprüften Stand aller Eingaben des Tests gehört. Quelle
  ist der Datensatz des Prüfskripts von git-commit-helper im Git-Ordner (`git rev-parse --git-path skill-checks.json`,
  Schema 2, Eintrag je Check). audit erkennt ihn als „Ausführung“ nur an, wenn alles zutrifft:
  - der Check hat im Profil Eingabemuster (`[eingaben: …]`), und `inputs.patterns` stimmt mit ihnen überein
  - `definition_digest` passt zur heutigen Profilzeile (Befehle, Auswahl, Eingaben, `(allein)`)
  - die heute passenden Dateien und ihre Hashes entsprechen `inputs.files`, nachgerechnet, nicht nur verglichen
  - `exit_code` ist 0, `input_stable` ist wahr, und `result_artifact` existiert mit dem genannten Hash; aus ihm geht
    hervor, dass die zugeordneten Testfälle liefen und nicht übersprungen wurden (pytest etwa mit `-rA`; `-q` allein
    nennt keine Testfälle)
- Fehlt eines davon, meldet audit „früherer grüner Lauf vermerkt – Ausführung für den aktuellen Stand offen“; ohne
  Datensatz „Ausführung offen“. Checks ohne Eingabemuster liefern nie mehr als „früherer Lauf vermerkt“.
- audit führt keine Tests aus und startet HA nicht neu. Manuelle Kurztests (z. B. nach einem Neustart) zählen nur, wenn
  sie als manueller Nachweis mit Datum festgehalten sind.

## Sonderfall Konfigurationsordner

Der Konfigurationsordner von Home Assistant (Stufe 0–1, ohne Git, ohne Steckbriefpflicht):

- nur die Positivliste aus `Modul.Prüfumfang` lesen (z. B. eigene Pakete, Automationen, Skripte, Vorlagen)
- nie `.storage/`, Datenbanken (`*.db`), Sicherungen, `secrets.yaml` oder fremde Integrationen (`custom_components/`
  aus HACS) öffnen
- sinnvoll prüfbar: G-01 und G-09 an benannten Werten (fehlt die Angabe, „Beurteilungsgrundlage fehlt“), G-08, G-18,
  G-21 an konkreten Automationen und Vorlagen
- Ausführungs- und Commit-Nachweise bleiben offen; nichts unterstellt eine Steckbriefpflicht

## Geheimnisse

- Treffer nie wörtlich wiedergeben: nur Datei, Zeile und Art („Token“, „Koordinate“).
- Gesperrte Bereiche (Geheimnisse, Speicher von HA, Sperren der Umgebung) werden nicht geöffnet, um darin zu suchen.
- `!secret <schlüssel>` in YAML ist korrekt und kein Befund.
