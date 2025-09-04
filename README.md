# Zepp Cloud Python SDK

Python SDK for Zepp/Amazfit cloud and accompanying CLI supporting offline export.

## Status
- Transport/auth/config implemented (httpx sync transport with retries + pacing).
- Band daily summaries implemented (models, parser, CLI) with docs.
- Band detail implemented with HR decoding (`data_hr`) and CLI; docs updated.
- Events implemented (SDK+CLI): Stress, Blood Oxygen (click/osa_event/odi), PAI, Readiness.
- CLI binary `zepp-cloud` available via editable install.
- Not published to PyPI yet.

## Next Steps
- Workouts history/detail endpoints.

We will update this README after each major milestone.

## Quickstart

Install from source (editable):
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate
python -m pip install -U pip
pip install -e .
```

Set required environment variables (see docs for obtaining values):
```bash
export HUAMI_TOKEN="<your apptoken>"
export HUAMI_USER_ID="<your user id>"
export TZ="America/New_York"  # or your IANA timezone
```

Minimal SDK example:
```python
from zepp_cloud.client import ZeppClient

client = ZeppClient(apptoken=HUAMI_TOKEN, user_id=HUAMI_USER_ID, timezone="America/New_York")
try:
    days = client.events.stress(days=14, time_zone="America/New_York")
    print(days[0].date, days[0].avg if days else None)
finally:
    client.close()
```

CLI examples:
```bash
# Band daily summaries (JSONL by default)
zepp-cloud band summary --from 2025-08-20 --to 2025-08-21 --tz "$TZ" --user "$HUAMI_USER_ID" --token "$HUAMI_TOKEN"

# Band detail with HR curve
zepp-cloud band detail --from 2025-08-20 --to 2025-08-20 --tz "$TZ" --user "$HUAMI_USER_ID" --token "$HUAMI_TOKEN" --pretty

# Events — Stress / Blood Oxygen / PAI / Readiness
zepp-cloud events stress --days 14 --tz "$TZ" --user "$HUAMI_USER_ID" --token "$HUAMI_TOKEN" --pretty
zepp-cloud events blood-oxygen --days 14 --tz "$TZ" --user "$HUAMI_USER_ID" --token "$HUAMI_TOKEN" --subtype odi
zepp-cloud events pai --days 30 --tz "$TZ" --user "$HUAMI_USER_ID" --token "$HUAMI_TOKEN" --pretty
zepp-cloud events readiness --days 7 --tz "$TZ" --user "$HUAMI_USER_ID" --token "$HUAMI_TOKEN" --pretty
```

## Local Development (temporary)
```bash
python3 -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
python -m pip install -U pip
```
```

## Security
- See `SECURITY.md`. Never share real tokens in issues, PRs, or logs.

## License
- Apache-2.0, see `LICENSE` and `NOTICE`.

## Documentation
- Documentation map: `docs/documentation-map.md`
- Band summaries guide: `docs/usage/band.md`
- Events (stress, blood oxygen, PAI, readiness): `docs/usage/events.md`
