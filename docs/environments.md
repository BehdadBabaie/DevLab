# DevLab Environment Guide

This document explains how programming environments are structured in
DevLab and how to add or maintain one.

The purpose of an environment is to provide a programming toolchain
inside Docker without requiring that toolchain to be installed directly
on the host machine.

---

## Environment Model

Each programming environment is represented by a Docker Compose service.

The general flow is:

```text
compose.yaml
    │
    ├── python
    ├── go
    ├── rust
    └── node
         │
         ▼
    environment Dockerfile
         │
         ▼
    Docker image
         │
         ▼
    DevLab CLI
```

DevLab discovers environments from the Compose configuration rather than
maintaining a separate hard-coded list of language names.

---

## Environment Layout

Language-specific Dockerfiles live under the Docker directory:

```text
docker/
├── base/
├── python/
├── go/
├── rust/
└── node/
```

Each environment should have a clear and predictable Docker build
definition.

The environment should build on the shared base image when appropriate
so that common system setup does not need to be duplicated.

---

## Compose Service

An environment must be represented by a service in `compose.yaml`.

The service name becomes the environment name used by the CLI.

For example:

```yaml
services:
  python:
    build:
      context: .
      dockerfile: docker/python/Dockerfile
```

The environment can then be addressed through:

```bash
uv run devlab build python
uv run devlab run python
uv run devlab verify python
```

The exact Compose configuration should follow the existing project
conventions rather than introducing a second environment model.

---

## Image Naming

DevLab uses the environment name when referring to its Docker image.

For an environment named `python`, the expected image is:

```text
devlab-python
```

For `rust`:

```text
devlab-rust
```

This convention allows the status command to determine whether an
environment image has already been built.

---

## Workspace

Environments use:

```text
/workspace
```

as their working directory.

The project workspace is made available to the container so that the
developer can edit files on the host while running the language
toolchain inside Docker.

The environment should therefore not require the source project to be
copied into the image merely to make interactive development possible.

---

## Toolchain Installation

An environment Dockerfile should install the tools required to make the
environment useful.

For example, a language environment may need:

- The language compiler or runtime.
- Its package manager.
- Basic certificates or network utilities.
- Any small set of tools required for normal development.

Avoid installing unrelated tooling into a language image.

The goal is a useful, focused environment rather than a general-purpose
everything image.

---

## Versioning

Each environment's Dockerfile is the authoritative definition of the
toolchain versions provided by that environment.

DevLab does not maintain a separate environment-version registry.

Toolchain versions should be explicitly declared whenever practical.
DevLab may use version ranges where the underlying package source
requires them, but the supported major or minor version should still
be explicit.

When changing a language or toolchain version:

1. Update the relevant environment Dockerfile.
2. Rebuild the environment image.
3. Run `devlab verify <environment>`.
4. Confirm `devlab status` reports the image as available.
5. Update documentation when the supported version changes.

Version changes should be intentional and isolated from unrelated
changes.

Exact dependency or image digests are not required at this stage.

### Supported Toolchain Versions

The currently supported toolchain versions are:

| Environment | Toolchain version |
|-------------|-------------------|
| Python      | 3.14              |
| Go          | 1.26.6            |
| Rust        | 1.89.0            |
| Node.js     | 22.x              |

## Verification

Every environment should have a meaningful verification command where
practical.

Verification should answer:

> "Is the toolchain I expect actually available inside this environment?"

Examples include:

```text
python3 --version
uv --version
```

```text
go version
```

```text
rustc --version
cargo --version
```

```text
node --version
npm --version
```

Verification should be lightweight and should not require a full
application project.

---

## Adding a New Environment

When adding a new programming language:

### 1. Create the Dockerfile

Add the environment under:

```text
docker/<language>/
```

Follow the structure of the existing environments.

### 2. Add the Compose service

Add a service to:

```text
compose.yaml
```

The service name should be the environment name users will type into
DevLab.

### 3. Add verification

Add the appropriate verification command(s) so DevLab can confirm that
the toolchain is installed.

### 4. Add tests

Test the behavior that belongs to DevLab itself.

For example, verify that:

- The new service is discovered.
- The CLI accepts the environment name.
- Verification is configured correctly.

Do not make the normal unit test suite dependent on actually building
the Docker image.

### 5. Build the environment

Build it with:

```bash
uv run devlab build <language>
```

### 6. Run the environment

Start an interactive environment:

```bash
uv run devlab run <language>
```

### 7. Verify the toolchain

Run:

```bash
uv run devlab verify <language>
```

### 8. Check status

Confirm the image is available:

```bash
uv run devlab status
```

### 9. Update documentation

Update the README and roadmap when the new environment becomes part of
the supported project scope.

---

## Environment Checklist

Before considering an environment complete:

- [ ] Dockerfile exists.
- [ ] Compose service exists.
- [ ] Service name follows project conventions.
- [ ] Image builds successfully.
- [ ] Interactive shell works.
- [ ] `/workspace` is usable.
- [ ] Toolchain version can be verified.
- [ ] DevLab discovers the environment.
- [ ] `devlab build <environment>` works.
- [ ] `devlab run <environment>` works.
- [ ] `devlab verify <environment>` works.
- [ ] `devlab status` reports the image correctly.
- [ ] Automated tests cover the relevant CLI behavior.
- [ ] Documentation is updated.
- [ ] Toolchain version is explicitly defined where practical.
- [ ] Toolchain version can be verified.
- [ ] Updating the toolchain version requires an intentional Dockerfile change.

---

## Keeping Environments Consistent

New environments should follow the same user-facing workflow:

```text
list
 │
 ▼
build <environment>
 │
 ▼
run <environment>
 │
 ▼
verify <environment>
 │
 ▼
status
```

A user should not need to learn a completely different workflow for
each language.

This consistency is one of the main reasons DevLab exists.
