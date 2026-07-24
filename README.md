# DevLab

A Docker-based development platform providing reproducible environments for programming languages and developer tools.

---

## Why?

Instead of installing multiple SDKs, compilers, interpreters, and CLIs on your Windows machine, DevLab provides isolated development environments using Docker.

---

## Features

- Docker Compose
- VS Code Dev Containers
- Language-specific environments
- Reproducible toolchains
- Minimal host installation

---

## Current Environments

| Environment | Status |
| ----------- | ------ |
| Base        | ✅     |
| Python      | ✅     |
| Go          | ✅     |
| Rust        | 🚧     |

---

## Requirements

- Docker Desktop
- VS Code
- Dev Containers extension

---

## Quick Start

```bash
docker compose build python
docker compose up -d python
```

Open the folder in VS Code and reopen in the Dev Container.

---

## Repository Structure

docker/
docs/
examples/
scripts/

---

## Roadmap

- Rust
- Node.js
- Java
- C#
- C/C++
- Zig
- Databases
- DevOps tools
