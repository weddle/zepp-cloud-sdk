# Contributing

Thanks for your interest in contributing! We welcome issues, docs, code, and test improvements.

Before contributing, please read:

- `CODE_OF_CONDUCT.md`
- `SECURITY.md`
- `NOTICE`

## Development Workflow

- Use Python 3.11+ locally (project supports 3.9–3.13 in CI).
- Create a virtualenv and install dev tools as described in the README (to be added).
- Run lint and tests before opening a PR.

## Commit Sign-off (DCO)

This project uses the Developer Certificate of Origin (DCO). Each commit must be signed off with your real name and email:

```
git commit -s -m "feat: add parser for stress events"
```

The sign-off certifies the DCO 1.1:

> Developer Certificate of Origin 1.1
>
> By making a contribution to this project, I certify that:
>
> (a) The contribution was created in whole or in part by me and I have the right to submit it under the open source license indicated in the file; or
> (b) The contribution is based upon previous work that, to the best of my knowledge, is covered under an appropriate open source license and I have the right under that license to submit that work with modifications, whether created in whole or in part by me, under the same open source license (unless I am permitted to submit under a different license), as indicated in the file; or
> (c) The contribution was provided directly to me by some other person who certified (a), (b) or (c) and I have not modified it.
>
> (d) I understand and agree that this project and the contribution are public and that a record of the contribution (including all personal information I submit with it, including my sign-off) is maintained indefinitely and may be redistributed consistent with this project or the open source license(s) involved.

## Agent Interaction Preferences

We use an AI coding agent to assist with scaffolding and routine tasks. See `docs/agent.md` for detailed expectations. Highlights:

- No external network calls without explicit approval; use mocks/fixtures.
- Small, focused patches; align with repo style; avoid unrelated changes.
- Keep CI green; add targeted tests alongside new code.
- Never commit secrets; redact tokens in logs.

## Pull Requests

- Keep PRs focused and include a short rationale.
- Add/adjust tests and docs to cover changes.
- CI must pass; maintainers review before merge.

