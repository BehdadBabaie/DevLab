from dataclasses import dataclass
from pathlib import Path

import yaml


@dataclass(slots=True)
class Settings:
    compose_file_name: str = "compose.yaml"
    default_shell: str = "bash"


PROJECT_ROOT = Path(__file__).resolve().parent.parent
CONFIG_FILE = PROJECT_ROOT / "devlab.yaml"


def validate_settings(settings: Settings) -> None:
    if not isinstance(settings.default_shell, str) or not settings.default_shell:
        raise ValueError("'default_shell' must be a non-empty string.")

    if (
        not isinstance(settings.compose_file_name, str)
        or not settings.compose_file_name
    ):
        raise ValueError("'compose_file_name' must be a non-empty string.")


def load_settings() -> Settings:
    settings = Settings()

    if not CONFIG_FILE.exists():
        return settings

    with CONFIG_FILE.open(encoding="utf-8") as file:
        config = yaml.safe_load(file) or {}
        settings.compose_file_name = config.get(
            "compose_file_name",
            settings.compose_file_name,
        )
        settings.default_shell = config.get(
            "default_shell",
            settings.default_shell,
        )

    validate_settings(settings)
    return settings


_settings: Settings | None = None


def get_settings() -> Settings:
    global _settings
    if _settings is None:
        _settings = load_settings()
    return _settings
