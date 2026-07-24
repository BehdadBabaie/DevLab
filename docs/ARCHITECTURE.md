# Architecture Decisions

## ADR-001

Base image is Debian.

Reason:

- Stable
- Huge package ecosystem
- Excellent Docker support

Alternatives considered:

- Ubuntu
- Alpine

Decision:
Debian.

## ADR-002

One image per language.

Reason:
Avoid dependency conflicts between toolchains.
