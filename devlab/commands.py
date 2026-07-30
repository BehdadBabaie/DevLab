import sys
import subprocess
from devlab.console import console
from devlab.compose import get_services

VERIFY_COMMANDS = {
    "python": [
        "python3 --version",
        "uv --version",
    ],
    "go": [
        "go version",
    ],
    "rust": [
        "rustc --version",
        "cargo --version",
    ],
    "node": [
        "node --version",
        "npm --version",
    ],
}


def docker_compose(*args: str) -> None:
    command = " ".join(args)
    console.print(f"[dim]$ docker compose {command}[/dim]")
    try:
        subprocess.run(
            [
                "docker",
                "compose",
                *args,
            ],
            check=True,
        )
    except FileNotFoundError:
        console.print(
            "[bold red]✗ Docker is not installed or is not available on your PATH.[/]"
        )
        console.print(
            "[bold red]Please install Docker Desktop and ensure 'docker' is available on your PATH.[/]"
        )
        sys.exit(1)
    except subprocess.CalledProcessError as error:
        console.print(
            "[bold red]✗ Command failed.[/]"
        )
        sys.exit(1)


def is_valid_environment(environment: str) -> bool:
    environments = get_services()
    if environment not in environments:
        console.print(f"[red]Unknown environment:[/] {environment}")
        console.print(f"Available:")
        for env in environments:
            console.print(f" • {env}")
        return False
    return True


def list_environments() -> None:
    console.rule("[bold cyan]DevLab Environments[/]")

    for environment in get_services():
        console.print(f"✅ [green]{environment}[/]")



def build_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    console.print(f"🔨 Building [bold]{environment}[/]...")
    docker_compose("build", environment)


def run_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    console.print(f"🚀 Launching [bold]{environment}[/]...")
    docker_compose(
        "run",
        "--rm",
        environment,
        "bash",
    )


def verify_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    commands = VERIFY_COMMANDS.get(environment)

    if commands is None:
        console.print(f"[yellow]No verification commands defined for '{environment}'.[/]")
        return

    script = " && ".join(commands)

    console.print(f"🔍 Verifying [bold]{environment}[/]...")
    docker_compose(
        "run",
        "--rm",
        environment,
        "bash",
        "-c",
        script,
    )