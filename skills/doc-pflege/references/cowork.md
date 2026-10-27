# Cowork-Chat

Was im Cowork-Chat anders ist als in Claude Code. Modi, Profil und Regeln stehen in `../SKILL.md`; Dateizugriff und
Shell laufen über Desktop Commander (DC) nach cc-steuerung.

## Skill-Profil und Docs lesen

Claude Code liest die `CLAUDE.md` des Repos automatisch. Im Cowork-Chat das Skill-Profil (bzw. das ältere Doku-Profil)
und die Docs per DC lesen.

## Arbeitsverzeichnis

Bei DC-Operationen das Arbeitsverzeichnis nach **cc-steuerung**, Abschnitt „Arbeitsverzeichnis“, ermitteln.

## Branch

Die Shell ist DC: `git branch --show-current` über DC; die Regeln dazu stehen in `../SKILL.md#Grundsätze`.

## Dateien ändern

Änderungen als SUCHE/ERSETZE im Chat oder direkt per DC.
