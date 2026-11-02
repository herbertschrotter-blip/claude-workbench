# Seitenliste

Standard für alle Projekte mit Oberfläche: eine maschinenlesbare Quelldatei mit einer Zeile je Seite oder Formular,
daraus erzeugt eine Doku und eine veröffentlichte Seite. Dateien und Befehle kommen immer aus dem Skill-Profil
(`Mockup.Seitenliste`, `Mockup.Theme`, `Mockup.Beziehungen`, `Mockup.Pruefung`, `Mockup.Datenliste`), Suchmuster aus der Config der Werkzeuge.

## Inhalt

- Wann sie gilt
- Prüfen und nachträglich anlegen
- Quelldatei
- Versionen
- Aktualisieren
- Theme-Abgleich
- Veröffentlichte Seitenliste
- Mockups und Theme
- Dev-Schalter
- Altes Mockup übernehmen
- Vorschau
- Abnahme
- Datenliste
- Abgleich
- Werkzeuge

## Wann sie gilt

Ein Projekt hat eine Oberfläche, wenn `Mockup.Ablage` nicht `none` ist. Ohne Oberfläche stehen die Felder auf `none`. Steht `Mockup.Seitenliste` bei einem Projekt mit Oberfläche auf `none`, ist
es bewusst ausgenommen: Es gilt die bisherige Arbeitsweise, und es kommt keine Frage.

## Prüfen und nachträglich anlegen

Gilt für mockup-erstellen, code-erstellen, ticket, doc-pflege und projekt-anlegen, sobald sie in einem Projekt mit
Oberfläche arbeiten. audit meldet Fehlendes nur.

1. Stehen die Felder im Profil und gibt es die Dateien, im Format dieser Reference?
2. Fehlt etwas: sagen, was fehlt, und per Auswahlfrage „Jetzt anlegen (Empfehlung)“ / „Nach dieser Aufgabe anlegen“ /
   „Dieses Projekt ausnehmen“ (alle Felder werden im Profil `none`). Eine laufende kleine Aufgabe wird davon nicht
   blockiert. „Nach dieser Aufgabe anlegen“ gilt für die Sitzung: Es kommt am Ende der Aufgabe wieder, nicht in jedem Skill.
3. Anlegen, unter mockup-erstellen (Skill laden, die Dateien liegen in der Ablage):
   - zuerst die Felder ins Profil: Erzeuger, Vorlagen und Check gehören in `Mockup.Seitenliste`, sonst blockt der Skill-Wächter
   - Seiten aus dem Code ermitteln, Nummern vergeben, alle auf Version 0.1, außer der User nennt Überarbeitetes
   - vorhandene Mockups als `mockup_alt` zuordnen
   - Werkzeuge aus `../assets/seitenliste/` übernehmen und an den Stack anpassen (Abschnitt „Werkzeuge“)
   - hat das Projekt einen Datenspeicher: Datenliste anlegen (Abschnitt „Datenliste“), Tabellen und Speicherorte einordnen;
     ohne Datenspeicher `Mockup.Datenliste: none`
   - Check in `Code.Tests` und `Commit.Pre-Commit-Checks`, `Commit.Doku-Check` um „Seite geändert →
     Quelldatei; Schema oder Speicherort geändert → Datenliste“ ergänzen
   - nach dem ersten Commit Listen-Befehl mit `--start`, Seitenliste veröffentlichen (Abschnitt „Vorschau“)

Nichts ohne Bestätigung am Code der App ändern.

## Quelldatei

Eine Liste von Bereichen (`nr`, `bereich`, `seiten`). Je Seite:

| Feld | Inhalt |
|---|---|
| `nr` | fester Ort, z. B. `2.3` (Bereich.Seite), nicht die Version. Bleibt für immer; neue Seiten bekommen die nächste freie Nummer im Bereich. Sagt der User „ändere 2.3“, ist diese Seite gemeint |
| `name`, `art` | Name; Seite, Blatt, Formular oder Vollbild |
| `code` | Dateien, mit Komma getrennt, relativ zu `code_wurzel` der Config |
| `schluessel` | Bezug auf das Code-Element, z. B. `blatt:rechnung`; Variante mit `#` |
| `version_mockup`, `version_code` | getrennt geführt, jede Änderung zählt hoch (Abschnitt „Versionen“) |
| `version_abgenommen` | letzte abgenommene Mockup-Version; weiter als `version_code` = abgenommen, aber noch nicht gebaut. Fehlt das Feld, gilt `version_mockup` |
| `mockup`, `mockup_alt` | Mockup je Seite bzw. älteres Mockup je Thema, relativ zur Ablage |
| `verlauf` | je Version `v`, `datum`, `was`, `ticket`, dazu `art` (code oder mockup) und `commit` |
| `zu` | Verbindungen zu anderen Seiten; „Kommt von“ wird daraus berechnet |
| `nutzt` | gemeinsame Bausteine |
| `code_stand` | Fingerabdruck der Code-Dateien, gesetzt mit `--abnahme <nr>` des Listen-Befehls, wenn der Code gebaut ist |
| `stand_commit` | Commit, bis zu dem die Seite abgeglichen ist |

## Versionen

1.0 = überarbeitet und abgenommen, 0.1 = noch nicht durchgegangen. Kleine Änderung +0.1, Neugestaltung +1.0.

Jede Änderung an einer Seite ist eine neue Version: `version_code` oder `version_mockup` zählt für sich +0.1 hoch. Die
Nummer läuft ohne Überlauf weiter (0.9, 0.10), denn eine neue Hauptnummer entsteht nur durch die Abnahme oder durch die
Entscheidung „Neugestaltung“. Eine Mockup-Version gilt erst mit `version_abgenommen` als abgenommen; gebaut werden nur
abgenommene Stände.

## Aktualisieren

Auslöser: „aktualisiere Seitenliste“ (auch „Seitenleiste“), dazu automatisch nach der Auslieferung in code-erstellen und
beim Schließen eines Tickets. Die Liste wird abgeglichen, nicht neu aufgebaut: Seiten ohne Änderung bleiben unberührt.
Das Skript liefert Fakten und schreibt, Claude liest und bewertet.

1. Erster Lauf eines Projekts: Listen-Befehl mit `--start`. Das setzt `stand_commit` und `version_abgenommen`. Commits davor
   werden nicht nachgeholt; meldet der Check einen geänderten Fingerabdruck, gibt es dafür einmalig eine Sammelversion.
2. Listen-Befehl mit `--offen`: je Seite die Commits seit `stand_commit`, getrennt nach Code und Mockup, dazu `gemeinsam`
   (Dateien mehrerer Seiten) und `nicht_committet`. Nicht Committetes zählt nicht: zuerst committen. Bei vielen Commits
   vorher die Zahl nennen.
3. Je Commit den Diff lesen und entscheiden:
   - **Eine echte Änderung ist eine Version.** Ein Commit und seine Nachbesserung ergeben zusammen eine Version; reine
     Formatierung und Commits, die schon im Verlauf stehen (Abnahme), ergeben keine.
   - **Gemeinsame Dateien:** Nur Seiten, deren Teil der Diff wirklich ändert, bekommen eine Version. Bleibt das unklar,
     bekommen alle eine, mit „gemeinsame Datei“ im Text.
   - **Theme und Bausteine:** Eine Änderung dort zählt nicht je Seite; sie steht im Verlauf der betroffenen Seite nur, wenn
     sich deren eigene Datei ändert.
   - **Text:** `was` beschreibt die Änderung in Klartext aus Sicht der Seite, nicht den Commit-Titel.
   - **Gebaut:** Setzt der Commit einen abgenommenen Stand um, trägt der Eintrag `"gebaut": true`; dann zieht `version_code`
     auf `version_abgenommen` nach, statt +0.1 zu zählen.
4. Die Einträge als JSON-Liste in eine Datei im Scratchpad schreiben, in der Reihenfolge der Commits, und mit `--eintragen
   <datei>` übernehmen. Je Eintrag `nr`, `art`, `was`, dazu `datum` und `commit` aus Schritt 2, wo vorhanden `ticket`. Der Befehl
   zählt die Versionen, schreibt die Mockup-Version in die Datei, setzt `code_stand` und `stand_commit` aller Seiten.
   Versionsnummern, Hashes und erzeugte Dateien nie von Hand ändern.
5. Theme-Abgleich (nächster Abschnitt) und Befehl aus `Mockup.Beziehungen`. Ist `dev_versionen` gesetzt und hat sich eine
   Code-Version geändert: neu bauen, das Gebaute kommt in den Commit aus dem nächsten Schritt, danach `Code.Auslieferung`
   (Abschnitt „Dev-Schalter“).
6. Check aus `Mockup.Pruefung`, Commit mit `Seitenliste aktualisiert` im Kurztitel (diese Commits zählt `--offen` nicht
   mit), Seitenliste veröffentlichen (Abschnitt „Vorschau“), danach sagen: welche Seiten, welche Versionen, welche Zuordnung
   unsicher war.

Der Lauf geht nur in einer Sitzung. Änderungen von anderswo holt der nächste Lauf nach, weil die Commits da sind.

## Theme-Abgleich

Sucht feste Werte in den Dateien der Seiten: Farben und die Eigenschaften aus `themeabgleich` der Config, außerhalb von
`var(--…)`. Dateien des Themes bleiben draußen. Die Hinweise blockieren nichts.

1. `tools/themeabgleich.py` gibt die Treffer je Seite als JSON aus; `token` nennt den Token mit genau diesem Wert.
2. Bewerten: Fehlalarme streichen; ein Treffer mit `token` ist sicher ein Befund, einer ohne eine Entscheidung (neuer Token
   oder begründet lassen, `grund` nennt die Begründung). Berechnete Werte im Code prüfen, die das Muster nicht sieht.
3. Das Ergebnis mit `--uebernehmen <datei>` schreiben, dann den Listen-Befehl ausführen. Die Zeilennummern altern, darum läuft der Abgleich bei
   jedem Aktualisieren neu; ohne Treffer bleibt ein leeres `{}`.

Behoben werden die Werte nur auf Auftrag, unter code-erstellen bzw. mockup-erstellen. Der Abgleich ersetzt nicht den
Token-Abgleich vor dem Speichern eines Mockups.

## Veröffentlichte Seitenliste

Erzeugt aus `seitenliste_vorlage.html`:

- Liste mit Nummern, leichter Baumlinie, Chips M und C, Suche nach Nummer, Name oder Baustein, Filter Alle, Offen, Fertig,
  Nicht gebaut
- mit Theme-Hinweisen: Chip T mit der Zahl, Filter Theme, aufklappbarer Hinweis je Seite und für alle Seiten, jeweils mit
  „Prompt kopieren“ und dem Prompt in einem Textfeld, falls die Zwischenablage gesperrt ist
- Reiter Seiten und Daten, wenn es eine Datenliste gibt
- Haben Mockup und Code einer Seite beide eine Version und sind sie ungleich, sind beide Chips rot und die Zeile ist rot
  gerahmt und hinterlegt; beim Abdunkeln bleibt sie gut sichtbar, der Kopf erklärt es („rot: M und C ungleich“). Seiten ohne
  Mockup oder ohne Code bleiben normal. Rot heißt nur ungleich, auch wenn der Code weiter ist als das Mockup
- Knopf „Gesamt“ für den offenen Reiter: Vollbild mit allen Seiten bzw. Tabellen je Bereich und allen Verbindungen als
  Linien. Antippen hebt die Seite samt Nachbarn und Linien hervor, zeigt „kommt von n · geht zu n“ und „Öffnen ›“ zur
  Fokus-Ansicht. Rote Seiten bleiben rot
- Fokus-Ansicht: gewählte Seite in der Mitte, Kommt von und Geht zu mit Pfeilen, ab 7 Nachbarn „+ n weitere“, der Weg
  bleibt oben stehen; am Desktop neben der Liste, am Handy als eigene Ansicht
- Mockups öffnen in einem eigenen Fenster per fetch und `srcdoc` mit `base`, weil Seitenlinks im Rahmen der
  Veröffentlichung nicht zuverlässig gehen. Wechsel zwischen Mockups per `postMessage` über die Liste.

## Mockups und Theme

- Je Seite oder Formular eine Datei in der Ablage. Sie enthält nur Inhalt und Zustände; Bausteine kommen aus dem Theme.
- Vor dem Mockup die Seitenliste lesen. Gibt es die Seite schon, wird nur ihre Datei geändert, ohne neues Mockup und ohne
  die Auswahlfrage Archivieren/Überschreiben.
- Eine neue Seite kommt vor der Vorschau in die Quelldatei, ohne `code` und `version_code`, danach läuft der Befehl aus
  `Mockup.Seitenliste`. Der Abgleich nimmt sie aus, bis der Code steht.
- Vor einer Änderung an einem Baustein über `nutzt` nennen, welche Seiten sich mitändern.
- Ein Baustein, den mehrere Seiten nutzen, wird im Theme geändert, nie in eine Seite kopiert.
- Das Theme wird, wo möglich, aus den Stilen der App erzeugt und nie von Hand geändert: Stile in der App ändern
  (code-erstellen), dann den Befehl aus `Mockup.Theme` ausführen. Kann ein Stack das nicht, liegt es von Hand gepflegt in
  einer Datei.
- Seiten brauchen die Theme-Dateien und sind deshalb nicht allein öffenbar (`../SKILL.md#Standalone-fähig`).
- Der Token-Abgleich entfällt für erzeugte Theme-Dateien. Er gilt für alles, was in der Seite oder im von Hand gepflegten
  Theme-Teil steht.
- Interaktiv heißt: Seiten, Zustände und Hauptknöpfe sind klickbar, Knöpfe führen zur nächsten Seite. Keine echte Logik.
- Die Pflichtansichten aus `Mockup.Ansichten` sind umschaltbar, Nummer und Version stehen in der Vorführleiste.
- Jedes Mockup zeigt Nummer und Version der Seite unten links im Rahmen (`theme.js`), immer und ohne Schalter.
- Ältere Mockups bleiben liegen. Eine Seite wandert erst um, wenn sie dran ist (Abschnitt „Altes Mockup übernehmen“); das
  alte Mockup wird dann am Abnahme-Ort als abgelöst vermerkt.

## Dev-Schalter

Standard für alle Projekte mit Oberfläche (`Mockup.Dev-Schalter`; `none` nimmt ein Projekt bewusst aus). Der Schalter blendet
Entwicklerhilfen ein, ist ab Werk aus und gilt nur für das Gerät (im Web `localStorage`, ohne Speicher bleibt er aus). Er
steht im Menü der App, in ha-hausbau unter ☰ Mehr, und braucht keine Rechte.

- **Erste Hilfe:** Nummer und Version der Seite unten links in jedem Fenster und Formular, nur bei Dev AN und an einer
  zentralen Stelle der App, nicht je Seite. Format wie im Mockup, z. B. `1.4 v2.1`. Das Programm zeigt `version_code`, das
  Mockup `version_mockup`.
- **Herkunft:** Die Anzeige holt die Werte über den Schlüssel der Seite aus der Datei `dev_versionen`. Der Listen-Befehl
  erzeugt sie aus der Quelldatei, der Abgleich meldet sie als veraltet. Fenster ohne Eintrag zeigen die Version des Programms.
- **Neu bauen:** Die Seitenversion entsteht erst nach dem Commit (Abschnitt „Aktualisieren“). Darum wird nach jedem
  Listen-Nachtrag neu gebaut und ausgeliefert; ohne das zeigt das Programm die alte Nummer. Die Bauergebnisse gehören
  nicht in `code` einer Seite, sonst meldet der Abgleich den Fingerabdruck als geändert.

## Altes Mockup übernehmen

Ein älteres Mockup je Thema wird zur Seite der Seitenliste, wenn seine Seite dran ist oder der User es sagt:

1. Die Seite aus dem alten Mockup heraus neu in der Ablage anlegen, mit Bausteinen aus dem Theme. Die alte Datei bleibt
   unberührt, auch wenn sie mehrere Seiten zeigt; jede Seite bekommt ihre eigene Datei, nur mit ihrem Teil.
2. Klickziele des alten Mockups übernehmen: Knöpfe führen mit `Mockup.geh` zur neuen Datei der Zielseite. Hat das Ziel noch
   keine eigene Datei, führt der Knopf zu seinem alten Mockup (`Mockup.geh('../<datei>')`).
3. In die Quelldatei eintragen: `mockup` setzen, `mockup_alt` bleibt als Herkunft stehen. Die Verlinkungen kommen nach `zu`:
   den Befehl aus `Mockup.Beziehungen` ausführen und Wege, die der Code nicht zeigt, unter `hand` der Config ergänzen. Fehlt
   die Seite noch in der Liste, bekommt sie die nächste freie Nummer.
4. Sieht die Seite aus wie vorher, bleibt `version_mockup`, im Verlauf steht „aus altem Mockup übernommen“ unter dieser
   Version. Ändert sie sich, zählt die Version nach Abschnitt „Abnahme“.
5. Befehl aus `Mockup.Seitenliste` ausführen, Vorschau wie unten. Nach der Abnahme das alte Mockup am Abnahme-Ort als
   abgelöst vermerken, die Datei selbst nicht ändern.

## Vorschau

Nicht als einzelne Datei senden: Eine Seite ohne Theme zeigt nichts Richtiges. Die Seitenliste samt Seiten und Theme mit
dem Werkzeug der Umgebung veröffentlichen (die Seitenliste als Seite, Seiten und Theme als ihre Dateien, die relativen
Pfade bleiben gleich), den Link als `link` in die Config schreiben und nennen. Cowork: [cowork.md](cowork.md#vorschau).

## Abnahme

Zusätzlich zu `../SKILL.md#Abnahme festhalten`:

1. `version_mockup` von der höheren der beiden Versionen aus hochzählen (Abschnitt „Versionen“) und Verlauf ergänzen.
2. Befehl aus `Mockup.Seitenliste` mit `--abgenommen <nr>` ausführen.
3. Eintrag am Abnahme-Ort, nur für diese Seite.

Quelldatei, erzeugte Dateien und Abnahme kommen in denselben Commit. Damit steht die Version fest; code-erstellen zieht
danach `version_code`, `code_stand` und Verlauf über „Aktualisieren“ nach.

## Datenliste

Reiter „Daten“ der Seitenliste, eigene Quelldatei und Doku (`Mockup.Datenliste`). Nummern `D1.1` für Tabellen, `S1.1` für
Speicherorte (Einstellungen, Dateien, Browser, Speicher). Je Eintrag Zweck, Felder, Verknüpfungen, genutzt von Seiten.

- Der Aufbau kommt aus einem frisch erzeugten, leeren Schema, nie aus echten Daten; die Liste zeigt nur Aufbau, keine
  Inhalte.
- Zweck, Bereiche, Speicherorte und zugehörige Seiten stehen in der Config unter `daten`. „Genutzt von“ gilt für den
  Bereich; ein Eintrag der Quelldatei kann mit eigenem `seiten` abweichen.
- Bei Projekten ohne Datenspeicher ist das Feld `none`, der Reiter fehlt dann.

## Abgleich

Check des Projekts (`Mockup.Pruefung`), Teil von `Code.Tests`, blockiert den Commit:

- jede Seite im Code steht in der Liste und umgekehrt
- Nummern sind eindeutig
- Verbindungen, Dateien und Mockups sind vorhanden
- Versionen in Liste, Verlauf und Mockup stimmen
- Theme und Liste sind neu erzeugt
- neue Tabelle oder Schema-Änderung ohne Eintrag ist rot; Datenliste und ihre Doku sind neu erzeugt, ihre Seiten gibt es

- `version_abgenommen` liegt nicht über `version_mockup`
- die Datei `dev_versionen` ist neu erzeugt

Ein geänderter Fingerabdruck ohne neue Version ist nur ein Hinweis, die Theme-Hinweise ebenso: Die Version entsteht erst aus dem fertigen Commit, darum kann der Check sie nicht sperren. Bekannte Grenze: Varianten mit `#` zählen nur als
„Hauptseite gibt es“.

## Werkzeuge

Vorlagen unter `../assets/seitenliste/`; sie kommen nach `tools/` des Projekts bzw. in die Ablage. Bei claude.ai liegen sie
nicht vor; angelegt wird in Claude Code.

| Datei | Zweck | Anpassen |
|---|---|---|
| `seitenliste.config.json` | alle Projektwerte der Werkzeuge: Pfade, `titel`, `start`, `link`, `dev_versionen` (Datei für den Dev-Schalter, `.json` oder JavaScript; ohne Schlüssel keine), `theme`, `seiten_im_code` (Muster, die Seiten im Code finden), `themeabgleich` (`ziel`, `token`, `eigenschaften`, `ausnahmen`), `beziehungen` (Einstieg, Ziele, Handwege, Bausteine), `daten` (Datenliste; fehlt der Schlüssel, gibt es keinen Reiter) | ganz |
| `seitenliste.py` | erzeugt Doku und Seite, `--abnahme <nr>` setzt `code_stand`; `--start`, `--offen`, `--eintragen`, `--abgenommen` (Abschnitt „Aktualisieren“) | nichts |
| `seitenliste_vorlage.html` | veröffentlichte Seite | nichts |
| `seitenbeziehungen.py` | schreibt `zu` und `nutzt` aus dem Code | nichts |
| `themeabgleich.py` | Treffer und `--uebernehmen` (Abschnitt „Theme-Abgleich“) | nichts |
| `seitenliste_check.py` | Abgleich, braucht Python und die Laufzeit des Theme-Befehls | nichts |
| `datenliste.py` | erzeugt Quelldatei und Doku der Datenliste | nichts |
| `schema_leer.py` | gibt das leere Schema als JSON aus, Vorlage für SQLite | `leere_datenbank`; andere Speicher: eigenes Skript mit derselben Ausgabe |
| `theme.js`, `seite.html` | Vorführleiste und Muster einer Seite, für die Ablage | `ANSICHTEN` aus `Mockup.Ansichten`, Pfade |
| `mockup_theme.mjs` | Theme aus den Stilen, Vorlage für Lit | Pfade; andere Stacks: eigener Befehl oder Theme von Hand |

Profilwerte, Beispiel: [beispiele.md](beispiele.md#seitenliste-ha-hausbau).
