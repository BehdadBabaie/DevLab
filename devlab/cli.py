import argparse

from devlab.commands import (
    build_environment,
    doctor,
    list_environments,
    run_environment,
    show_config,
    show_version,
    verify_environment,
)
from devlab.console import console
from devlab.state import state


def main() -> None:
    try:
        _main()
    except ValueError as error:
        console.print("[bold red]✗ Invalid configuration[/]")
        console.print()
        console.print(error)
        raise SystemExit(1)


def _main() -> None:
    parser = argparse.ArgumentParser(
        prog="devlab",
        description="Devlab Development Environment Manager",
    )

    parser.add_argument(
        "-v",
        "--verbose",
        action="store_true",
        help="Enable verbose output",
    )

    subparsers = parser.add_subparsers(
        dest="command",
        required=True,
    )

    list_parser = subparsers.add_parser(
        "list",
        help="List available environments.",
    )

    list_parser.set_defaults(func=handle_list)

    version_parser = subparsers.add_parser(
        "version",
        help="Show DevLab version.",
    )

    version_parser.set_defaults(func=handle_version)

    doctor_parser = subparsers.add_parser(
        "doctor",
        help="Check the DevLab environment.",
    )

    doctor_parser.set_defaults(func=handle_doctor)

    config_parser = subparsers.add_parser(
        "config",
        help="Show the active configuration.",
    )

    config_parser.set_defaults(func=handle_config)

    build_parser = subparsers.add_parser(
        "build",
        help="Build an environment.",
    )

    build_parser.add_argument(
        "environment",
        help="Environment to build.",
    )

    build_parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Build the environment without using Docker's cache.",
    )

    build_parser.set_defaults(func=handle_build)

    run_parser = subparsers.add_parser(
        "run",
        help="Run an environment.",
    )

    run_parser.add_argument(
        "environment",
        help="Environment to run.",
    )

    run_parser.add_argument(
        "--shell",
        help="Shell to use inside the environment.",
    )

    run_parser.set_defaults(func=handle_run)

    verify_parser = subparsers.add_parser(
        "verify",
        help="Verify an environment."
    )

    verify_parser.add_argument(
        "environment",
        help="Environment to verify.",
    )

    verify_parser.add_argument(
        "--shell",
        help="Shell to use inside the environment.",
    )

    verify_parser.set_defaults(func=handle_verify)

    args = parser.parse_args()

    state.verbose = args.verbose

    args.func(args)


def handle_list(_args: argparse.Namespace) -> None:
    list_environments()


def handle_version(_args: argparse.Namespace) -> None:
    show_version()


def handle_doctor(_args: argparse.Namespace) -> None:
    doctor()


def handle_config(_args: argparse.Namespace) -> None:
    show_config()


def handle_build(args: argparse.Namespace) -> None:
    build_environment(
        args.environment,
        no_cache=args.no_cache,
    )


def handle_run(args: argparse.Namespace) -> None:
    run_environment(
        args.environment,
        shell=args.shell,
    )


def handle_verify(args: argparse.Namespace) -> None:
    verify_environment(
        args.environment,
        shell=args.shell,
    )
