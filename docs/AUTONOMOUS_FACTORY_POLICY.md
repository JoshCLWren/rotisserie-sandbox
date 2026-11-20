# Autonomous factory policy

- Work only on the assigned issue or PR.
- Product correctness first: meet the acceptance criteria with tests.
- A PR merges only after CI passes on its exact head and an independent review approves it.
- Never merge, push `main`, change workflows, or edit this policy.
- Pre-push fast checks: ruff, ty and the targeted tests must pass before the wrapper pushes.
