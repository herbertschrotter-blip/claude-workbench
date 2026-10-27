# Chat-Anker-System — Master-Spec

**Zweck:** Präzise Rückverfolgung welcher Chat welchen Task ausgelöst/abgeschlossen hat — per Chat-Suche (`conversation_search`) auf eindeutige Anker-Strings. Löst die Chat-URL-Problematik (URL nicht programmatisch auslesbar, Indexierungs-Verzögerung).

**Geltung:** Das Anker-Format im Chat-Body gilt in jeder Umgebung. Die Memory-Registry `[ANKER-LIVE]`, ihr Lifecycle, die TEMP-ID, das Kommando `anker setzen` und der Stale-Check gelten nur im Cowork-Chat (Memory-Werkzeuge und Shell dort: `cowork.md`). In Claude Code gibt es keine Anker-Registry.

**Konzept-Doc:** `docs/chat-anker-konzept.md` im Skill-Repo.

**Hinweis:** Diese Datei ist die Master-Spezifikation. `code-erstellen` (Auto-Anker) und `chat-wechsel` (Übergabe) haben eigene lokale Kopien der für sie relevanten Teile. Bei Änderungen der Spec müssen dort die Kopien mit-gepflegt werden.

## Inhalt

- Anker-Format im Chat-Body
- Memory-Registry `[ANKER-LIVE]`
- Lifecycle
- TEMP-ID Generierung
- Kommando `anker setzen: <text>`
- Stale-Check (am Chat-Start)

Beispiele: `beispiele.md`, Abschnitt „Chat-Anker“.

---

## Anker-Format im Chat-Body

```
[<PRÄFIX>-ANCHOR-<id>] — <typ>: <kurzbeschreibung max 80 Zeichen>
```

- `<PRÄFIX>` ist der Anker-Präfix des Projekts. **Der Präfix wird pro Projekt festgelegt** (Tracker-Config, Quittungsformat).
- `<id>` = `TEMP-<10-char-base32>` (Ausarbeitungsphase, vor Task-Erstellung, nur Cowork-Chat) **oder** ClickUp-Task-ID (Task angelegt bzw. erledigt)
- `<typ>` = `erstellt` | `erledigt`

---

## Memory-Registry `[ANKER-LIVE]`

Live-Liste aller aktiven Anker der aktuellen Session.

**Format:**
```
[ANKER-LIVE] <id>|<typ>|<timestamp>|<kurzbeschreibung>
```

- `<id>` = TEMP-ID oder Task-ID
- `<typ>` = `offen` (temp, kein Task) | `erstellt` | `erledigt`
- `<timestamp>` = ISO `YYYY-MM-DDTHH:MM`
- `<kurzbeschreibung>` = max 60 Zeichen

**Beispiel während Session:**
```
[ANKER-LIVE] TEMP-01JS7KABCD|offen|2026-04-21T18:45|Wetter-Modul GS-Worker
[ANKER-LIVE] 86c9eupfk|erstellt|2026-04-21T19:00|tracker Anker-Logik
```

---

## Lifecycle

| Event | Aktion auf `[ANKER-LIVE]` |
|-------|---------------------------|
| `anker setzen: <text>` | Eintrag mit Typ `offen` hinzufügen |
| `tracker neu` mit vorhandenem TEMP | TEMP-Eintrag **ersetzen** durch Task-ID-Eintrag mit Typ `erstellt` |
| `tracker neu` ohne TEMP | neuer Eintrag mit Typ `erstellt` |
| `tracker done` erfolgreich | **beide Einträge** (erstellt + erledigt wenn vorhanden) entfernen |
| **Batch (≥2 Task-Operationen in einer Antwort)** | Obige Regeln **pro Task einzeln** anwenden — keine Sammelaktualisierung am Batch-Ende. Spec: `batch-protocol.md` |
| `chat-wechsel` | komplette Liste in Übergabeprompt kopieren, dann leeren |

---

## TEMP-ID Generierung

**Format:** `TEMP-<10 Zeichen Crockford-Base32>`

**In der Shell** (Beispiel PowerShell, im Cowork-Chat über die Shell nach `cowork.md`):
```powershell
$ts = [DateTimeOffset]::UtcNow.ToUnixTimeMilliseconds()
$rand = Get-Random -Maximum 1024
"TEMP-" + ("{0:x}{1:x}" -f $ts, $rand).ToUpper().Substring(0, 10)
```

**Fallback (Claude selbst):** Base32-Hash aus `yyMMddHHmm` + Zufallsbuchstaben. Reicht für Session-Eindeutigkeit.

---

## Kommando `anker setzen: <text>`

**Zweck:** Manueller TEMP-Anker in der Ausarbeitungsphase des Chat-Anker-Systems (vor Task-Erstellung). Nutze dieses Kommando wenn die Auto-Keyword-Erkennung im `code-erstellen`-Skill nicht greift aber der User eine Stelle im Chat für späteres Wiederfinden markieren will.

Abgrenzung:
- **Auto-Anker** (code-erstellen): Claude setzt automatisch bei Task-Keywords
- **`anker setzen`** (manuell): User fordert explizit einen Anker

### Trigger-Phrasen

- "anker setzen: <text>"
- "setze einen anker: <text>"
- "anker für <text>"
- "merk dir diese stelle: <text>"

### Ablauf

1. **TEMP-ID generieren** (siehe Abschnitt "TEMP-ID Generierung"):
   - Primär in der Shell
   - Fallback: Claude erzeugt `TEMP-<yyMMddHHmm><3 Zufallsbuchstaben>`
2. **Kurzbeschreibung** aus `<text>` ableiten (max 60 Zeichen, keine Zeilenumbrüche)
3. **Anker-Zeile im Chat schreiben**:
   ```
   [<PRÄFIX>-ANCHOR-TEMP-<id>] — Idee: <kurzbeschreibung>
   ```
4. **Memory aktualisieren**: Eintrag `[ANKER-LIVE] TEMP-<id>|offen|<ISO-timestamp>|<kurzbeschreibung>` hinzufügen
   (Memory-Werkzeug: `cowork.md`)
5. **Bestätigung an User**:
   ```
   ✅ Anker gesetzt: TEMP-<id>
      Thema: <kurzbeschreibung>
      Wird bei `tracker neu` mit Task-ID verknüpft oder bei `chat-wechsel` in Übergabeprompt übernommen.
   ```

### Wann KEIN manueller Anker?

- Beschreibung unter 10 Zeichen (zu vage)
- Mehr als 10 Einträge bereits in `[ANKER-LIVE]` (erst aufräumen per `tracker neu` oder `tracker done`)
- Nahezu identischer Anker existiert bereits in `[ANKER-LIVE]` (Duplikat-Check)

Bei Duplikat: Hinweis auf bestehenden Anker statt neuen zu setzen.

---

## Stale-Check (am Chat-Start)

Am Chat-Start (nach dem Laden des Memory) prüfen ob es veraltete Anker gibt.

**Veraltet** = älter als 24 Stunden, berechnet aus dem `<timestamp>`-Feld jedes `[ANKER-LIVE]`-Eintrags.

### Ablauf

1. **Alle `[ANKER-LIVE]`-Einträge parsen**: 
   - Format: `[ANKER-LIVE] <id>|<typ>|<timestamp>|<kurzbeschreibung>`
   - Timestamp ist ISO `YYYY-MM-DDTHH:MM`
2. **Aktuelle Zeit ermitteln** (ISO via `[DateTimeOffset]::UtcNow` oder Claude-intern)
3. **Differenz berechnen** — wenn älter als 24h → stale
4. **Stale-Liste anzeigen** (nur wenn ≥1 stale):
   ```
   ⚠️ Veraltete Anker in [ANKER-LIVE] (älter als 24h):

   | ID | Alter | Thema |
   |----|-------|-------|
   | TEMP-01JS7KABCD | 3 Tage | Wetter-Modul GS-Worker |
   | 86c9eupfk | 26 Std | tracker-Skill Anker-Logik |
   ```

5. **Per Auswahlfrage** fragen was damit passieren soll:
   ```
   Frage: "Was mit den veralteten Ankern tun?"
   Optionen:
   - "Alle verwerfen (Memory bereinigen)"
   - "Einzeln entscheiden"
   - "Behalten (nur Hinweis)"
   ```
6. **Bei "Alle verwerfen":** Alle stale Einträge aus dem Memory entfernen (`cowork.md`)
7. **Bei "Einzeln entscheiden":** Pro stale Eintrag eine Auswahlfrage mit Optionen:
   - "Verwerfen"
   - "`tracker neu` — Task daraus machen"
   - "Behalten"
8. **Bei "Behalten":** Nichts tun, nur im Chat notiert

### Keine stale Anker vorhanden?

Ausgabe unterdrücken. Kein "Alles OK"-Hinweis — der Chat-Start soll nicht überladen werden.

### Edge Cases

- **Timestamp unparseable** → Eintrag als stale behandeln, im Hinweis markieren ("unbekanntes Alter")
- **Mehr als 10 stale Einträge** → nur die 10 ältesten anzeigen, Gesamtzahl erwähnen
- **Memory nicht lesbar** → Check überspringen (still)
