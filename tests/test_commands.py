import subprocess

import pytest

from devlab import commands


def test_build_environment_calls_docker_compose(monkeypatch):
    called = {}

    def fake_docker_compose(*args: str) -> None:
        called["args"] = args

    monkeypatch.setattr(
        commands,
        "docker_compose",
        fake_docker_compose,
    )

    monkeypatch.setattr(
        commands,
        "is_valid_environment",
        lambda environment: True,
    )

    commands.build_environment("rust")

    assert called["args"] == (
        "build",
        "rust",
    )


def test_run_environment_calls_docker_compose(monkeypatch):
    called = {}

    def fake_docker_compose(*args: str) -> None:
        called["args"] = args

    monkeypatch.setattr(
        commands,
        "docker_compose",
        fake_docker_compose,
    )

    monkeypatch.setattr(
        commands,
        "is_valid_environment",
        lambda environment: True,
    )

    commands.run_environment(
        "rust",
        shell="sh",
    )

    assert called["args"] == (
        "run",
        "--rm",
        "rust",
        "sh",
    )


def test_validate_shell_rejects_empty_shell():
    with pytest.raises(
        commands.InvalidShellError,
        match="Shell must be a non-empty string",
    ):
        commands.validate_shell("   ")


def test_verify_environment_calls_docker_compose(monkeypatch):
    called = {}

    def fake_docker_compose(*args: str) -> None:
        called["args"] = args

    monkeypatch.setattr(
        commands,
        "docker_compose",
        fake_docker_compose,
    )

    monkeypatch.setattr(
        commands,
        "is_valid_environment",
        lambda environment: True,
    )

    commands.verify_environment(
        "node",
        shell="sh",
    )

    assert called["args"] == (
        "run",
        "--rm",
        "node",
        "sh",
        "-c",
        "node --version && npm --version",
    )


def test_build_environment_does_not_call_docker_for_invalid_environment(
    monkeypatch,
):
    called = False

    def fake_docker_compose(*args: str) -> None:
        nonlocal called
        called = True

    monkeypatch.setattr(
        commands,
        "docker_compose",
        fake_docker_compose,
    )

    monkeypatch.setattr(
        commands,
        "is_valid_environment",
        lambda environment: False,
    )

    commands.build_environment("kotlin")

    assert called is False


def test_docker_compose_runs_expected_command(monkeypatch):
    called = {}

    def fake_run(command, check):
        called["command"] = command
        called["check"] = check

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        fake_run,
    )

    commands.docker_compose("build", "rust")

    assert called == {
        "command": [
            "docker",
            "compose",
            "build",
            "rust",
        ],
        "check": True,
    }


def test_docker_compose_handles_missing_docker(monkeypatch, capsys):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        fake_run,
    )

    with pytest.raises(SystemExit) as error:
        commands.docker_compose("build", "rust")

    assert error.value.code == 1

    captured = capsys.readouterr()

    assert "Docker is not installed" in captured.out
    assert "Please install Docker Desktop" in captured.out


def test_docker_compose_handles_command_failure(monkeypatch, capsys):
    def fake_run(*args, **kwargs):
        raise subprocess.CalledProcessError(
            returncode=1,
            cmd=["docker", "compose", "build", "rust"],
        )

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        fake_run,
    )

    with pytest.raises(SystemExit) as error:
        commands.docker_compose("build", "rust")

    assert error.value.code == 1

    captured = capsys.readouterr()

    assert "✗ Command failed: docker compose build rust" in captured.out


def test_status_environments_reports_image_status(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python", "rust"],
    )

    monkeypatch.setattr(
        commands,
        "_environment_image_exists",
        lambda environment: True,
    )

    commands.status_environments()

    output = capsys.readouterr().out

    assert "python" in output
    assert "rust" in output
    assert "image available" in output


def test_status_environments_reports_missing_image(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python"],
    )

    monkeypatch.setattr(
        commands,
        "_environment_image_exists",
        lambda environment: False,
    )

    commands.status_environments()

    output = capsys.readouterr().out

    assert "python" in output
    assert "image not built" in output


def test_docker_is_available_returns_true(monkeypatch):
    class Result:
        returncode = 0

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: Result(),
    )

    assert commands._docker_is_available() is True


def test_docker_is_available_returns_false(monkeypatch):
    class Result:
        returncode = 1

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: Result(),
    )

    assert commands._docker_is_available() is False


def test_docker_compose_is_available_returns_true(monkeypatch):
    class Result:
        returncode = 0

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: Result(),
    )

    assert commands._docker_compose_is_available() is True


def test_docker_compose_is_available_returns_false(monkeypatch):
    class Result:
        returncode = 1

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: Result(),
    )

    assert commands._docker_compose_is_available() is False

def test_doctor_reports_valid_compose_configuration(
    monkeypatch,
    capsys,
    tmp_path,
):
    compose_file = tmp_path / "compose.yaml"
    compose_file.touch()

    monkeypatch.setattr(
        commands,
        "get_compose_file",
        lambda: compose_file,
    )

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0},
        )(),
    )

    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python", "go", "rust"],
    )

    monkeypatch.setattr(
        commands,
        "_environment_image_exists",
        lambda environment: True,
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "Compose configuration valid" in output
    assert "3 environments discovered" in output


def test_doctor_reports_invalid_compose_configuration(
    monkeypatch,
    capsys,
    tmp_path,
):
    compose_file = tmp_path / "compose.yaml"
    compose_file.touch()

    monkeypatch.setattr(
        commands,
        "get_compose_file",
        lambda: compose_file,
    )

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0},
        )(),
    )

    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: (_ for _ in ()).throw(
            ValueError("Compose file contains invalid YAML.")
        ),
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "Invalid Compose configuration" in output
    assert "invalid YAML" in output


def test_doctor_stops_when_docker_is_not_installed(
    monkeypatch,
    capsys,
):
    def fake_run(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        fake_run,
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "Docker executable not found" in output
    assert "Docker daemon available" not in output


def test_doctor_stops_when_docker_daemon_is_unavailable(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0},
        )(),
    )

    monkeypatch.setattr(
        commands,
        "_docker_is_available",
        lambda: False,
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "Docker executable found" in output
    assert "Docker daemon unavailable" in output
    assert "Docker compose available" not in output


def test_doctor_stops_when_docker_compose_is_unavailable(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0},
        )(),
    )

    monkeypatch.setattr(
        commands,
        "_docker_is_available",
        lambda: True,
    )

    monkeypatch.setattr(
        commands,
        "_docker_compose_is_available",
        lambda: False,
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "Docker executable found" in output
    assert "Docker daemon available" in output
    assert "Docker compose unavailable" in output
    assert "compose.yaml found" not in output


def test_doctor_reports_missing_compose_file(
    monkeypatch,
    capsys,
    tmp_path,
):
    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0},
        )(),
    )

    monkeypatch.setattr(
        commands,
        "_docker_is_available",
        lambda: True,
    )

    monkeypatch.setattr(
        commands,
        "_docker_compose_is_available",
        lambda: True,
    )

    monkeypatch.setattr(
        commands,
        "get_compose_file",
        lambda: tmp_path / "compose.yaml",
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "compose.yaml not found" in output


def test_doctor_reports_missing_environment_image(
    monkeypatch,
    capsys,
):
    monkeypatch.setattr(
        commands.subprocess,
        "run",
        lambda *args, **kwargs: type(
            "Result",
            (),
            {"returncode": 0},
        )(),
    )

    monkeypatch.setattr(
        commands,
        "_docker_is_available",
        lambda: True,
    )

    monkeypatch.setattr(
        commands,
        "_docker_compose_is_available",
        lambda: True,
    )

    monkeypatch.setattr(
        commands,
        "get_compose_file",
        lambda: type(
            "ComposeFile",
            (),
            {
                "exists": lambda self: True,
                "name": "compose.yaml",
            },
        )(),
    )

    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python"],
    )

    monkeypatch.setattr(
        commands,
        "_environment_image_exists",
        lambda environment: False,
    )

    commands.doctor()

    output = capsys.readouterr().out

    assert "python" in output
    assert "image not built" in output


def test_status_environments_handles_missing_docker(
    monkeypatch,
    capsys,
):
    def raise_missing_docker(*args, **kwargs):
        raise FileNotFoundError

    monkeypatch.setattr(
        commands,
        "_environment_image_exists",
        raise_missing_docker,
    )

    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python", "rust"],
    )

    commands.status_environments()

    output = capsys.readouterr().out

    assert "Docker is not installed" in output


