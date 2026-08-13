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


class DockerCommandError(Exception):
    """Raised when a Docker Compose command cannot be executed."""


def validate_shell(shell: str) -> None:
    if not shell.strip():
        raise ValueError("Shell must be a non-empty string.")

def docker_compose(*args: str) -> None:
    command = " ".join(args)

    if state.verbose:
        console.print(f"[dim]$ docker compose {command}[/dim]")

    try:
        _run_docker_compose(*args)
    except DockerCommandError as error:
        console.print(f"[bold red]✗ {error}[/]")
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

    validate_shell(shell)

    console.print(f"🚀 Launching [bold]{environment}[/]...")
    docker_compose(
        "run",
        "--rm",
        environment,
        shell,
    )


def verify_environment(environment: str, shell: str | None = None) -> None:
    if not is_valid_environment(environment):
        return

    commands = VERIFY_COMMANDS.get(environment)

    if commands is None:
        console.print(
            f"[yellow]No verification commands defined for '{environment}'.[/]"
        )
        return

    if shell is None:
        shell = get_settings().default_shell

    validate_shell(shell)

    script = " && ".join(commands)

    console.print(f"🔍 Verifying [bold]{environment}[/]...")
    docker_compose(
        "run",
        "--rm",
        environment,
        shell,
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
    except FileNotFoundError:
        console.print("❌ Docker executable not found")
        return

    if _docker_is_available():
        console.print("✅ Docker daemon available")
    else:
        console.print(
            "❌ Docker daemon unavailable\n"
            "Start Docker Desktop and run this command again."
        )
        return

    if _docker_compose_is_available():
        console.print("✅ Docker compose available")
    else:
        console.print(
            "❌ Docker compose unavailable"
        )
        return

    compose_file = get_compose_file()
    if compose_file.exists():
        console.print(f"✅ {compose_file.name} found")
    else:
        console.print(f"❌ {compose_file.name} not found")

    try:
        services = get_services()
        console.print("✅ Compose configuration valid")
        console.print(f"✅ {len(services)} environments discovered")
        console.print()
        console.print("[bold]Environment images")

        for environment in services:
            if _environment_image_exists(environment):
                console.print(
                    f"✅ [green]{environment:<10}[/] image available"
                )
            else:
                console.print(
                    f"❌ [red]{environment:<10}[/] image not built"
                )
    except ValueError as error:
        console.print(f"❌ Invalid Compose configuration: {error}")


def show_config() -> None:
    console.rule("[bold cyan]DevLab Configuration[/]")
    console.print()

    settings = get_settings()

    console.print(f"Compose file : {settings.compose_file_name}")
    console.print(f"Default shell: {settings.default_shell}")


def status_environments() -> None:
    console.rule("[bold cyan]DevLab Environment Status[/]")
    console.print()

    for environment in get_services():

        try:
            available = _environment_image_exists(environment)
        except FileNotFoundError:
            console.print(
                "[bold red]✗ Docker is not installed or is not available "
                "on your PATH.[/]"
            )
            return

        if available:
            console.print(
                f"✅ [green]{environment:<10}[/] image available"
            )
        else:
            console.print(
                f"❌ [red]{environment:<10}[/] image not built"
            )


def _run_docker_compose(*args: str) -> None:

    try:
        subprocess.run(
            [
                "docker",
                "compose",
                *args,
            ],
            check=True,
        )
    except FileNotFoundError as error:
        raise DockerCommandError(
            "Docker is not installed or is not available on your PATH.\n"
            "Please install Docker Desktop and ensure 'docker' is available "
            "on your PATH."
        ) from error
    except subprocess.CalledProcessError as error:
        command = " ".join(error.cmd)
        raise DockerCommandError(
            f"Command failed: {command}"
        ) from error


def _docker_image_exists(image: str) -> bool:
    result = subprocess.run(
        ["docker", "image", "inspect", image],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def _docker_is_available() -> bool:
    result = subprocess.run(
        ["docker", "info"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def _docker_compose_is_available() -> bool:
    result = subprocess.run(
        ["docker", "compose", "version"],
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )

    return result.returncode == 0


def _environment_image_exists(environment: str) -> bool:
    return _docker_image_exists(f"devlab-{environment}")
