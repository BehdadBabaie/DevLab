import pytest

from devlab.config import Settings, validate_settings


def test_settings_defaults():
    settings = Settings()

    assert settings.compose_file_name == "compose.yaml"
    assert settings.default_shell == "bash"


def test_validate_settings_accepts_valid_settings():
    settings = Settings(
        compose_file_name="docker-compose.yaml",
        default_shell="sh",
    )

    validate_settings(settings)


def test_validate_settings_rejects_empty_shell():
    settings = Settings(
        default_shell="",
    )

    with pytest.raises(
        ValueError,
        match="'default_shell' must be a non-empty string.",
    ):
        validate_settings(settings)


def test_validate_settings_rejects_non_string_shell():
    settings = Settings(
        default_shell=123,
    )

    with pytest.raises(
        ValueError,
        match="'default_shell' must be a non-empty string.",
    ):
        validate_settings(settings)


def test_validate_settings_rejects_empty_compose_file_name():
    settings = Settings(
        compose_file_name="",
    )

    with pytest.raises(
        ValueError,
        match="'compose_file_name' must be a non-empty string.",
    ):
        validate_settings(settings)


def test_validate_settings_rejects_non_string_compose_file_name():
    settings = Settings(
        compose_file_name=123,
    )

    with pytest.raises(
        ValueError,
        match="'compose_file_name' must be a non-empty string.",
    ):
        validate_settings(settings)
