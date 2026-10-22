# Sitemap und Klick-Navigation (Profil „Sitemap: ja“)

Gilt für mockup-erstellen, wenn das Mockup-Profil „Sitemap / Klick-Navigation: ja“ sagt (BPM). Ablage, Design-Quelle,
Workflow und HTML-Regeln stehen in `SKILL.md`.

## Inhalt

- Namenskonvention
- Interaktivität und Klick-Navigation
- Sitemap und Selbstcheck
- Neues Fenster anlegen
- Fenster nachträglich hinzufügen

## Namenskonvention

Verbindlich bei Profil „Sitemap: ja“ (BPM).

### Ordnerstruktur (ab 2026-05)

Jedes Fenster (Screen, Wizard, Dialog) bekommt **einen eigenen Ordner**. Mockup-Dateien
liegen innerhalb dieses Ordners. Damit lassen sich Wizard-Schritte, Tab-Varianten und
Design-Varianten sauber gruppieren.

```
Docs/Mockups/
├── <Modul>/
│   ├── _SITEMAP.md                       ← Navigationskanten (siehe „Sitemap und Selbstcheck“)
│   ├── NN_Fenster/
│   │   ├── NN_Variante.html
│   │   └── ...
│   ├── NN_NaechstesFenster/
│   │   └── ...
│   └── _Archiv/
│       └── ...
└── ...
```

### Schema

```
<Modul>/NN_Fenster/NN_Variante.html
```

| Teil | Beschreibung | Beispiel |
|------|-------------|----------|
| **Modul** | Modulname aus der App | PlanManager, Settings |
| **NN_Fenster** | Ordner pro Fenster, NN = Navigationstiefe (2-stellig) | 01_Projektuebersicht, 04_ProfilWizard |
| **NN_Variante** | Datei innerhalb des Fenster-Ordners. NN = Reihenfolge bei Mehrfach-Files | 01_Hauptansicht, 01_Datei, 05_Erkennung |

### NN-Vergabe für Fenster-Ordner

- **01** — Hauptseite des Moduls (z.B. Projektübersicht)
- **02** — Detail-/Unterseite (z.B. Projektdetail)
- **03+** — weitere Screens, Dialoge, Wizards in der Reihenfolge des Auftretens

### NN-Vergabe für Dateien innerhalb eines Fenster-Ordners

- **Single-Screen-Fenster:** eine Datei, z.B. `01_Hauptansicht.html` oder `01_<Fenstername>.html`
- **Tab-Ansichten:** eine Datei pro Tab, NN entspricht Tab-Reihenfolge
- **Wizard-Schritte:** eine Datei pro Schritt, NN = Schritt-Nummer
- **Design-Varianten während Klärungsphase:** `01_Variante_Kompakt.html`, `01_Variante_Breit.html` — nach Auswahl gelöscht (Memory-Regel: Mockup-Varianten aufräumen)

### Modul-Ordner

Ordnername = Modulname aus der App:
- `PlanManager`
- `Settings` (oder `Einstellungen`, je nach App-Namen)
- `Foto` (wenn Modul gebaut wird)
- `Zeiterfassung` (wenn Modul gebaut wird)
- `Bautagebuch` (wenn Modul gebaut wird)

### Beispiele

```
PlanManager/01_Projektuebersicht/01_Projektuebersicht.html
PlanManager/02_Projektdetail/01_Profile.html
PlanManager/02_Projektdetail/02_ManuellSortieren.html
PlanManager/02_Projektdetail/03_Sync.html
PlanManager/03_ImportVorschau/01_ImportVorschau.html
PlanManager/04_ProfilWizard/01_Datei.html
PlanManager/04_ProfilWizard/02_Segmente.html
PlanManager/04_ProfilWizard/03_Index.html
PlanManager/04_ProfilWizard/04_Zielordner.html
PlanManager/04_ProfilWizard/05_Erkennung.html
PlanManager/_Archiv/00_Gesamtuebersicht.html
Settings/01_Allgemein/01_Allgemein.html
Settings/02_DevTools/01_Log.html
Settings/02_DevTools/02_Reset.html
```

### Sonderregeln

- Keine Umlaute in Ordner- und Dateinamen (ue statt ü, ae statt ä)
- Keine Leerzeichen (Underscore als Trenner)
- Archiv-Ordner: `_Archiv/` mit Unterstrich-Prefix → sortiert ans Ende
- Bestehende einzelne Mockup-Dateien (Legacy-Stand vor 2026-05) werden bei Bedarf in passenden Fenster-Ordner verschoben

---

## Interaktivität und Klick-Navigation

Pflicht bei Profil „Sitemap: ja“ (ab 2026-05).

Alle Mockups werden als **durchklickbarer Prototyp** ausgelegt. Buttons, Tabs, Karten,
Sidebar-Einträge, Wizard-Weiter/Zurück: alles bekommt ein Klick-Ziel.

### Klickbare Elemente

Jedes interaktive Element bekommt:
```html
onclick="location.href='<relativer_pfad>'"
```

Plus visueller Hinweis auf Klickbarkeit (mindestens `cursor:pointer`, idealerweise Hover-Effekt).

### Relative Pfade

Pfade beziehen sich auf den Ordner des aktuellen Mockups:

```
gleicher Fenster-Ordner:     ./<NN_Variante>.html         (z.B. Wizard-Schritt → nächster Schritt)
Geschwister-Fenster:         ../<NN_Fenster>/<datei>.html  (z.B. Projektübersicht → Projektdetail)
Anderes Modul:               ../../<Modul>/<NN_Fenster>/<datei>.html  (z.B. Sidebar Settings)
```

### Tote Pfade (Ziel-Mockup existiert noch nicht)

Wenn das Ziel-Mockup geplant aber noch nicht gebaut ist:

```html
onclick="alert('Mockup folgt: <Fenstername>')"
style="border: 1px dashed #858585; opacity: 0.7;"
```

Plus visueller Hinweis (gestrichelter Rand, reduzierte Deckkraft) — damit User beim
Durchklicken sieht: hier ist Klickbarkeit geplant, aber Ziel fehlt noch.

Tote Pfade werden in der Sitemap mit Status `🟡 tot` markiert (Abschnitt „Sitemap und Selbstcheck“).

### Navigation-Verhalten

- **Gleicher Tab** (Default — natürliche App-Navigation, Browser-Zurück funktioniert)
- Kein `target="_blank"` — Mockups simulieren echte App-Navigation, nicht externe Links
- Sidebar/Modulleisten verlinken zwischen Modul-Ordnern

### Beispiele

**Projektübersicht-Karte klickt zur Detail-Ansicht:**
```html
<div class="projekt-karte" onclick="location.href='../02_Projektdetail/01_Profile.html'">
  ...
</div>
```

**Wizard "Weiter →"-Button:**
```html
<button onclick="location.href='./02_Segmente.html'">Weiter →</button>
```

**Sidebar Settings-Eintrag aus PlanManager-Modul:**
```html
<div onclick="location.href='../../Settings/01_Allgemein/01_Allgemein.html'">⚙ Einstellungen</div>
```

**Toter Pfad (Mockup noch nicht da):**
```html
<button onclick="alert('Mockup folgt: ImportVorschau')"
        style="border:1px dashed #858585;opacity:0.7;">Import starten</button>
```

---

## Sitemap und Selbstcheck

Ab 2026-05, nur bei Profil „Sitemap: ja“.

### `_SITEMAP.md` pro Modul-Ordner

Zentrale Wahrheit für Navigationskanten. Wird bei jedem neuen Mockup gelesen und
nach Mockup-Erstellung aktualisiert.

**Speicherort:** `Docs/Mockups/<Modul>/_SITEMAP.md`

### Format

```markdown
# <Modul> — Sitemap

## Fenster

| Ordner | Status | Datei(en) |
|---|---|---|
| 01_Projektuebersicht | ✅ aktiv | 01_Projektuebersicht.html |
| 02_Projektdetail | ✅ aktiv | 01_Profile.html, 02_ManuellSortieren.html, 03_Sync.html |
| 04_ProfilWizard | 🟡 in Arbeit | 05_Erkennung.html (1-4 fehlen) |

## Navigationskanten

| Quelle | Ziel | Trigger | Status |
|---|---|---|---|
| 01_Projektuebersicht/01_Projektuebersicht.html | 02_Projektdetail/01_Profile.html | Projekt-Karte (Klick) | ✅ |
| 02_Projektdetail/01_Profile.html | 01_Projektuebersicht/01_Projektuebersicht.html | Zurück-Pfeil (←) | ✅ |
| 02_Projektdetail/01_Profile.html | 04_ProfilWizard/01_Datei.html | "+ Neuen Dokumenttyp" | 🟡 tot |
| 02_Projektdetail/01_Profile.html | 04_ProfilWizard/01_Datei.html | "✎ Profil" pro Profil | 🟡 tot |
| 04_ProfilWizard/01_Datei.html | 04_ProfilWizard/02_Segmente.html | "Weiter →" | 🟡 tot |
```

### Status-Symbole

- **✅ aktiv** — beide Mockups existieren, Klick-Navigation funktioniert
- **🟡 tot** — Ziel-Mockup fehlt noch, Aufrufer hat `alert('Mockup folgt: X')`
- **❌ kaputt** — Pfad-Inkonsistenz (z.B. Datei verschoben, Link nicht angepasst)

### Pflege-Pflicht

- **Vor jedem neuen Mockup:** Sitemap lesen
- **Nach jedem neuen Mockup:** Sitemap aktualisieren (neue Kanten ergänzen, tote → aktiv wenn Ziel jetzt da)
- **Bei Umbenennung/Verschiebung:** alle Pfade in Sitemap UND in HTML-onclick-Refs anpassen
- **Bei Mockup-Löschung:** Sitemap-Einträge entfernen, eingehende Kanten auf `🟡 tot` setzen oder Aufrufer-Mockups patchen

### Selbstcheck

Vor Commit:

1. **Sitemap-Kanten vs HTML-onclick-Refs vergleichen**
   - Jede Kante in Sitemap muss als `onclick` im Quell-HTML existieren
   - Jeder `onclick` im HTML muss als Kante in der Sitemap stehen
2. **Datei-Existenz prüfen**
   - Jedes Ziel in `onclick="location.href='...'"` muss als Datei existieren
   - Falls nicht → Kante als `🟡 tot` markieren ODER `alert('Mockup folgt: X')` verwenden
3. **Diskrepanzen melden** statt stillschweigend zu korrigieren — User entscheidet

---

## Neues Fenster anlegen

A+B kombiniert, nur bei Profil „Sitemap: ja“.

Wenn ein komplett neues Fenster (Screen, Wizard, Dialog) angelegt wird, läuft der
Skill folgenden Sub-Workflow ab:

### Schritt 1 — User fragen (B-Mechanik)

Per Auswahlfrage oder Prosa (bei freiem Text-Input):

- **Eingehende Links:** Aus welchen bestehenden Fenstern wird das neue aufgerufen?
  - Liste der vorhandenen Fenster aus Sitemap als Optionen
  - Plus "Keine eingehenden Links" (z.B. neues Hauptmenü)
- **Trigger im Aufrufer:** Welcher Button/Karte/Tab löst die Navigation aus?
  - Freier Text-Input (z.B. "Button 'Neuen Dokumenttyp anlernen'")
- **Ausgehende Links / Zurück-Verhalten:** Wohin kehrt das neue Fenster zurück?
  - Aufrufer (typisch bei Dialogen) | Hauptseite | Anderes Fenster | Nirgends (Standalone)
- **NN-Vergabe:** nächste freie Nummer, oder dazwischen-rücken (dann müssen nachfolgende renamed werden)

### Schritt 2 — Aufrufer-HTMLs patchen (B-Mechanik)

Für jede genannte Eingangs-Quelle:
1. HTML-Datei laden
2. Passende Klick-Stelle suchen (Button-Label, Karte mit bekanntem Text, Tab)
3. `onclick="location.href='<pfad_zum_neuen_fenster>'"` einfügen
4. Falls bisher `alert('Mockup folgt: X')` mit dem genauen Fenster-Namen drin war → ersetzen

### Schritt 3 — Neues Mockup erstellen

Standard-Workflow (`SKILL.md`, Abschnitt „Workflow“) für das neue Fenster:
- Stil-Referenz: bestehende Mockups im selben Modul
- Klick-Navigation: Zurück-Pfeil/Schließen-Button mit `onclick` zum angegebenen Rückkehr-Ziel
- Tote Pfade für noch nicht existente Folge-Mockups

### Schritt 4 — Sitemap aktualisieren (A-Persistenz)

`_SITEMAP.md` patchen:
- Neuen Fenster-Eintrag in "Fenster"-Tabelle
- Neue Kanten in "Navigationskanten"-Tabelle (eingehend + ausgehend)
- Status entsprechend: `✅` wenn beide Seiten existieren, `🟡 tot` wenn Ziel/Quelle fehlt

### Schritt 5 — Tote Pfade scannen

In allen HTML-Files des Moduls nach `alert('Mockup folgt: <neues_fenster>')` suchen:
- Wenn gefunden → durch echten `location.href`-Link ersetzen
- Sitemap-Status entsprechend von `🟡 tot` auf `✅` aktualisieren

### Schritt 6 — Selbstcheck

Abschnitt „Sitemap und Selbstcheck“ — Sitemap-Kanten vs HTML-onclick-Refs vergleichen, Datei-Existenz prüfen.

---

## Fenster nachträglich hinzufügen

Nur bei Profil „Sitemap: ja“.

Wenn ein Fenster nachträglich (nach mehreren bereits gebauten Mockups) hinzugefügt
wird, gilt der gleiche Workflow wie „Neues Fenster anlegen“, plus:

### Zusatz-Schritt — Bidirektionalität prüfen

Beim nachträglichen Einfügen verändern sich oft auch **bestehende Navigationsflüsse**:

- Bestehendes Fenster A ruft jetzt zusätzlich das neue Fenster N auf
- Bestehendes Fenster B verlinkt evtl. auf N statt auf altes Fenster C
- Sitemap-Reorganisation möglich (NN-Vergabe)

**Aktion:** Per Auswahlfrage fragen ob bestehende Flüsse angepasst werden müssen.

### NN-Reorganisation (Vorsicht)

Falls die NN-Vergabe geändert werden soll (z.B. neues Fenster zwischen alten 02 und 03
→ alle ab 03 hochrücken):

- ALLE Mockup-Ordner umbenennen
- ALLE relativen Pfade in allen `onclick="location.href='...'"` anpassen
- Sitemap komplett neu pflegen

Das ist aufwendig. **Default:** neue Nummer am Ende vergeben (z.B. 06_NeuesFenster),
auch wenn es thematisch zwischen 02 und 03 gehört. Sitemap stellt den logischen Fluss
ohnehin separat dar.

### Sitemap-Cleanup auch hier

Wie in „Neues Fenster anlegen“, Schritt 5: tote Pfade auf das neue Fenster scannen und ersetzen,
Sitemap-Status nachziehen.
