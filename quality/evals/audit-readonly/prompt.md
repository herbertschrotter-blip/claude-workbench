---
description: "Skills gegen INDEX prüfen, audit soll auslösen, doc-pflege nicht. Seit v0.58.5 deckt die audit-Description die Prüfung einer Index- oder Router-Datei gegen die Beschreibungen ab (audit-001)."
tags: [baseline, routing, pilot, critical, ziel, audit, doc-pflege]
runs: 3
max_turns: 8
timeout_seconds: 180
allowed_tools: [Skill, Read, Glob, Grep]
---

Prüfe bitte, ob die INDEX.md und die Beschreibungen der Skills zusammenpassen. Nur prüfen und die Befunde nennen, nichts
ändern.
