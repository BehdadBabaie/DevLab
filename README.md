# DevLab

DevLab is a CLI for managing Docker-based programming environments.

Its goal is to let you learn or experiment with programming languages
without installing their development toolchains directly on your host
machine.

For example, instead of installing Rust, Cargo, Go, or Node.js on your
Windows machine, DevLab provides those tools inside Docker environments.

---

## Why DevLab?

Learning a programming language often requires installing its compiler,
runtime, package manager, and other development tools.

That can leave a host machine with many different toolchains that may
conflict with each other or are no longer needed after learning the
language.

DevLab takes a different approach:

```text
Host Machine
│
├── DevLab
└── Docker
    │
    ├── Python
    ├── Go
    ├── Rust
    └── Node.js
```

The programming toolchains live inside Docker while the project
workspace is mounted into the environments.

The result is a simple way to experiment with different programming
languages while keeping the host machine relatively clean.

---

## Features

- Docker-based programming environments
- Docker Compose integration
- CLI for managing environments
- Isolated language toolchains
- Reproducible environments
- Shared `/workspace` directory
- Environment verification
- Docker diagnostics
- Configuration support
- Verbose command output
- VS Code Dev Container support
- Automated tests

---

## Requirements

DevLab itself requires:

- Python 3.11 or newer
- Docker
- [uv](https://docs.astral.sh/uv/)

Docker must be available on the host machine because DevLab uses Docker
Compose to create and run the programming environments.

VS Code is optional. It can be used with the Dev Container configuration
included in the repository.

---

## Getting Started

After cloning the repository, install the project environment with `uv`:

```bash
uv sync
```

You can then run DevLab with:

```bash
uv run devlab --help
```

---

## CLI

DevLab provides a single interface for managing its environments.

### List environments

```bash
uv run devlab list
```

This discovers the environments defined in the project's Compose file.

### Build an environment

Build an environment before using it:

```bash
uv run devlab build rust
```

To build without using Docker's build cache:

```bash
uv run devlab build rust --no-cache
```

### Run an environment

Start an interactive shell inside an environment:

```bash
uv run devlab run rust
```

A specific shell can be selected:

```bash
uv run devlab run rust --shell sh
```

If no shell is specified, DevLab uses the configured default shell.

### Verify an environment

DevLab can verify the development tools installed in supported
environments:

```bash
uv run devlab verify rust
```

For example, the Rust environment checks:

```text
rustc --version
cargo --version
```

The Node.js environment checks:

```text
node --version
npm --version
```

The Python environment checks:

```text
python3 --version
uv --version
```

The Go environment checks:

```text
go version
```

### Diagnose DevLab

```bash
uv run devlab doctor
```

The `doctor` command checks the local Docker setup and DevLab
configuration and reports problems that may prevent environments from
working correctly.

### Show configuration

```bash
uv run devlab config
```

### Show the DevLab version

```bash
uv run devlab version
```

---

## Verbose Mode

DevLab supports verbose output for commands that invoke Docker.

For example:

```bash
uv run devlab --verbose build node
```

Verbose mode displays the Docker command being executed:

```text
$ docker compose build node
```

This can be useful when troubleshooting or when you want to see what
DevLab is doing underneath the CLI.

---

## Available Environments

The current Compose configuration provides the following environments:

| Environment | Description                         |
|-------------|-------------------------------------|
| Base        | Common base development environment |
| Python      | Python development environment      |
| Go          | Go development environment          |
| Rust        | Rust development environment        |
| Node.js     | Node.js development environment     |

The environments are defined in `compose.yaml`.

Each language environment has its own Dockerfile and image.

---

## Workspace

DevLab environments use:

```text
/workspace
```

as their working directory.

The repository is mounted into this directory by Docker Compose.

This means the development tools are provided by the container while
the project files remain available on the host machine.

For example:

```text
Host
│
└── DevLab project
        │
        │ Docker volume mount
        ▼
    Container
        │
        └── /workspace
```

Changes made to files inside `/workspace` are therefore reflected in
the project on the host machine.

---

## Configuration

DevLab can be configured with a `devlab.yaml` file in the project root.

The available settings are:

```yaml
compose_file_name: compose.yaml
default_shell: bash
```

### `compose_file_name`

Specifies the Compose file DevLab should use.

The default is:

```yaml
compose_file_name: compose.yaml
```

### `default_shell`

Specifies the shell used by `devlab run` and `devlab verify` when a
shell is not explicitly provided.

The default is:

```yaml
default_shell: bash
```

For example:

```yaml
compose_file_name: compose.yaml
default_shell: sh
```

---

## VS Code Dev Containers

DevLab includes a VS Code Dev Container configuration.

This allows the repository to be opened inside a development container
while keeping the language toolchains inside Docker.

VS Code and the Dev Containers extension are optional. The DevLab CLI
can be used independently.

---

## Repository Structure

```text
DevLab/
│
├── .devcontainer/
│   ├── devcontainer.json
│   └── post-create.sh
│
├── devlab/
│   ├── __init__.py
│   ├── __main__.py
│   ├── cli.py
│   ├── commands.py
│   ├── compose.py
│   ├── config.py
│   ├── console.py
│   └── state.py
│
├── docker/
│   ├── base/
│   ├── python/
│   ├── go/
│   ├── rust/
│   ├── node/
│   └── scripts/
│
├── docs/
├── tests/
├── compose.yaml
├── devlab.yaml
├── pyproject.toml
├── uv.lock
└── README.md
```

---

## Development

DevLab is itself a Python project.

Install the project environment:

```bash
uv sync
```

Run the test suite:

```bash
uv run pytest
```

Run Ruff:

```bash
uv run ruff check .
```

Both should pass before committing changes.

---

## Adding New Environments

Programming environments are defined through Docker Compose services
and their corresponding Dockerfiles.

A new environment should integrate with the existing DevLab workflow:

```text
devlab list
     │
     ▼
devlab build <environment>
     │
     ▼
devlab run <environment>
     │
     ▼
devlab verify <environment>
```

Where appropriate, a new environment should also have verification
commands and supporting documentation.

---

## Roadmap

The project roadmap is maintained in:

```text
docs/RoadMAP.md
```

The primary focus is expanding DevLab with additional programming
environments while improving the CLI and the reliability of the
environment-management workflow.

---

## Scope

DevLab is an **environment manager**.

It is not intended to become:

- A programming-language learning platform
- A programming tutorial system
- An IDE
- A replacement for Docker
- A package-management abstraction

The core idea should remain:

> Provide a useful programming environment without requiring its
> development toolchain to be installed directly on the host machine.
