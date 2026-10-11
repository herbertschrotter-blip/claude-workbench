"""Auslieferung mit Rückweg – ohne Home Assistant, in einer nachgebauten Konfiguration."""

import shutil
import subprocess
import sys
from pathlib import Path

import pytest

SKRIPT = Path(__file__).resolve().parents[2] / "ausliefern.py"
DOMAIN = "{{package}}"


@pytest.fixture
def ha(tmp_path):
    """HA-Konfiguration mit dem Projekt unter projekte/, wie auf dem HA-Rechner."""
    (tmp_path / "configuration.yaml").write_text("homeassistant:\n", encoding="utf-8")
    projekt = tmp_path / "projekte" / "projekt"
    integration = projekt / "custom_components" / DOMAIN
    integration.mkdir(parents=True)
    (integration / "manifest.json").write_text('{"version": "2"}', encoding="utf-8")
    (integration / "__pycache__").mkdir()
    shutil.copy(SKRIPT, projekt / "ausliefern.py")
    return tmp_path


def lauf(ha, *args):
    return subprocess.run(
        [sys.executable, str(ha / "projekte" / "projekt" / "ausliefern.py"), *args],
        capture_output=True,
        text=True,
        timeout=60,
        check=False,
    )


def ausgeliefert(ha):
    return (ha / "custom_components" / DOMAIN / "manifest.json").read_text(encoding="utf-8")


def test_erste_auslieferung(ha):
    r = lauf(ha)
    assert r.returncode == 0, r.stderr
    assert ausgeliefert(ha) == '{"version": "2"}'
    assert not (ha / "custom_components" / DOMAIN / "__pycache__").exists()
    assert "neu starten" in r.stdout


def test_vorige_fassung_sichern_und_zurueck(ha):
    alt = ha / "custom_components" / DOMAIN
    alt.mkdir(parents=True)
    (alt / "manifest.json").write_text('{"version": "1"}', encoding="utf-8")
    assert lauf(ha).returncode == 0
    assert ausgeliefert(ha) == '{"version": "2"}'
    r = lauf(ha, "--zurueck")
    assert r.returncode == 0, r.stderr
    assert ausgeliefert(ha) == '{"version": "1"}'


def test_zurueck_nach_erster_auslieferung_entfernt(ha):
    assert lauf(ha).returncode == 0
    r = lauf(ha, "--zurueck")
    assert r.returncode == 0, r.stderr
    assert not (ha / "custom_components" / DOMAIN).exists()
    assert lauf(ha, "--zurueck").returncode == 1


def test_zurueck_ohne_sicherung(ha):
    r = lauf(ha, "--zurueck")
    assert r.returncode == 1
    assert "keine gesicherte Fassung" in r.stderr


def test_ziel_ohne_configuration_yaml(ha, tmp_path_factory):
    leer = tmp_path_factory.mktemp("kein_ha")
    r = lauf(ha, "--ziel", str(leer))
    assert r.returncode == 1
    assert not (leer / "custom_components").exists()
