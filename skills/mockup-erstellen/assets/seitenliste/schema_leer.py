"""Gibt das leere Schema als JSON aus. Vorlage für SQLite: leere_datenbank an das Projekt anpassen; andere Speicher brauchen
ein eigenes Skript mit derselben Ausgabe. Baut immer eine frische Datenbank, die echte wird nie gelesen."""

from __future__ import annotations

import json
import sqlite3
import tempfile
from pathlib import Path


def leere_datenbank(pfad: Path) -> str:
    """Legt das Schema in pfad an und gibt die Schema-Version zurück. Anpassen: Aufruf der Datenbank-Schicht des Projekts."""
    raise NotImplementedError


def main() -> None:
    with tempfile.TemporaryDirectory() as ordner:
        pfad = Path(ordner) / "leer.db"
        version = leere_datenbank(pfad)
        c = sqlite3.connect(pfad)
        tabellen = {}
        for (n,) in c.execute("select name from sqlite_master where type='table' and name not like 'sqlite_%'").fetchall():
            felder = [[r[1], r[2] or "", bool(r[5])] for r in c.execute(f'pragma table_info("{n}")')]
            fk = sorted({r[2] for r in c.execute(f'pragma foreign_key_list("{n}")')})
            tabellen[n] = {"felder": felder, "fk": fk}
        c.close()
    print(json.dumps({"version": version, "tabellen": tabellen}, ensure_ascii=False))


if __name__ == "__main__":
    main()
