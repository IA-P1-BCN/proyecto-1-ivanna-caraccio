# TaxiTech — Software Taximeter

## What is TaxiTech?

TaxiTech is a software taximeter prototype for a taxi driver. It calculates the
fare of a race in real time while the vehicle is stopped or moving, keeps a
daily history of races, logs every relevant event and protects its sensitive
operations with a password. It runs locally with two interchangeable
interfaces: a touch-friendly **GUI** with big buttons (default) and a classic
**terminal CLI**.

---

## Stack Tech

![Python](https://img.shields.io/badge/Python-3.10%2B-3776AB?logo=python&logoColor=white)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-000000?logo=tcl&logoColor=white)
![pytest](https://img.shields.io/badge/tested%20with-pytest-262522?logo=pytest&logoColor=white)
![Ruff](https://img.shields.io/badge/linter-Ruff-D7FF64?logo=ruff&logoColor=black)

| Layer | Technology |
|---|---|
| Language | Python ≥ 3.10 (developed on 3.14) |
| GUI | Tkinter (stdlib) |
| CLI | Python stdlib (`input`/`print`) |
| Logging | `logging` (stdlib) |
| Persistence | JSON files (`data/`, `config/`) |
| Testing | `pytest` (51 tests) |
| Lint | `ruff` (line length 88) |

**No runtime dependencies** — everything the app needs ships with Python.

---

## Features

- **Race lifecycle** — start, switch between *stopped* / *moving*, finish.
- **Real-time fare** — updated every second from configurable rates
  (0.02 €/s stopped, 0.05 €/s moving by default).
- **Race cycles** — start a new race right after finishing the previous one.
- **Daily history** — every race persisted in `data/race_history.json` with
  the day's accumulated total.
- **Configurable rates** — `config/rates.json`, no code changes needed (US-07).
- **Logging** — key events and unexpected errors written to `logs/taximeter.log`.
- **Password access** — SHA-256 hash stored in `config/auth.json`, never in
  plain text (US-08).
- **Dual interface** — GUI with big touch-friendly buttons for
  phone/tablet (default) and a terminal CLI behind `--cli` (US-09).

---

## Structure

```
proyecto-1-ivanna-caraccio/
├── src/
│   ├── domain/            # Entities & business rules (Carrera, Rates, Password…)
│   ├── application/       # Use cases (StartRace, FinishRace, ValidateAccess…)
│   ├── infrastructure/    # IO: persistence, config readers, logging
│   ├── interfaces/        # Entry points: gui.py, cli.py, theme, formatting
│   └── main.py            # Composition root (wires everything together)
├── config/                # auth.json (hash), rates.json (fares)
├── data/                  # race_history.json (daily history)
├── logs/                  # taximeter.log
├── docs/                  # taxitech-backlog.md (the spec)
└── tests/                 # pytest suite
```

**Why this structure?** The code follows SOLID layered architecture so that
each layer has a single reason to change:

- **`domain/`** is pure business logic — no imports from IO, frameworks or
  interfaces, so the rules of the taximeter are testable in isolation.
- **`application/`** orchestrates the domain through use cases; both interfaces
  (GUI and CLI) reuse the *same* use cases — no duplicated business logic.
- **`infrastructure/`** isolates everything that talks to the outside world
  (files, JSON, logs). Swapping a JSON store for a database would only touch
  this layer.
- **`interfaces/`** contains only entry points and presentation concerns.
  This is why adding the GUI required **zero changes** to `domain/` or
  `application/`.

The result: 51 passing tests, and two interchangeable UIs over the same core.

---

## How to Run

### Clone the repo

```bash
git clone git@github.com:IA-P1-BCN/proyecto-1-ivanna-caraccio.git
cd proyecto-1-ivanna-caraccio
```

### Run it

```bash
python src/main.py         # GUI (Tkinter) — default
python src/main.py --cli   # terminal interface
```

Both interfaces ask for the password on startup (default: `taxi123`).

### Play

1. **INICIAR CARRERA** — the race starts and the fare begins to accumulate.
2. Toggle **PARADO** / **EN MOVIMIENTO** — watch the amount grow in real time.
3. **FINALIZAR CARRERA** — a summary shows the totals and the race is saved.
4. **HISTÓRICO DE HOY** — review today's races and the accumulated income.
5. **SALIR** (or the window ✕ button) — any active race is finished and saved first.

### Quality checks

```bash
python -m pytest -q   # run the test suite
ruff check .          # lint
```

---

## GitHub Projects

Work is organized on the **"P1 IA - Taximetro"** project board, driven by the
spec in [`docs/taxitech-backlog.md`](docs/taxitech-backlog.md):

1. **Spec → issues**: each user story of the backlog becomes a GitHub issue
   labelled `user story`, split into smaller issues labelled `subtask`
   (plus `architecture` / `documentation` for foundations and docs).
2. **Issues → board**: all issues live on the project board so progress is
   visible at a glance (to-do / in progress / done).
3. **Issue → branch → PR**: every issue gets its own branch
   (`9-us-09-visual-ui`), developed through a pull request merged into `dev`,
   and from `dev` into `main`.

**Why this organization?**

- **Traceability** — every line of code maps back to a backlog entry and an
  issue; the spec is the single source of truth.
- **Small, reviewable units** — sub-issues keep PRs focused instead of one
  giant merge.
- **Parallel-safe** — feature branches avoid stepping on each other.
- **Visibility** — the board shows the real state of the project at any time.

---

## Develop Methods

The project mixes two AI-assisted development approaches:

**Spec-driven AI development.** Before any code, requirements are written down
as user stories with acceptance criteria and broken into sub-issues. Each unit
of work follows the same loop: agree on a plan with the AI → implement it step
by step → run `ruff` and `pytest` → review → commit with a conventional message
(`feat:`, `fix:`, `docs:`, `test:`). The AI proposes, the human approves every
step — the spec stays in charge of the code, not the other way around.

**Vibe coding to learn.** Especially at the beginning, the AI assistant
(**Claude Code**) was used in a more free-form, exploratory way — asking about
Python syntax, idioms and conventions, trying things out and reading the
results — to learn Python *while* building the project. The tests and the
backlog keep that experimentation honest: code only ships when the suite is
green.

---

## Decisions Taken

### Tkinter for the visuals (US-09.1)

| Option | Pros | Cons |
|---|---|---|
| **Tkinter** | In Python stdlib, no new dependencies, mature and enough for touch buttons and a real-time fare | Basic aesthetics |
| PySimpleGUI | Compact syntax | External dependency; its licensing/commercial terms since 2022 are problematic for free use |
| Kivy | Real touch/responsive design | Heavy dependency and a learning curve disproportionate to a prototype |

**Decision: Tkinter.** It meets the US-09 criteria (big buttons, real-time
amount and status, tablet-sized window) without adding dependencies, keeping
the prototype's stdlib-only approach and the SOLID/DRY rules of `AGENTS.md`.

### SHA-256 for the password (US-08)

The password is never stored in plain text: only its SHA-256 hash lives in
`config/auth.json`, and passwords are never written to the logs.

- **Why SHA-256 (stdlib) instead of bcrypt/argon2:** a local, single-user
  prototype cannot justify external dependencies; `hashlib` ships with Python
  and is enough to avoid *accidental* disclosure (shoulder-surfing, leaked
  config file).
- **Trade-off acknowledged:** SHA-256 without salt is not resistant to
  brute-force on a public system — an online service would need bcrypt/argon2
  with per-user salts.

To set a new password, hash it and update `config/auth.json`:

```bash
python -c "import hashlib; print(hashlib.sha256('NUEVA'.encode('utf-8')).hexdigest())"
```

Default password: `taxi123`.

### Stdlib-only, zero runtime dependencies

No external packages are required to *run* the app (only `pytest` and `ruff`
as dev tools). Everything — GUI, hashing, logging, JSON — comes from the
standard library, which keeps the prototype portable and easy to install.

### GUI by default, CLI behind `--cli`

The target user is a driver on a tablet, so `python src/main.py` opens the
graphical interface. The terminal CLI remains one flag away, which is handy
for debugging, scripts and CI.

### JSON file persistence

The daily history lives in `data/race_history.json`. A full database would be
overkill for a single-user prototype; a JSON file is transparent, versionable
and trivial to inspect (and the repository interface makes it swappable later).

### Rates in a config file

Fares are read from `config/rates.json` (US-07), so changing a price never
requires touching (and possibly breaking) the business logic.

---

## Future Implementations

The next milestone is to evolve the prototype into a connected application:

- **REST API with FastAPI** — the app will consume a FastAPI service built on
  top of a database created specifically for this software, instead of talking
  directly to files.
- **JSON → database migration** — race history and configuration will move
  from JSON files (`data/`, `config/`) to reading/writing entities in that
  database, through the existing repository interfaces in `infrastructure/`,
  so the swap stays invisible to `domain/` and `application/`.
- **Web panel for the fleet manager** — a dashboard served by the same
  backend and accessible from any browser, so the person in charge of the
  fleet can check the race history **without installing anything**, including
  **previous days** (today the GUI/CLI only show today's history).
