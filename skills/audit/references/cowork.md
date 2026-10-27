# audit im Cowork-Chat

Gilt nur im Cowork-Chat, wenn audit über Desktop Commander (DC) auf das Repo zugreift. Was audit prüft, steht in
`../SKILL.md`; wie DC arbeitet, regelt cc-steuerung. audit bleibt auch hier read-only.

## Inhalt

- Arbeitsverzeichnis
- Dateien auflisten und suchen
- Shell für den Branch

## Arbeitsverzeichnis

Bei DC-Operationen Arbeitsverzeichnis nach **cc-steuerung**, Abschnitt „Arbeitsverzeichnis“, ermitteln.

## Dateien auflisten und suchen

- Existenz: DC `list_directory`
- Inhalt: DC `start_search`

## Shell für den Branch

Ohne Skill-Profil ist DC die Shell für `git branch --show-current` (`../SKILL.md#Grundsätze`, Branch).
