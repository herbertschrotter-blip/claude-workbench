# CGR-2026-10-13-ha-grundsatz — Langzeitarchiv eigener Integrationen (Vorschlag G-24)

**Thema:** `ha-grundsatz` – einheitliches Langzeitarchiv für Ereignisse, Sitzungen und Ergebnisse aller eigenen
HA-Integrationen, damit später eine Auswertung über alle möglich ist. Anlass: Ticket WU-0002 in `ha-netzwerk`
(Verbindungs-Log mit allen Daten zum Auswerten).
**Zeitraum:** 2026-10-13
**Branch:** `main`
**Weg:** codex
**Codex-Thread:** 01a135f0-04fd-7b72-b015-a0ee4abab069
**Websuche:** live
**Status:** Abgeschlossen (13.10.2026)
**Ergebnis:** Regel G-24 Langzeitarchiv festgelegt, Konzept [`docs/ha-grundsatz/archiv.md`](../../ha-grundsatz/archiv.md) Fassung 3

---

## Runden-Übersicht

### Runde 1 — Entwurf `docs/ha-grundsatz/archiv.md`
- **Artefakte:** [r1/](./r1/)
- **Fokus:** Zwei-Schichten-Ansatz, Format JSONL je Monat, Arten-Katalog in `module.yaml`, Schreiben, Datenschutz,
  Verhältnis zu G-10 und zum Community-Weg (Langzeitstatistik, VictoriaMetrics/Grafana)
- **Kernergebnis:**
  - Grundansatz bestätigt; die Abgrenzung lautet „normaler Verlauf“ (Recorder) vs. „fachlicher Vorgang“ (Archiv).
  - Feldsatz ergänzt: `id`, `instanz`, `art_v`, `erfasst`, `ersetzt`, `herkunft`; Zeiten in UTC, Monatsdatei nach
    Schreibzeit, `schema/` im Archiv.
  - Gerätekennungen mit HMAC; Schreiber je Domain.
  - Herbert: ein kurzes, dokumentiertes Verlustfenster statt Pflicht zur Vormerk-Kette.

### Runde 2 — Fassung 2, Sitzungsform
- **Artefakte:** [r2/](./r2/)
- **Fokus:** Sitzungsform A/B/C für Herbert erklärt; Fassung 2 auf Fehler und Prüfbarkeit; Freigabe
- **Kernergebnis:**
  - Variante A (Beginn – Signal nach jedem Abruf – Ende), von Herbert gewählt.
  - Verlustfenster prüfbar mit Frist und Ausfallregel (`archiv.luecke`).
  - Unveränderliche Schemas `(art, art_v)`, `erfasst` bei Wiederholung gleich.
  - Nachtrag-Dateien bei Uhrsprung; ehrliche Kennzeichnung nachgetragener Stundenwerte.
  - G-24 abnahmefähig.

## Ergebnisse

- Regel **G-24 Langzeitarchiv** in [`docs/ha-grundsatz/README.md`](../../ha-grundsatz/README.md); Konzept
  [`archiv.md`](../../ha-grundsatz/archiv.md); `module-yaml.md` um `archive:` und `storage: archiv` erweitert.
- Offen (Bau): Baustein `archiv` in projekt-anlegen samt Validator und Zeile in der audit-Tabelle; danach Netzwerk als
  erste Integration (Ticket WU-0002 in `ha-netzwerk`).
