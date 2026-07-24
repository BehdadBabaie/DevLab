# DevLab Architecture

## Mission

DevLab is a Docker-based development platform that provides reproducible, ready-to-use development environments for programming languages and developer tools without requiring local installation on the host operating system.

---

## Goals

- No language toolchains installed on Windows
- Reproducible development environments
- Consistent project structure
- Easy to extend with new languages and tools
- VS Code Dev Container support

---

## Design Principles

### Reproducible

Anyone should be able to clone the repository and obtain the same environment.

### Isolated

Each environment is independent.

### Consistent

Every language follows the same directory layout.

### Minimal

Only install tools necessary for development.

### Extensible

Adding a new language should require minimal effort.

---

## Repository Layout

docker/
docs/
examples/
scripts/

---

## Supported Categories

- Programming Languages
- Databases
- DevOps Tools
- Cloud CLIs
- Other Developer Utilities
