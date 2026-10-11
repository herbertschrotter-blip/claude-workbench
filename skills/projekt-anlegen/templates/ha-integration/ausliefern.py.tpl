"""Integration in die Home-Assistant-Konfiguration ausliefern – mit Rückweg.

    python ausliefern.py [--ziel <HA-Konfiguration>]            ausliefern
    python ausliefern.py [--ziel <HA-Konfiguration>] --zurueck  vorige Fassung wiederherstellen

Kopiert den Ordner der Integration aus custom_components/ in die HA-Konfiguration. Die dort
liegende Fassung wird vorher im Projekt unter .auslieferung/vorher/ gesichert (nicht im Repo);
--zurueck stellt sie wieder her, gab es keine, entfernt es die Integration wieder. Ohne --ziel
gilt der Ordner zwei Ebenen über dem Projekt, wenn dort eine configuration.yaml liegt. Danach:
Konfiguration prüfen und Home Assistant neu starten – das macht der Nutzer.
"""

import argparse
import shutil
import sys
from pathlib import Path

DOMAIN = "{{package}}"
PROJEKT = Path(__file__).resolve().parent
QUELLE = PROJEKT / "custom_components" / DOMAIN
VORHER = PROJEKT / ".auslieferung" / "vorher" / DOMAIN
KEINE = VORHER.with_name(f"{DOMAIN}.keine")  # Merker: vor der Auslieferung gab es keine Fassung
OHNE = shutil.ignore_patterns("__pycache__", "*.pyc")


class AuslieferFehler(RuntimeError):
    """Ziel oder Sicherung passt nicht; es wurde nichts geändert."""


def ha_konfiguration(ziel: str | None) -> Path:
    """HA-Konfiguration: --ziel oder zwei Ebenen über dem Projekt, mit configuration.yaml."""
    ordner = Path(ziel).resolve() if ziel else PROJEKT.parents[1]
    if not (ordner / "configuration.yaml").is_file():
        hinweis = "" if ziel else " – mit --ziel den Ordner der HA-Konfiguration angeben"
        raise AuslieferFehler(f"{ordner}: keine configuration.yaml{hinweis}")
    return ordner


def _ersetzen(quelle: Path, ziel: Path) -> None:
    """ziel durch eine Kopie von quelle ersetzen; erst kopieren, dann tauschen."""
    neu = ziel.with_name(f".{ziel.name}.neu")
    shutil.rmtree(neu, ignore_errors=True)
    shutil.copytree(quelle, neu, ignore=OHNE)
    if ziel.exists():
        shutil.rmtree(ziel)
    neu.rename(ziel)


def ausliefern(konfiguration: Path) -> str:
    ziel = konfiguration / "custom_components" / DOMAIN
    if not (QUELLE / "manifest.json").is_file():
        raise AuslieferFehler(f"{QUELLE}: keine manifest.json")
    ziel.parent.mkdir(exist_ok=True)
    if ziel.exists():
        _ersetzen(ziel, VORHER)
        KEINE.unlink(missing_ok=True)
        gesichert = f"; vorige Fassung gesichert in {VORHER.relative_to(PROJEKT)}"
    else:
        shutil.rmtree(VORHER, ignore_errors=True)
        KEINE.parent.mkdir(parents=True, exist_ok=True)
        KEINE.touch()
        gesichert = "; es gab keine vorige Fassung"
    _ersetzen(QUELLE, ziel)
    return f"ausgeliefert nach {ziel}{gesichert}"


def zurueck(konfiguration: Path) -> str:
    ziel = konfiguration / "custom_components" / DOMAIN
    if KEINE.is_file():
        shutil.rmtree(ziel, ignore_errors=True)
        KEINE.unlink()
        return f"{ziel} entfernt – vor der Auslieferung gab es keine Fassung"
    if not (VORHER / "manifest.json").is_file():
        raise AuslieferFehler(f"{VORHER}: keine gesicherte Fassung – nichts zurückzunehmen")
    _ersetzen(VORHER, ziel)
    shutil.rmtree(VORHER)
    return f"vorige Fassung wiederhergestellt in {ziel}"


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=f"{DOMAIN} in die HA-Konfiguration ausliefern")
    parser.add_argument("--ziel", help="Ordner der HA-Konfiguration (mit configuration.yaml)")
    parser.add_argument("--zurueck", action="store_true", help="vorige Fassung wiederherstellen")
    args = parser.parse_args(argv)
    try:
        konfiguration = ha_konfiguration(args.ziel)
        meldung = zurueck(konfiguration) if args.zurueck else ausliefern(konfiguration)
    except (AuslieferFehler, OSError) as exc:
        print(f"Fehler: {exc}", file=sys.stderr)
        return 1
    print(meldung)
    print("Jetzt: Konfiguration prüfen und Home Assistant neu starten (macht der Nutzer).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
