from pathlib import Path

import pytest

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


def test_get_services_raises_value_error_when_services_missing(
    tmp_path: Path,
):
    compose = tmp_path / "compose.yaml"

    compose.write_text(
        """
version: "3.9"
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="services"):
        get_services(compose)


def test_get_services_raises_value_error_for_invalid_yaml(
    tmp_path: Path,
):
    compose = tmp_path / "compose.yaml"

    compose.write_text(
        """
services:
  python:
    image: python
    - invalid
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="invalid YAML"):
        get_services(compose)


def test_get_services_raises_value_error_when_services_is_not_mapping(
    tmp_path: Path,
):
    compose = tmp_path / "compose.yaml"

    compose.write_text(
        """
services:
  - python
  - node
""",
        encoding="utf-8",
    )

    with pytest.raises(ValueError, match="services"):
        get_services(compose)
