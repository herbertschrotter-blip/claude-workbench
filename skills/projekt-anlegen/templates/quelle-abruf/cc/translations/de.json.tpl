{
  "config": {
    "step": {
      "user": {
        "title": "Gerät verbinden",
        "description": "Adresse des Geräts oder Dienstes.",
        "data": {
          "adresse": "Adresse"
        }
      }
    },
    "error": {
      "cannot_connect": "Keine Verbindung möglich."
    },
    "abort": {
      "already_configured": "Dieses Gerät ist schon eingerichtet."
    }
  },
  "entity": {
    "sensor": {
      "status": {
        "name": "Status",
        "state": {
          "bereit": "Bereit",
          "quelle_fehlt": "Quelle fehlt"
        }
      }
    }
  },
  "exceptions": {
    "ticket_fehlt": {
      "message": "Ticket {ticket} gibt es nicht."
    },
    "ticket_ungueltig": {
      "message": "Ticket nicht geändert: {grund}"
    }
  },
  "services": {
    "ticket": {
      "name": "Ticket ändern",
      "description": "Status, Notiz, Version und Commit eines Tickets ändern (für tools/ticket.py).",
      "fields": {
        "ticket": {
          "name": "Ticket",
          "description": "Nummer, z. B. FE-0001"
        },
        "status": {
          "name": "Status",
          "description": "neu, angenommen, in_arbeit, geloest, geschlossen, verworfen"
        },
        "notiz": {
          "name": "Notiz",
          "description": "Was gemacht wurde oder warum"
        },
        "version": {
          "name": "Version",
          "description": "Version mit der Lösung"
        },
        "commit": {
          "name": "Commit",
          "description": "Commit mit der Lösung"
        },
        "von": {
          "name": "Von",
          "description": "Wer ändert (Standard: Claude)"
        }
      }
    }
  }
}
