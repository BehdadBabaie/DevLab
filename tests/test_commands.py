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

    assert "✗ Command failed." in captured.out


def test_status_environments_reports_image_status(monkeypatch, capsys):
    def fake_run(*args, **kwargs):
        class Result:
            returncode = 0

        return Result()

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        fake_run,
    )

    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python", "rust"],
    )

    commands.status_environments()

    output = capsys.readouterr().out

    assert "python" in output
    assert "rust" in output
    assert "image available" in output


def test_status_environments_reports_missing_image(monkeypatch, capsys):
    def fake_run(*args, **kwargs):
        class Result:
            returncode = 1

        return Result()

    monkeypatch.setattr(
        commands.subprocess,
        "run",
        fake_run,
    )

    monkeypatch.setattr(
        commands,
        "get_services",
        lambda: ["python"],
    )

    commands.status_environments()

    output = capsys.readouterr().out

    assert "python" in output
    assert "image not built" in output
