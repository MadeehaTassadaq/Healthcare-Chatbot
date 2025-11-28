<!-- Sync Impact Report:
Version change: 1.0.0 → 1.0.1
List of modified principles:
  - Project Name: Claude Code Constitution → Promotional Video Generation Web App Constitution
Added sections: None
Removed sections: None
Templates requiring updates:
  - .specify/templates/plan-template.md: ⚠ pending
  - .specify/templates/spec-template.md: ⚠ pending
  - .specify/templates/tasks-template.md: ⚠ pending
  - .specify/templates/commands/*.md: ⚠ pending
Follow-up TODOs: None
-->
# Promotional Video Generation Web App Constitution

## Core Principles

### I. Library-First
Every feature starts as a standalone library; Libraries must be self-contained, independently testable, documented; Clear purpose required - no organizational-only libraries

### II. CLI Interface
Every library exposes functionality via CLI; Text in/out protocol: stdin/args → stdout, errors → stderr; Support JSON + human-readable formats

### III. Test-First (NON-NEGOTIABLE)
TDD mandatory: Tests written → User approved → Tests fail → Then implement; Red-Green-Refactor cycle strictly enforced

### IV. Integration Testing
Focus areas requiring integration tests: New library contract tests, Contract changes, Inter-service communication, Shared schemas

### V. Observability & Simplicity
Text I/O ensures debuggability; Structured logging required; Start simple, YAGNI principles


## Additional Constraints

Technology stack requirements, compliance standards, deployment policies, etc.

## Development Workflow

Code review requirements, testing gates, deployment approval process, etc.

## Governance

All PRs/reviews must verify compliance; Complexity must be justified; Use documentation for runtime development guidance

**Version**: 1.0.1 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-28
