import subprocess
import sys
from importlib.metadata import version

from devlab.compose import get_compose_file, get_services
from devlab.config import get_settings
from devlab.console import console
from devlab.state import state

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

    if state.verbose:
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
            "[bold red]Please install Docker Desktop and ensure 'docker' is available "
            "on your PATH.[/]"
        )
        sys.exit(1)
    except subprocess.CalledProcessError:
        console.print("[bold red]✗ Command failed.[/]")
        sys.exit(1)


def is_valid_environment(environment: str) -> bool:
    environments = get_services()
    if environment not in environments:
        console.print(f"[red]Unknown environment:[/] {environment}")
        console.print("Available:")
        for env in environments:
            console.print(f" • {env}")
        return False
    return True


def list_environments() -> None:
    console.rule("[bold cyan]DevLab Environments[/]")

    for environment in get_services():
        console.print(f"✅ [green]{environment}[/]")


def build_environment(
    environment: str,
    no_cache: bool = False,
) -> None:
    if not is_valid_environment(environment):
        return

    console.print(f"🔨 Building [bold]{environment}[/]...")
    if no_cache:
        docker_compose("build", "--no-cache", environment)
    else:
        docker_compose("build", environment)


def run_environment(
    environment: str,
    shell: str | None = None,
) -> None:

    if not is_valid_environment(environment):
        return

    if shell is None:
        shell = get_settings().default_shell

    if not shell.strip():
        raise ValueError("Shell must be a non-empty string.")

    console.print(f"🚀 Launching [bold]{environment}[/]...")
    docker_compose(
        "run",
        "--rm",
        environment,
        shell,
    )


def verify_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    commands = VERIFY_COMMANDS.get(environment)

    if commands is None:
        console.print(
            f"[yellow]No verification commands defined for '{environment}'.[/]"
        )
        return

    script = " && ".join(commands)

    console.print(f"🔍 Verifying [bold]{environment}[/]...")
    docker_compose(
        "run",
        "--rm",
        environment,
        get_settings().default_shell,
        "-c",
        script,
    )


def show_version() -> None:
    console.print(f"DevLab {version('devlab')}")


def doctor() -> None:
    console.rule("[bold cyan]DevLab Doctor[/]")

    try:
        subprocess.run(
            ["docker", "--version"],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
        console.print("✅ Docker executable found")
    except (FileNotFoundError, subprocess.CalledProcessError):
        console.print("❌ Docker executable not found")

    compose_file = get_compose_file()
    if compose_file.exists():
        console.print(f"✅ {compose_file.name} found")
    else:
        console.print(f"❌ {compose_file.name} not found")

    try:
        services = get_services()
        console.print(f"✅ {len(services)} environments discovered")
    except Exception:
        console.print("❌ Unable to discover environments")


def show_config() -> None:
    console.rule("[bold cyan]DevLab Configuration[/]")
    console.print()

    settings = get_settings()

    console.print(f"Compose file : {settings.compose_file_name}")
    console.print(f"Default shell: {settings.default_shell}")
