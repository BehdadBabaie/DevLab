from pathlib import Path

import yaml

from devlab.config import get_settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_compose_file() -> Path:
    settings = get_settings()
    return PROJECT_ROOT / settings.compose_file_name


def get_services(compose_file: Path | None = None) -> list[str]:
    compose_file = compose_file or get_compose_file()

    try:
        with compose_file.open("r", encoding="utf-8") as file:
            compose = yaml.safe_load(file) or {}
    except yaml.YAMLError as error:
        raise ValueError(
            "Compose file contains invalid YAML."
        ) from error

    if "services" not in compose:
        raise ValueError(
            "Compose file is missing the 'services' section."
        )

    if not isinstance(compose["services"], dict):
        raise ValueError(
            "Compose file 'services' section must be a mapping."
        )

    return sorted(compose["services"].keys())


