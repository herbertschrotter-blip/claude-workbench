{
  "config": {
    "step": {
      "user": {
        "title": "Quelle wählen",
        "description": "Die Integration nutzt die Entität einer vorhandenen Integration.",
        "data": {
          "quelle": "Quelle"
        }
      }
    },
    "error": {
      "quelle_unbekannt": "Diese Entität gibt es nicht."
    },
    "abort": {
      "already_configured": "Diese Quelle ist schon eingerichtet."
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
