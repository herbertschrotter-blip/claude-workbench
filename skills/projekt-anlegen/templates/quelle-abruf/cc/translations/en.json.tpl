{
  "config": {
    "step": {
      "user": {
        "title": "Connect device",
        "description": "Address of the device or service.",
        "data": {
          "adresse": "Address"
        }
      }
    },
    "error": {
      "cannot_connect": "Failed to connect."
    },
    "abort": {
      "already_configured": "This device is already configured."
    }
  },
  "entity": {
    "sensor": {
      "status": {
        "name": "Status",
        "state": {
          "bereit": "Ready",
          "quelle_fehlt": "Source missing"
        }
      }
    }
  },
  "exceptions": {
    "ticket_fehlt": {
      "message": "Ticket {ticket} does not exist."
    },
    "ticket_ungueltig": {
      "message": "Ticket not changed: {grund}"
    }
  },
  "services": {
    "ticket": {
      "name": "Change ticket",
      "description": "Change status, note, version and commit of a ticket (used by tools/ticket.py).",
      "fields": {
        "ticket": {
          "name": "Ticket",
          "description": "Number, e.g. FE-0001"
        },
        "status": {
          "name": "Status",
          "description": "neu, angenommen, in_arbeit, geloest, geschlossen, verworfen"
        },
        "notiz": {
          "name": "Note",
          "description": "What was done or why"
        },
        "version": {
          "name": "Version",
          "description": "Version with the fix"
        },
        "commit": {
          "name": "Commit",
          "description": "Commit with the fix"
        },
        "von": {
          "name": "By",
          "description": "Who changes it (default: Claude)"
        }
      }
    }
  }
}
