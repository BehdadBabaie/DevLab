from pathlib import Path

import yaml

from devlab.config import get_settings

PROJECT_ROOT = Path(__file__).resolve().parent.parent


def get_compose_file() -> Path:
    settings = get_settings()
    return PROJECT_ROOT / settings.compose_file_name


def get_services(compose_file: Path | None = None) -> list[str]:
    compose_file = compose_file or get_compose_file()

    with compose_file.open("r", encoding="utf-8") as file:
        compose = yaml.safe_load(file)

    return sorted(compose["services"].keys())
