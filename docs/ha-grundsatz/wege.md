# Wege

Wie ein HA-Vorhaben vom Auftrag bis zur Abnahme läuft. Der Weg wächst mit der Ausbaustufe
([`README.md`](./README.md#ausbaustufen)).

## Inhalt

- Reihenfolge beim Planen
- Kurzer Weg (Stufe 0–1)
- Voller Weg (ab Stufe 2)
- Einspielen

## Reihenfolge beim Planen

Nicht mit „Welche Entitäten brauchen wir?“ anfangen, sondern:

```text
Welches Problem?
      ↓
Welche Werte gibt es?
      ↓
Wem gehört jeder Wert?
      ↓
Welche Werte hat HA schon?
      ↓
Welche Fähigkeiten bietet HA schon?
      ↓
Welche neue Fachlogik bleibt übrig?
      ↓
Wie wird sie nach außen dargestellt?
```

So zeigt sich früh, wenn mehrere geplante Entitäten, Dateien oder Tabellen dasselbe fachliche Datum meinen (G-01).

## Kurzer Weg (Stufe 0–1)

1. **Auftrag:** Was soll funktionieren?
2. **Bestand:** Was kann HA schon (G-02)?
3. **Vertrag:** Welche Quellen, Zustände, Einstellungen und Aktionen?
4. **Bau:** Helfer, Vorlage, Automation, Dashboard.
5. **Abnahme:** funktioniert, übersteht einen Neustart, verhält sich bei `unavailable` richtig (G-21), Doku steht.

Ergebnis: ein Modul-Steckbrief ([`steckbrief-vorlage.md`](./steckbrief-vorlage.md)); `module.yaml` ist freiwillig.

## Voller Weg (ab Stufe 2)

1. Auftrag
2. HA-Bestand
3. Eigentumsregister
4. Modulvertrag und `module.yaml` ([`module-yaml.md`](./module-yaml.md))
5. Ausbaustufe und Aufbau
6. Mockup
7. Fachlogik mit Tests (ohne HA, G-12)
8. HA-Integration
9. Oberfläche und Automationen
10. Diagnose, Abnahme, Einspielen

Tore (Gates):

- **zwischen 4 und 5:** Kein Code, solange Eigentümer, Eingänge, Ergebnisse und Schreibwege nicht eindeutig sind.
- **zwischen 7 und 8:** Fachlogik-Tests grün.
- **vor 10:** Keine Fachlogik doppelt in Oberfläche, Automation und Integration (G-04).

## Einspielen

- Oberflächen-Code: ausliefern, im Browser neu laden.
- Optionsänderung: lädt den Eintrag neu (G-16).
- Python-Code einer Integration: wird erst mit einem HA-Neustart aktiv. Den Neustart löst nur Herbert aus. Deshalb
  Änderungen sammeln, vorher am Pi testen (`pytest`), dann ein Neustart je Lieferung; vor dem Neustart die Konfiguration
  prüfen.
