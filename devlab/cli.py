import argparse
from devlab.commands import (
    list_environments,
    build_environment,
    run_environment,
    verify_environment,
)

def main() -> None:
    parser = argparse.ArgumentParser(
        prog="devlab",
        description="Devlab Development Environment Manager",
    )

    parser.add_argument(
        "command",
        choices=["list", "build", "run", "verify"],
        help="Command to execute",
    )

    parser.add_argument(
        "environment",
        nargs="?",
        help="Target environment",
    )

    args = parser.parse_args()

    if args.command == "list":
        list_environments()

    elif args.command == "build":
        build_environment(args.environment)

    elif args.command == "run":
        run_environment(args.environment)

    elif args.command == "verify":
        verify_environment(args.environment)