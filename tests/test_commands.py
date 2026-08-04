
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
