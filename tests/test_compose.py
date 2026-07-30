from pathlib import Path

from devlab.compose import get_services


def test_get_services_returns_sorted_services(tmp_path: Path):
    compose = tmp_path / "compose.yaml"

    compose.write_text(
        """
services:
  rust:
    image: rust
  python:
    image: python
  node:
    image: node
""",
        encoding="utf-8",
    )

    services = get_services(compose)

    assert services == ["node", "python", "rust"]

def test_get_services_returns_empty_list_when_no_services(tmp_path: Path):
    compose = tmp_path / "compose.yaml"

    compose.write_text(
        """
services: {}
""",
        encoding="utf-8",
    )

    assert get_services(compose) == []


def test_get_services_are_sorted(tmp_path: Path):
    compose = tmp_path / "compose.yaml"

    compose.write_text(
        """
services:
  zulu:
    image: alpine
  alpha:
    image: alpine
  beta:
    image: alpine
""",
        encoding="utf-8",
    )

    assert get_services(compose) == [
        "alpha",
        "beta",
        "zulu",
    ]
