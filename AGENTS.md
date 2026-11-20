# Agent guide

`ledger` is a tiny expense ledger.

## Layout

- `src/ledger/core.py`: `Entry` and `Ledger`.
- `src/ledger/cli.py`: the `ledger` command line.
- `tests/`: pytest tests. Every behavior change needs a test.

## Commands

```bash
uv sync
uv run ruff format .
uv run ruff check .
uv run ty check
uv run pytest -q
```

## Rules

- Change only what the assigned issue or PR asks for.
- Use `Decimal` for money, never `float`.
- Keep the standard library only. Do not add dependencies.
