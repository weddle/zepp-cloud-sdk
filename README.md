# Zepp Cloud Python SDK

High-quality, typed, sync+async Python SDK for Zepp/Amazfit cloud surfaces, with first-class offline export and optional TSDB sinks.

## Status
- Sprint 0–1 complete (scaffold, transport/auth/config).
- Sprint 2 complete: Band daily summaries (models, parser, CLI) with docs.
- Sprint 3 complete: Band detail with HR decoding (data_hr) and CLI; docs updated.
- Sprint 4 in progress: Events — Stress implemented (SDK+CLI) and documented.
- Not published to PyPI yet.

## Next Step
- Wrap Sprint 4 (stress events) polish and move to Sprint 5 (Blood oxygen events).

We will update this README after each major milestone.

## Local Development (temporary)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -U pip
```

### Local Dev Loop
Run formatter, linter (with autofix), then tests:
```bash
ruff format .
ruff check . --fix
pytest -q
```

Pre-commit (local only) also runs Ruff format, Ruff lint (autofix), and MyPy:
```bash
pip install pre-commit
pre-commit install
pre-commit run --all-files
```

## Contributing
- See `CONTRIBUTING.md` and `docs/agent.md` for workflow and agent preferences.
- Code of Conduct: `CODE_OF_CONDUCT.md`.

## Security
- See `SECURITY.md`. Never share real tokens in issues, PRs, or logs.

## License
- Apache-2.0, see `LICENSE` and `NOTICE`.

## CI Roadmap
- Current CI: single smoke job on pushes to `main` and PRs; installs minimal deps, runs Ruff format check, Ruff lint, and `pytest -q`.
- Reintroduce later, in order:
  1) Coverage gate with a modest threshold
  2) MyPy in CI
  3) Python version matrix
  4) Extras needed by integration tests

## Documentation
- Documentation map: `docs/documentation-map.md`
- Band summaries guide: `docs/usage/band.md`
 - Events (stress) guide: `docs/usage/events.md`
