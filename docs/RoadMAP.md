# DevLab Roadmap

## Mission

DevLab is a CLI for providing ready-to-use, reproducible programming
environments without requiring the corresponding development toolchains
to be installed on the host machine.

The primary use case is:

> "I want to learn or experiment with a programming language without
> installing its compiler, runtime, package manager, or development
> environment locally."

DevLab manages environments. It is not intended to be a programming
language learning platform, IDE, tutorial system, or alternative to
Docker.

---

## Phase 1 — Programming Environments

Provide practical, isolated environments for commonly learned
programming languages.

### Current environments

- [x] Python
- [x] Go
- [x] Rust
- [x] Node.js

### Planned environments

- [ ] C
- [ ] C++
- [ ] Java
- [ ] C#
- [ ] Zig
- [ ] Kotlin

Additional languages can be added when there is a clear use case.

### Environment requirements

Every environment should provide, where applicable:

- [ ] Reproducible Docker image
- [ ] Interactive shell
- [ ] Persistent workspace
- [ ] Toolchain/version verification
- [ ] VS Code Dev Container support
- [ ] Minimal smoke test
- [ ] Environment documentation

---

## Phase 2 — DevLab CLI

Provide a consistent interface for discovering and managing
environments.

### Current commands

- [x] `devlab list`
- [x] `devlab build`
- [x] `devlab run`
- [x] `devlab verify`
- [x] `devlab version`
- [x] `devlab doctor`
- [x] `devlab config`

### Current CLI capabilities

- [x] Verbose output
- [x] Custom shell selection
- [x] Docker command error handling
- [x] Configuration validation
- [x] Compose file validation
- [x] Automated tests

### Future CLI improvements

- [ ] Improve environment discovery and diagnostics
- [ ] Improve environment status reporting
- [ ] Improve error messages and recovery guidance
- [ ] Add useful environment management commands when justified

New commands should only be added when they directly improve
environment management.

---

## Phase 3 — Environment Maintenance

Keep environments reliable and usable over time.

- [ ] Define environment versioning strategy
- [ ] Define toolchain update strategy
- [ ] Detect outdated environments where useful
- [ ] Improve environment health checks
- [ ] Document supported versions
- [ ] Establish a consistent environment update workflow

---

## Phase 4 — Developer Tools and Services

Expand DevLab beyond programming languages only when the same core
principle applies:

> Provide a useful development environment or tool without requiring
> it to be installed on the host machine.

Possible future environments:

- [ ] Database environments
- [ ] DevOps tools
- [ ] Cloud CLIs
- [ ] Other development utilities

These are intentionally future scope and should not distract from the
core programming-environment goal.

---

## Phase 5 — Stable Release

Prepare DevLab for a stable release once the environment system and CLI
are mature.

- [ ] Finalize supported environments
- [ ] Finalize CLI interface
- [ ] Finalize documentation
- [ ] Establish release/versioning policy
- [ ] Verify clean installation and usage workflow
- [ ] Release DevLab 1.0

---

## Guiding Principles

When considering a new feature, ask:

1. Does this make it easier to use a development environment without
   installing its toolchain locally?
2. Does this make environments more reproducible or reliable?
3. Does this make managing environments easier?
4. Does this make adding or maintaining environments easier?

If the answer is no to all four, the feature probably does not belong
in DevLab.

DevLab should remain an environment manager, not become a programming
language learning platform.
