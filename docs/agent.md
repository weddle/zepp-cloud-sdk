# Agent Interaction Guidelines

These preferences describe how our AI coding agent collaborates in this repo.

## Principles

- Be concise, clear, and actionable.
- Favor small, focused patches that align with existing style.
- Avoid unrelated changes; fix root causes within scope.

## Network and Data

- No external network calls without explicit maintainer approval.
- Use mocks/fixtures and `respx` for transport tests.
- Never commit or log secrets; redact tokens.

## Planning and Changes

- Maintain a lightweight plan with clear steps; update as work progresses.
- Pause at sprint boundaries or before broad refactors for confirmation.
- Document assumptions and next steps in PR descriptions.

## Testing and Quality

- Add targeted tests with new code; keep CI green.
- Use Ruff (lint+fmt) locally before PRs; MyPy is currently disabled in hooks/CI.
- Keep public APIs typed and documented.
- At the end of each sprint (before pushing changes), ensure local gates pass:
  - `pre-commit run --all-files` (ruff-format, ruff lint, EOF/trailing hooks)
  - `ruff format --check .` and `ruff check .`
  - `pytest -q`
  - Fix issues and rerun until clean; only then push.

## Files and Patches

- Use minimal, surgical diffs; keep filenames and structure stable unless agreed.
- Update docs when adding capabilities or changing behavior.

## Approvals and Safety

- Ask before destructive actions (e.g., file deletions, mass renames).
- Prefer opt-in flags for debug output; default to safe behavior.

## Hand-off Notes

- Summarize what changed, why, and any follow-ups.
- Reference exact files/paths touched for easy review.
