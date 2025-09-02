# Zepp Cloud Python SDK

High-quality, typed, sync+async Python SDK for Zepp/Amazfit cloud surfaces, with first-class offline export and optional TSDB sinks.

## Status
- Early scaffolding in progress.
- Repo contains legal/policy docs, docs landing page, agent guidelines, `.gitignore`, `tmp/`, and a local `.venv/` (ignored).
- No published package yet; API and transports not implemented.

## Next Step
- Sprint 0: scaffold packaging and tooling.
  - Add `pyproject.toml` with PEP 621 + setuptools-scm.
  - Create `src/zepp_cloud/` package skeleton and CLI entrypoint.
  - Configure Ruff (lint+fmt), MyPy (strict), Pytest, and pre-commit.
  - Set up GitHub Actions CI (3.9–3.13) running lint, type-check, tests, coverage.

We will update this README after each major milestone.

## Local Development (temporary)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -U pip
```

## Contributing
- See `CONTRIBUTING.md` and `docs/agent.md` for workflow and agent preferences.
- Code of Conduct: `CODE_OF_CONDUCT.md`.

## Security
- See `SECURITY.md`. Never share real tokens in issues, PRs, or logs.

## License
- Apache-2.0, see `LICENSE` and `NOTICE`.

