from pathlib import Path

import yaml

PROJECT_ROOT = Path(__file__).resolve().parent.parent
COMPOSE_FILE = PROJECT_ROOT / "compose.yaml"


def get_services() -> list[str]:
    with COMPOSE_FILE.open("r", encoding="utf-8") as file:
        compose = yaml.safe_load(file)

    return sorted(compose["services"].keys())
