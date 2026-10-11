# Einstellungen

Wo eine Einstellung liegt und wie sie bedient wird (Regel G-09 in [`README.md`](./README.md#ha-grundsatzregeln)).
Leitsatz: **ein fachlicher Eigentümer je Wert**, und **eine Schnittstelle ist kein Speicherort**.

## Inhalt

- Einstellungsmatrix
- Aktion oder WebSocket
- Kein zweiter Speicher
- Erben und leere Listen
- Auswahl aus HA-Objekten
- Bedienort

## Einstellungsmatrix

| Art | Eigentümer / Speicher | Bedienung |
|---|---|---|
| Grundlegende Einrichtung | Einrichtung (Config Entry `data`) | Einrichtungsdialog (Config Flow) |
| Seltene technische Option der Integration | Optionen (Config Entry `options`) | Optionsdialog (Options Flow) |
| Laufend sichtbarer oder automatisierbarer Einzelwert | Integrations-Speicher (Store) + Einstellungs-Entität | HA-Standardaktionen, Dashboard |
| Liste oder Objekt, das die eigene Oberfläche bearbeitet | Integrations-Speicher (Store) | WebSocket; zusätzlich Aktion, wenn Automatisierung sinnvoll ist |
| Komplexes Fachobjekt | eigene Datenbank des Moduls | eigene Aktionen, WebSocket |
| Abweichung je Plan | im Planobjekt der Datenbank | eigene Oberfläche bzw. Schnittstelle |
| Aktueller Gerätewert | Integration des Geräts | vorhandene Entität |
| Gemeinsamer Fakt des Hauses | Haus-Modul `haus` | Entität von `haus` |
| Reine Darstellungsvorliebe | Dashboard- bzw. Benutzerdaten | Oberfläche |
| Einmaliger Vorgang | keine Einstellung | Aktion oder Taste (G-08) |
| Verlauf normaler Entitäten | Recorder | automatisch |
| Fachliche Langzeit- und Lerndaten | Datenbank des Moduls | Fachlogik- und Datenschicht |

Einstellungen einer Integration liegen im Integrations-Speicher, nicht in einer eigenen Datenbank; die Datenbank ist für
Fachdaten (Pläne, Läufe, Lernen). Den Zustand nach einem Neustart nicht über `RestoreEntity` herstellen, wenn der Wert
einen Speicher beim Eigentümer hat.

## Aktion oder WebSocket

| Fall | Schnittstelle |
|---|---|
| Einstellung soll von Automationen, Skripten, Sprache oder den Entwicklerwerkzeugen gesetzt werden | **Aktion** |
| Lesen komplexer Daten für die eigene Karte | **WebSocket** |
| Bearbeiten komplexer Objekte nur in der eigenen Oberfläche | **WebSocket** |
| Vorgang für Oberfläche und Automationen | **Aktion** als öffentlicher Schreibweg, WebSocket höchstens zum Lesen |
| Große oder strukturierte Abfragen (Listen, Pläne, Raumzuordnungen) | **WebSocket** |

Kurz: **Automatisierbarer Befehl → Aktion. Bearbeiten und komplexes Lesen in der eigenen Oberfläche → WebSocket.**

## Kein zweiter Speicher

Aktion und WebSocket dürfen denselben Wert ändern; beide sind nur Transportwege und enden beim selben Eigentümer, der prüft
und speichert:

```text
Karte ───── WebSocket ─┐
                       ▼
Automation ─ Aktion ─► Einstellungs-Dienst (Eigentümer, prüft)
                       │
                       ▼
                 Integrations-Speicher
```

## Erben und leere Listen

Abweichungen je Plan speichern nur, was vom globalen Wert abweicht:

- `null` (nicht gesetzt) → der Plan **erbt** den globalen Wert
- `[]` (leere Liste) → **bewusst leer**, z. B. „für diesen Plan zählt keine Person“

## Auswahl aus HA-Objekten

Eine Auswahl wie „welche Personen zählen für dieses Gerät“ kommt dynamisch aus HA (`person.*`), nicht aus festen Werten.
Gespeichert wird die Referenz (Entitäts-ID). Fehlt eine gespeicherte Person später, wird sie nicht still gelöscht, sondern
als Reparatur-Hinweis gemeldet. Das Haus-Modul `haus` liefert nur Fakten (wer ist da, Arbeitszeit, Prognose); jedes Gerät
wählt selbst, welche Personen für es zählen.

## Bedienort

Jede Einstellung hat **einen bevorzugten Bedienort** (Dashboard, Optionsdialog oder eigene Oberfläche). Andere Wege sind
nicht verboten, sie enden beim selben Eigentümer.
