import subprocess

SUPPORTED_ENVIRONMENTS = [
    "base",
    "python",
    "go",
    "rust",
    "node",
    "C",
    "C++",
]

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

def is_valid_environment(environment: str) -> bool:
    if environment not in SUPPORTED_ENVIRONMENTS:
        print(f"Unknown environment: {environment}")
        print(f"Available: {', '.join(SUPPORTED_ENVIRONMENTS)}")
    return True

def list_environments() -> None:

    print("Available Devlab environments:")

    for environment in SUPPORTED_ENVIRONMENTS:
        print(f" • {environment}")

def build_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    subprocess.run(
        [
            "docker",
            "compose",
            "build",
            environment
        ],
        check=True,
    )

def run_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            environment,
            "bash",
        ],
        check=True,
    )

def verify_environment(environment: str) -> None:
    if not is_valid_environment(environment):
        return

    commands = VERIFY_COMMANDS.get(environment)

    if commands is None:
        print(f"No verification commands defined fo '{environment}'.")

    script = " && ".join(commands)

    subprocess.run(
        [
            "docker",
            "compose",
            "run",
            "--rm",
            environment,
            "bash",
            "-c",
            script,
        ],
        check=True,
    )