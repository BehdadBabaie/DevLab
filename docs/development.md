# DevLab Development Guide

This document explains the internal structure of DevLab and the workflow
for developing the project itself.

DevLab is a Python CLI that manages Docker-based programming environments.
The CLI is the control layer; Docker and Docker Compose provide the actual
development environments.

---

## Development Setup

DevLab is developed with Python and `uv`.

Install the project environment:

```bash
uv sync
```

Run the CLI directly from the project:

```bash
uv run devlab --help
```

Run the test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

Before committing changes, both the test suite and Ruff should pass.

---

## Project Architecture

The main Python package is:

```text
devlab/
├── __init__.py
├── __main__.py
├── cli.py
├── commands.py
├── compose.py
├── config.py
├── console.py
└── state.py
```

### `__main__.py`

Provides the module entry point so DevLab can be invoked as:

```bash
python -m devlab
```

The installed `devlab` command ultimately enters the same CLI flow.

### `cli.py`

Defines the command-line interface.

It is responsible for:

- Creating the argument parser.
- Defining subcommands.
- Parsing command-line arguments.
- Dispatching parsed commands to command handlers.

The CLI layer should remain focused on argument parsing and dispatching
rather than implementing Docker operations directly.

### `commands.py`

Contains the application-level command operations.

Examples include:

- Listing environments.
- Building environments.
- Running environments.
- Verifying environments.
- Showing environment status.
- Running diagnostics.
- Displaying configuration and version information.

Docker-specific subprocess execution belongs here rather than in the
argument parser.

### `compose.py`

Provides access to the Docker Compose configuration.

It is responsible for operations such as:

- Locating the configured Compose file.
- Reading Compose configuration.
- Discovering available services.
- Validating the expected `services` structure.

This keeps Compose-file handling separate from the CLI.

### `config.py`

Provides DevLab configuration and validation.

Configuration should describe how DevLab operates rather than contain
environment-specific Docker implementation details.

### `console.py`

Provides the shared Rich console used by the CLI.

Keeping console creation in one place prevents individual modules from
creating unrelated console instances.

### `state.py`

Contains DevLab state-related functionality.

State should be kept separate from command parsing and Docker invocation
so that state management can evolve without coupling it to the CLI layer.

---

## Command Flow

A typical command follows this general path:

```text
User
 │
 ▼
devlab CLI
 │
 ▼
cli.py
 │
 ├── parse arguments
 └── dispatch handler
       │
       ▼
   commands.py
       │
       ├── compose.py
       ├── config.py
       └── subprocess / Docker Compose
              │
              ▼
           Docker
```

For example:

```bash
uv run devlab build rust
```

roughly follows:

```text
devlab build rust
        │
        ▼
    cli.py
        │
        ▼
 commands.py
        │
        ▼
 docker compose build rust
        │
        ▼
    Docker
```

This separation is intentional. The CLI should not need to know the
details of how Docker Compose executes a build.

---

## Error Handling

Docker-related failures are converted into DevLab-level errors where
appropriate.

For example, a missing Docker executable and a failed Docker command are
different underlying failures, but the CLI should present both as useful
user-facing errors instead of exposing raw Python tracebacks.

When adding a new command:

1. Identify expected operational failures.
2. Convert low-level exceptions into meaningful application errors.
3. Present the error through the CLI.
4. Add tests for the failure path.

---

## Testing

Tests are organized around the main application components:

```text
tests/
├── test_cli.py
├── test_commands.py
├── test_compose.py
└── test_config.py
```

### CLI tests

Verify argument parsing and command dispatch behavior.

### Command tests

Verify application-level command behavior without requiring real Docker
operations when a subprocess can be mocked.

### Compose tests

Verify Compose-file loading, service discovery, and validation.

### Configuration tests

Verify configuration defaults and validation behavior.

---

## Testing Philosophy

Tests should avoid depending on a developer's local Docker state whenever
possible.

For example, command tests can replace `subprocess.run` with a test
double and verify how DevLab reacts to:

- Successful commands.
- Missing Docker.
- Failed Docker commands.

This keeps the test suite fast and deterministic.

Actual Docker builds should be treated as environment/integration checks,
not as a prerequisite for every unit test.

---

## Adding a CLI Command

When adding a command:

1. Add the command parser in `cli.py`.
2. Add a handler if the command requires one.
3. Implement the application operation in `commands.py`.
4. Keep Docker/Compose details out of the parser.
5. Add unit tests.
6. Run Ruff.
7. Run the complete test suite.
8. Update the README or documentation if the user-facing interface
   changed.

Avoid adding commands merely because they are technically possible.
A command should make managing DevLab environments easier.

---

## Change Workflow

A normal development cycle is:

```text
Understand the ticket
        │
        ▼
Inspect the existing implementation
        │
        ▼
Make the smallest appropriate change
        │
        ▼
Add or update tests
        │
        ▼
uv run ruff check .
        │
        ▼
uv run pytest
        │
        ▼
Review git diff
        │
        ▼
Commit the completed work
```

Changes should remain focused on the current ticket.

---

## Design Principle

DevLab should remain an environment manager.

When evaluating a proposed feature, ask:

1. Does it make programming environments easier to use?
2. Does it make environments more reproducible or reliable?
3. Does it make environments easier to manage?
4. Does it make adding or maintaining environments easier?

If a feature does not serve these goals, it probably does not belong in
DevLab.
