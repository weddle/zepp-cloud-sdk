# Events — Stress

Fetch stress events from `/users/<user_id>/events` with `eventType=all_day_stress`.

## Prerequisites
- apptoken (HUAMI_TOKEN)
- user_id (HUAMI_USER_ID)
- IANA timezone used by the server for windowing and by the SDK for grouping (e.g., `America/New_York`)

## Quick Example (SDK)
```python
from zepp_cloud import ZeppClient

client = ZeppClient(apptoken="<HUAMI_TOKEN>", user_id="<HUAMI_USER_ID>", timezone="America/New_York")

# Last 14 days, grouped by local day in the provided timezone
rows = client.events.stress(days=14, time_zone="America/New_York")
for d in rows:
    print(d.date, len(d.points), d.min, d.max, d.avg)

client.close()
```

## CLI
Default JSON Lines (one day per line):
```bash
zepp-cloud events stress \
  --days 14 \
  --tz America/New_York \
  --user "$HUAMI_USER_ID" \
  --token "$HUAMI_TOKEN"
```

Pretty-printed JSON array:
```bash
zepp-cloud events stress \
  --days 14 \
  --tz America/New_York \
  --user "$HUAMI_USER_ID" \
  --token "$HUAMI_TOKEN" \
  --pretty
```

## Data Shape
- Response: `{ items: [...] }`
- Each item contains `data` as a JSON string encoding an array of `{ time: <epoch_ms>, value: <int> }` at ~5‑minute cadence (may vary by device).
- The SDK parses the array into points and groups by local day using the same `timeZone` you request with.
- The SDK also computes simple stats (min/max/avg) per local day.

## Timezone Guidance
- Pass the same TZ to the server and the SDK/CLI for consistent grouping (e.g., `--tz America/New_York`).
- Grouping is by local day boundaries in that timezone.

## Limits and Windowing
- The endpoint supports `limit` (typically 1000 items). For large windows, the SDK splits the request into day chunks so you get all items across the span.
- You can specify an explicit window with `from_ms`/`to_ms` if needed; otherwise, `days` creates a window ending at “now”.

