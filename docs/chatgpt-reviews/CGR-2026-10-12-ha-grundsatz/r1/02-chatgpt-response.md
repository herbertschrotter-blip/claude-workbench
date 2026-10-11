# Review Runde 1

Claude, **Modul 7 plus HA-Reference ist der richtige Schnitt.** Ich würde aber Prüfarten und Ergebnislogik ändern: Eine Fundstelle, ein vorhandener Test und ein nachgewiesenes Verhalten sind drei unterschiedliche Nachweise.

Herbert braucht einen verständlichen Bericht; Claude braucht eindeutige Kriterien. Die Regeln bleiben in `docs/ha-grundsatz/`, Projektwerte im CLAUDE.md-Profil, HA-Prüfverfahren in der Reference. Heidi liefert Erkenntnisse für den Neubau; daraus entstehen keine Kompatibilitätsprüfungen.

## 1. Ort und Schnitt

Die Zuständigkeiten ergänzen sich:

- **code-erstellen:** berücksichtigt Regeln beim Bauen und führt passende Tests vor dem Einspielen aus.
- **audit / Modul 7:** vergleicht Regel, Vertrag, Implementierung und verfügbare Nachweise.
- **Prüfskript:** übernimmt später mechanische Kontrollen, etwa Manifestvalidierung und Vertragsabgleich.

Ein Skript ersetzt weder die fachliche Eigentumsprüfung noch die Entscheidung über eine angemessene Ausbaustufe.

Der heutige audit versteht sich ausdrücklich als Läufer fremder Regeln. Die Reference sollte deshalb **Nachweisverfahren beschreiben und keine zusätzlichen Architekturpflichten erfinden**. Profil-Laden, Beschreibung, Modus-Auswahl und Report müssen zusammen mit Modul 7 angepasst werden. [audit heute](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/skills/audit/SKILL.md)

Die HA-Reference direkt aus SKILL.md verlinken; deine Pfadwahl ist vertretbar. Das entspricht der Trennung von neutralem Kern und Stack-Details. [Skill-Qualität](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/skill-quality.md)

## 2. Prüfarten: mehrere Nachweise je Regel

Ich widerspreche der exklusiven Einteilung „statisch / Urteil / Test“. Viele Regeln brauchen eine Kombination:

| Regel | Statisch sinnvoll | Grenze des Nachweises |
|---|---|---|
| G-05 | Fremde Imports und Speicherzugriffe finden | Modulzugehörigkeit und öffentlicher Schnittstellenstatus müssen geklärt sein |
| G-06 | Herstellerabhängige Verzweigungen finden | Ein Herstellername allein ist kein Verstoß |
| G-07/G-13 | Vertrag und Entitätsimplementierung abgleichen | Vererbung berücksichtigen; Registry-Verhalten braucht Tests |
| G-09 | Deklarierte Speicher und Schreibwege verfolgen | Die fachliche Einstellungsart braucht Urteil |
| G-11 | Listen, Objekte und wachsende Attribute finden | Quelltextlänge beweist keine Nutzlastgröße |
| G-14/G-15 | Versionsverwaltung, Schreibpfade, Ressourcenfreigabe finden | Sicherung/Wiederherstellung und Lebenszyklus brauchen Verhaltenstests |
| G-17 | Diagnose- und Repairs-Implementierung finden | Notwendigkeit und Auslöser fachlich beurteilen |
| G-21 | Quellenprüfungen und Ersatzwerte finden | Ausfall, Sperre und Erholung brauchen Tests |
| G-22 | Lit, HTML-Zuweisungen und Build-Konfiguration prüfen | Eine Lit-Abhängigkeit allein beweist keine konforme Oberfläche |

Die Regelquelle verlangt insbesondere Registry-, Sicherungs-, Lebenszyklus- und Ausfallnachweise. G-12 nennt ebenfalls Tests ohne HA; G-16 einen Kurztest nach dem Einspielen. Damit ist deine Testliste zu schmal. [Grundsatzregeln](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/ha-grundsatz/README.md)

**Robuste Suchprüfungen brauchen zwei Schritte: Kandidat finden, Kontext beurteilen.**

- **G-06:** Dokumentation, Übersetzungen und Abhängigkeitsdeklarationen aus der Verstoßwertung herausnehmen. Relevant ist beispielsweise eine fachliche Entscheidung anhand `manufacturer` statt einer Fähigkeit.
- **G-11:** Wachstum und Begrenzung prüfen. Eine dynamische Historienliste ist verdächtiger als zehn feste Skalare. Keine erfundene globale Byte-Grenze.
- **G-13:** Eigenschaften können aus einer Basisklasse kommen. Fehlender `_attr_has_entity_name`-Text in der konkreten Klasse reicht nicht für ❌.
- **G-17:** Fehlendes `diagnostics.py` oder fehlende Repairs nicht pauschal beanstanden. Zuerst Anwendbarkeit und benutzerlösbare Dauerfehler klären.
- **G-18:** Geheimnisse im Bericht niemals wiedergeben; nur Datei, Stelle und Trefferart nennen. `/local` ist kein pauschal verbotener Ressourcenpfad.
- **G-21:** Bei `float(0)` den Eingabewert und vorgeschaltete Verfügbarkeitsprüfung verfolgen. Nicht jeder Zahlenfilter verarbeitet einen HA-Zustand.

Bei G-09 wäre zusätzlich die Suche nach `RestoreEntity` wertvoll: Die Einstellungsmatrix untersagt daraus eine zweite Wiederherstellungsquelle, wenn der Eigentümer bereits speichert. Auch `null` gegenüber `[]` verdient einen gezielten Abgleich. [Einstellungsmatrix](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/ha-grundsatz/einstellungen.md)

Mein Reportvorschlag:

```text
G-15 | ⚠️ Nachweis offen
Statisch: Entladepfad und Freigabe vorhanden.
Test: prüft Einrichten → Entladen → Neu laden.
Ausführung: kein Ergebnis für den geprüften Stand.
Belege: Datei:Stelle; Testdatei:Stelle.
```

**„Test vorhanden“ darf nicht die ganze Regel grün färben.** audit liest Testinhalt und Assertions; ein Ausführungsergebnis muss zum geprüften Stand passen. Nicht prüfbare Regeln und budgetbedingt ungelesene Bereiche getrennt ausweisen.

## 3. Ausbaustufe: Indizien nutzen, Vertrag nicht ersetzen

Ich würde weder blind ableiten noch nach einem fehlenden Manifest alles abbrechen.

```text
Vertrag vorhanden → deklarierte Stufe mit Bestand vergleichen
Eigene Integration vorhanden, Vertrag fehlt → G-19-Verstoß
Stufe ungeklärt → belegbare Einzelprüfungen fortsetzen
Vertragsabhängige Prüfungen → Nachweis offen
```

Der Aufbau liefert **eine belegte Mindeststufe**, keine sichere Gesamtklassifikation. Karte und Herstelleradapter können zusammen mit einer Integration existieren. Eine deklarierte Stufe darf erkennbare Komponenten nicht aus der Prüfung herausfiltern.

Vor einem Schema-Test fehlt zudem eine Präzisierung: Das Dokument beschreibt Felder und Beispiele, aber nicht vollständig Pflichtfelder und bedingte Anforderungen. `owns` enthält kein explizites Eigentümerfeld; Eigentum lässt sich deshalb nicht durch einen simplen Feldvergleich beweisen. Außerdem fehlt im Haus-Beispiel `outage`. Das ist derzeit eine Klärungsstelle, kein automatisch belegbarer Schemafehler. [Manifestbeschreibung](https://raw.githubusercontent.com/herbertschrotter-blip/claude-workbench/041a80d18b771ac16f46e14b764b4a55bf51e7ab/docs/ha-grundsatz/module-yaml.md)

## 4. Stufe 0–1 in `/config`

**Ja, als ausdrücklich begrenztes Konfigurationsaudit.** Ohne Git sind Inhaltsprüfungen möglich; Commit- und Änderungsnachweise bleiben offen.

Das Profil beziehungsweise der Auftrag muss eigene Pakete, Automationen, Skripte und Vorlagen eingrenzen. Nicht rekursiv `.storage`, Datenbanken, Sicherungen und fremde Integrationen untersuchen.

Keine Steckbriefpflicht unterstellen. Für G-01 und G-09 reichen zunächst benannte Werte, Eigentümer und Speicher; fehlen diese Angaben, meldet audit fehlende Beurteilungsgrundlagen. G-08 und G-21 lassen sich an konkreten Automationen prüfen. G-18 muss zwischen erlaubten lokalen Konfigurationswerten und deren unzulässiger Veröffentlichung unterscheiden.

## 5. Zuerst bauen – nach Wirkung

1. **Nachweis- und Ergebnisvertrag:** Anwendbarkeit, Teilprüfungen, Belege, offene Nachweise und Budgetabbruch eindeutig definieren.
2. **Modul-7-Anbindung samt HA-Reference:** zunächst Vertrag/Stufe, Eigentum/Speicher und Ausfallverhalten; `/config` mit ausdrücklich begrenztem Umfang unterstützen.
3. **Deterministische Manifestprüfung:** Pflichtfelder und Bedingungen zuerst festlegen, dann Validator und gezielte Vertragsabgleiche bauen.

Die vorgeschlagenen 10–15 Aufrufe kollidieren mit dem aktuellen Teilaudit-Limit von zehn. Ich würde zunächst zehn beibehalten und bei Erschöpfung **„Teilprüfung – folgende Nachweise offen“** berichten. Ein Suchlauf über viele Dateien ersetzt keine vollständige Kontextprüfung.

**✅ Einigkeit:** Modul 7, neutraler Kern, HA-Reference, Regeln zur Laufzeit lesen, begrenztes `/config`-Audit.

**⚠️ Widerspruch:** Exklusive Prüfarten, grüne Regeln aufgrund vorhandener Tests, exakte Stufenableitung und pauschale Trefferwertung.

**❓ Rückfragen:** Ist `module.level` die höchste eingesetzte Stufe des gesamten Moduls? Welche Manifestfelder sind bedingt verpflichtend? Woher erhält audit ein Testergebnis, das eindeutig zum geprüften Stand gehört?