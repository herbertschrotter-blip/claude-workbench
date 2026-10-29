# Stack: Home Assistant

Für Projekte mit Stack `home-assistant` oder `home-assistant-yaml`. Neu gestartet wird nur Home Assistant Core; das
Claude-Add-on läuft dabei weiter, die Sitzungen bleiben offen.

## Prüfen

- Konfiguration prüfen, Ergebnis muss gültig sein:
  - Shell der App: `ha core check`
  - oder Home-Assistant-MCP: Dienst `homeassistant.check_config` (`home-assistant:ha_call_service`), danach das
    Ergebnis im Protokoll bzw. in den Benachrichtigungen lesen
- Reicht ein Reload (nur Automationen, Skripte, Szenen, Templates, Helfer einer schon geladenen Domäne), keinen
  Neustart machen: Reload in dem Skill, der die Änderung macht. Neustart braucht es für neue Integrationen,
  geänderte `custom_components/`, neue Helfer-Domänen und `configuration.yaml`-Abschnitte ohne Reload.

## Neu starten

- Home-Assistant-MCP: `home-assistant:ha_restart`, sonst Shell: `ha core restart`.
- Danach warten, bis Home Assistant wieder antwortet: alle 10 Sekunden einen leichten Abruf (z. B. Zustand einer
  Entität), höchstens 5 Minuten. Antwortet es dann nicht: Nutzer sofort informieren, nichts weiter versuchen.

## Kontrollieren

- Protokoll seit dem Neustart auf neue Fehler und Warnungen der betroffenen Integrationen lesen (`ha core logs` oder
  Protokoll über MCP).
- Die Entitäten, Dienste oder Karten, die das Einspielen betrifft, sind vorhanden und nicht `unavailable`.
- Reparaturen und Benachrichtigungen nach neuen Einträgen ansehen.

## Nie

- `ha host reboot`, `ha os …`, den Neustart der Supervisor- oder Add-on-Ebene (`ha supervisor restart`,
  `ha addons restart`)
