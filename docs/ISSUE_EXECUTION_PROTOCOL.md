# Issue execution protocol

1. Read the issue. Its acceptance criteria are the contract.
2. Make the smallest change that meets every criterion.
3. Add or update tests that prove each criterion.
4. Run `uv run ruff check .`, `uv run ty check` and `uv run pytest -q`. All must pass.
5. Stop. Do not commit or push.
