from dataclasses import dataclass


@dataclass(slots=True)
class Settings:
    compose_file: str = "compose.yaml"
    default_shell: str = "bash"

settings =Settings()
