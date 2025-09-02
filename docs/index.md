# Zepp Cloud Python SDK

High-quality, typed, sync+async Python SDK for Zepp/Amazfit cloud surfaces, with first-class offline export and optional TSDB sinks.

## Status

Early scaffolding. The detailed project plan is maintained locally under `sprints/plan.md` (gitignored).

## Quickstart (placeholder)

```bash
pip install zepp-cloud-sdk
```

```python
from zepp_cloud import ZeppClient, AppTokenAuth

client = ZeppClient(apptoken="...", user_id="...", timezone="America/New_York")
```

## Documentation Map

- References: `docs/references.md`
- Agent Guidelines: `docs/agent.md`
- Security: `SECURITY.md`
- Contributing: `CONTRIBUTING.md`
- Documentation Map: `docs/documentation-map.md`
- Internal plan: `sprints/plan.md` (local, gitignored)
 - Usage: `docs/usage/band.md`, `docs/usage/events.md`
 - Research: `docs/research/band_data.md`, `docs/research/events.md`
