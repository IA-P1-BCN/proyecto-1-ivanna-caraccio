# AGENTS.md

## Project

Taximeter — Python prototype for taxi fare calculation.

## Folder Structure (mandatory)

```
taximeter/
├── src/
│   ├── domain/
│   ├── application/
│   ├── infrastructure/
│   └── interfaces/
├── config/
├── logs/
└── tests/
```

## Mandatory Specifications

- **OOP**: All business logic modeled as classes with encapsulated state.
- **SOLID**: Dependency inversion between layers; interfaces define contracts, implementations live in infrastructure.
- **DRY**: Shared utilities (e.g., currency formatting) in a single reusable location — never duplicated.
- **Ask before acting**: Any doubt or ambiguous idea → ALWAYS ask the user first. Never assume. Never omit.
- **Read** or **Modify** ONLY this project and links in `doc/taxitech-backlog.md`

## Architecture

- **domain/**: Entities and business rules (e.g., `Carrera`). No framework or IO imports.
- **application/**: Use cases that orchestrate domain logic (e.g., `IniciarCarrera`).
- **infrastructure/**: IO and external concerns — persistence, config reading, logging.
- **interfaces/**: Entry points (CLI commands, GUI). Must not contain business logic.

## Backlog

Full user stories and acceptance criteria: `doc/taxitech-backlog.md`

## Tech

- Python 3.x, `pytest` for tests.
- Config files in `taximeter/config/` (rates: 0.02€/s stopped, 0.05€/s moving).
- Logs written to `taximeter/logs/`.
