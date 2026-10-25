# Cowork-Chat

Was im Cowork-Chat anders ist als in Claude Code. Ablauf, Profil und Regeln stehen in `../SKILL.md`; Dateizugriff und
Shell laufen über cc-steuerung (Abschnitt „Arbeitsverzeichnis“ dort).

## Inhalt

- Docs und Ablage lesen
- Vorschau
- Speichern
- Visualizer-Variablen

## Docs und Ablage lesen

- Designquelle, Referenz-Mockup und Doku über DC `read_file` oder `github:get_file_contents` lesen.
- Ablage listen: `list_directory` → `<Ablage>/<Modul>/`; Sitemap: `read_file` → `<Ablage>/<Modul>/_SITEMAP.md`.

## Vorschau

- Mockup als **Visualizer** (show_widget) im Chat anzeigen.
- User bestätigt oder gibt Änderungswünsche; iterieren bis der User zufrieden ist.

## Speichern

- Via DC `write_file` in `<workFolder>/<Ablage>/…`.
- Erst, wenn der User DC ausdrücklich auslöst („dc“, „cc“, „auf platte“, „speichern“) – nie vorher.

## Visualizer-Variablen

- Der Visualizer nutzt eigene CSS-Variablen (`--color-background-primary` etc.) – die dürfen nie ins gespeicherte Mockup.
- Nie das Visualizer-HTML direkt speichern; das Mockup trägt die Tokens der Designquelle des Projekts.
