# Gesamtabnahme der Skills (Oktober 2026)

Messung für Phase 7 des Umbaus (`docs/skillsystem-umbau.md`): alle Fälle aus `quality/evals/` mit den umgebauten
Skills nach Phase 6, je drei Läufe. Vergleichsbasis ist die Grundmessung
(`grundmessung-2026-09.md`).

`claude plugin eval quality --runs 3 --ablation none --no-publish --trust-plugin`

- Lauf am 28.10.2026 ab 11:54 auf dem HA, Claude Code 2.1.311; 6661 Sekunden, Gegenwert zum Listenpreis 64,52 USD
  (Max-Abo, keine Rechnung).
- Ergebnisse: `quality/evals/results/2026-10-28T10-54-12-815Z/` (nicht im Repo).

## Ergebnis

- **114 von 114 Fällen bestanden, 341 von 342 Läufen (99,7 %).** Grundmessung: 55 von 60 Fällen, 172 von 180 Läufen
  (95,6 %).
- **Kritische Fälle: 34 von 34 mit 3/3.** Grundmessung: 20 von 23.
- Einzige Abweichung: `doc-pflege-real-uebergabe-bauplan` (normal, Tag `real`) mit 2/3, wie schon vor der Messung;
  bestanden nach der Schwelle von 2/3.
- Kein bisher bestandener Negativfall ist gekippt.

## Echte Sitzungen

Konflikte mit Skills von Anthropic, am selben Tag gemessen: EXT-01, EXT-02, EXT-03 und EXT-05 je 3/3 (12 von 12
Sitzungen). Protokoll: `quality/real-environment/2026-10-28.md`.

## Nacharbeit nach der Messung

Für die Neutralisierung der Kerne wurden danach fünf Stellen geprüft:

- audit v0.62.8, chatgpt-review v0.62.10 und mockup-erstellen v0.62.12: Ohne Profil schlägt der Skill Werte aus dem
  Repo vor und fragt nach, statt auf BPM-Werte zurückzufallen. Bei mockup-erstellen nennt die Description jetzt das
  Skill-Profil.
- sitzung v0.62.13: Beispiel ohne Projektnamen.
- code-erstellen: Das Beispiel „mach AB-002“ statt „mach BSM-002“ in der Description senkte den echten Fall
  `code-erstellen-real-weiter-mit` auf 1/3. Die Änderung ist zurückgenommen (v0.62.14), „BSM-002“ bleibt dort als
  Beispiel.
- chat-wechsel: keine Änderung nötig.

Die Fälle der geänderten Skills liefen danach erneut mit `--tag`; mockup-erstellen bestand 16 von 16 Fällen mit 3/3.
Alle Änderungen sind bei claude.ai hochgeladen und am 29.10.2026 gegen den Repo-Stand geprüft.
