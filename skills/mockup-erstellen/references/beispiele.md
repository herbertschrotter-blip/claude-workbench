# Beispielwerte BPM und Heidi

Werte aus den Mockup-Profilen von BPM und Heidi. Sie zeigen, wie die Felder gefüllt werden, und gelten als Rückfall für
BPM, wenn dort das Profil fehlt (`../SKILL.md#Voraussetzung: Skill-Profil`). Für jedes andere Projekt gilt nur dessen
eigenes Profil.

## Inhalt

- Profilwerte BPM und Heidi
- Docs laden BPM und Heidi
- Abnahme-Ort
- Commit

## Profilwerte BPM und Heidi

| Feld | BPM | Heidi |
|------|-----|-------|
| Ablage | `Docs/Mockups/<Modul>/NN_Fenster/` | `dreame_x60/mockups/` (flach) |
| Namensschema | `NN_Fenster/NN_Variante.html` (`sitemap.md#Namenskonvention`) | `<thema>.html`, klein, ohne Umlaute; ein Mockup = alle betroffenen Seiten mit Tabs |
| Design-Quelle | `Colors.xaml`, `UI_UX_Guidelines.md`, `WPF_UI_Architecture.md`, `Icons.xaml` | `dreame_x60/card/src/styles/tokens.ts` (`--dx-*`), Designvorgabe „Automotive Dark Bento“ |
| Referenz-Mockup | letztes Mockup im selben Modul | `dreame_x60/mockups/bento.html` |
| Token-Form im HTML | Hex-Werte aus Colors.xaml | CSS-Variablen `--dx-*` mit denselben Werten wie tokens.ts (`:root`-Block); Komponenten-Klassen wie in `bento.html` |
| Ansichten | Desktop | Desktop **und** 390 px (Smartphone) nebeneinander, Tablet wenn Container-Regeln betroffen |
| Sitemap / Klick-Navigation | ja | nein (Tabs in der Datei, keine Kanten) |
| Vorschau | Visualizer (Cowork) | Claude Code: Browser-Bereich (Datei öffnen) oder Datei per SendUserFile; Cowork: Visualizer |
| Abnahme-Ort | `_SITEMAP.md` (Status ✅) | Bauplan Abschnitt 7 (Seitentabelle: „Abgenommen von Herbert am <Datum> (Mockup <Datei>)“) und Notiz in Abschnitt 10; Abweichung zu v1 → PD-Eintrag 10a |
| Commit-Modul | `Docs` | `Doku` |

## Docs laden BPM und Heidi

**Heidi:** `tokens.ts` komplett (alle `--dx-*`), `bento.html` Kopf (`:root`-Block, Layout-Regeln Bento 12/6/1 Spalten,
`dx-nav`-Formen), Bauplan Abschnitt 7 (Seitentabelle) und die Aufgabenkarte des Schritts, für den das Mockup entsteht
(Akzeptanz = was das Mockup zeigen muss). Regel 14 des Bauplans: System-Schriftstapel, keine externen Ressourcen – gilt
auch im Mockup. Design-Entscheidungen: Bauplan Abschnitt 10, PD-Register. Stil-Referenz aus dem Code: Komponente
`src/components/dx-*.ts` + `styles/controls.ts`. Abgelöste Mockups bleiben liegen und werden im Bauplan als „abgelöst
durch <Datei>“ vermerkt (wie `seiten.html` → `bento.html`). Ablage listen: `dreame_x60/mockups/*.html`.

**BPM – Quickload-First-Pass** (Quickload reicht, kein Langform):

| Doc | Zweck | Laden via |
|-----|-------|-----------|
| **UI_UX_Guidelines.md** | Design-Token, Spacing, Komponenten | `github:get_file_contents` → `Docs/Referenz/UI_UX_Guidelines.md` |
| **WPF_UI_Architecture.md** | Token→WPF-Key Mapping, Dialog-Pattern | `github:get_file_contents` → `Docs/Referenz/WPF_UI_Architecture.md` |
| **Colors.xaml** | Aktuelle Farbwerte | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Colors.xaml` |
| **Icons.xaml** | Verfügbare Icon-Keys | `github:get_file_contents` → `src/BauProjektManager.App/Themes/Icons.xaml` |

Dazu `_SITEMAP.md` des Moduls (`Docs/Mockups/<Modul>/_SITEMAP.md`); Stil-Referenz aus dem Code: XAML über GitHub oder DC;
Token-Abgleich gegen Colors.xaml.

## Abnahme-Ort

- **Heidi:** Bauplan Abschnitt 7 (Zeile der Seite: „Abgenommen von Herbert am <Datum> (Mockup <Datei>)“) + Notiz in
  Abschnitt 10 (Art `Befund · Info`); Abweichung zum bisherigen Verhalten → PD-Eintrag 10a mit Status `freigegeben`.
- **BPM:** Sitemap-Status ✅.

## Commit

- Format: `[vX.Y.Z] <Commit-Modul>, Docs: Mockup <Datei> – <Kurztitel>` (BPM: `Docs`, Heidi: `Doku`)
- Version: BPM PATCH; Heidi: reine Doku-Commits behalten die Kartenversion
