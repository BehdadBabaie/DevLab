import sys

import pytest

from devlab import cli


def test_build_no_cache(monkeypatch):
    called = {}

    def fake_build(environment: str, no_cache: bool = False) -> None:
        called["environment"] = environment
        called["no_cache"] = no_cache

    monkeypatch.setattr(cli, "build_environment", fake_build)

    monkeypatch.setattr(
        sys,
        "argv",
        ["devlab", "build", "--no-cache", "rust"],
    )

    cli._main()

    assert called == {
        "environment": "rust",
        "no_cache": True,
    }


def test_run_shell(monkeypatch):
    called = {}

    def fake_run(environment: str, shell: str | None = None) -> None:
        called["environment"] = environment
        called["shell"] = shell


    monkeypatch.setattr(cli, "run_environment", fake_run)

    monkeypatch.setattr(
        sys,
        "argv",
        ["devlab", "run", "--shell", "sh", "rust"]
    )

    cli._main()

    assert called == {
        "environment": "rust",
        "shell": "sh",
    }


def test_run_without_shell(monkeypatch):
    called = {}

    def fake_run(environment: str, shell: str | None = None) -> None:
        called["environment"] = environment
        called["shell"] = shell

    monkeypatch.setattr(cli, "run_environment", fake_run)

    monkeypatch.setattr(
        sys,
        "argv",
        ["devlab", "run", "rust"],
    )

    cli.main()

    assert called == {
        "environment": "rust",
        "shell": None,
    }

def test_verify_shell(monkeypatch):
    called = {}

    def fake_verify(
        environment: str,
        shell: str | None = None,
    ) -> None:
        called["environment"] = environment
        called["shell"] = shell

    monkeypatch.setattr(cli, "verify_environment", fake_verify)

    monkeypatch.setattr(
        sys,
        "argv",
        ["devlab", "verify", "--shell", "sh", "node"],
    )

    cli.main()

    assert called == {
        "environment": "node",
        "shell": "sh",
    }


def test_invalid_shell_reports_error(monkeypatch, capsys):
    def fake_run(
        environment: str,
        shell: str | None = None,
    ) -> None:
        raise cli.InvalidShellError(
            "Shell must be a non-empty string."
        )

    monkeypatch.setattr(cli, "run_environment", fake_run)

    monkeypatch.setattr(
        sys,
        "argv",
        ["devlab", "run", "--shell", "   ", "rust"],
    )

    with pytest.raises(SystemExit) as error:
        cli.main()

    assert error.value.code == 1

    output = capsys.readouterr().out

    assert "Invalid shell" in output
    assert "Shell must be a non-empty string." in output
