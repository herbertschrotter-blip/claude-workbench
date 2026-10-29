---
description: "HA nach dem Einspielen abgestimmt neu starten – neustart soll auslösen, code-erstellen und sitzung nicht."
tags: [routing, critical, neustart, code-erstellen, sitzung]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Die neue Integration ist eingespielt. Starte jetzt Home Assistant neu, aber erst, wenn in den anderen Claude-Chats gerade nichts gegen HA läuft, und prüf danach, ob alles wieder hochgekommen ist.
