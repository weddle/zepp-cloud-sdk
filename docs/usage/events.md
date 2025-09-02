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

## Blood Oxygen (SpO₂)

Fetch blood oxygen events and handle subtypes (click, osa_event, odi).

### Quick Example (SDK)
```python
from zepp_cloud import ZeppClient

client = ZeppClient(apptoken="<HUAMI_TOKEN>", user_id="<HUAMI_USER_ID>", timezone="America/New_York")

data = client.events.blood_oxygen(days=14, time_zone="America/New_York")
print(len(data["click"]), len(data["osa_event"]), len(data["odi"]))
client.close()
```

### CLI
All subtypes (grouped) as pretty JSON:
```bash
zepp-cloud events blood-oxygen \
  --days 14 \
  --tz America/New_York \
  --user "$HUAMI_USER_ID" \
  --token "$HUAMI_TOKEN" \
  --pretty
```

Single subtype only (JSONL by default):
```bash
zepp-cloud events blood-oxygen \
  --days 14 \
  --tz America/New_York \
  --user "$HUAMI_USER_ID" \
  --token "$HUAMI_TOKEN" \
  --subtype click
```

### Subtype Mapping
- click: spot checks; `extra.spo2` (history may be present but is not standardized; preserved in `raw_item`).
- osa_event: discrete desaturation events; `extra.spo2_decrease`.
- odi: nightly ODI summary; fields `odi`, `odiNum`, `valid`, `score`, `dispCode`; grouped by local day.

## PAI

Fetch PAI daily summaries from `eventType=PaiHealthInfo` and map key fields.

### Quick Example (SDK)
```python
from zepp_cloud import ZeppClient

client = ZeppClient(apptoken="<HUAMI_TOKEN>", user_id="<HUAMI_USER_ID>", timezone="America/New_York")
rows = client.events.pai(days=30, time_zone="America/New_York")
for r in rows:
    print(r.date, r.daily_pai, r.total_pai, r.rest_hr, r.max_hr)
client.close()
```

### CLI
```bash
zepp-cloud events pai \
  --days 30 \
  --tz America/New_York \
  --user "$HUAMI_USER_ID" \
  --token "$HUAMI_TOKEN" \
  --pretty
```

### Field Mapping
- `daily_pai` ← `dailyPai`
- `total_pai` ← `totalPai`
- `rest_hr` ← `restHr`
- `max_hr` ← `maxHr`
- Zone thresholds (bpm): `zone_low_bpm` (low), `zone_med_bpm` (medium), `zone_high_bpm` (high) — names may vary, parser is lenient
- Zone minutes: `minutes_low`, `minutes_med`, `minutes_high` — names may vary, parser is lenient

## Readiness

Fetch readiness `watch_score` items and preserve companion `watch_score_data` raw payloads.

### Quick Example (SDK)
```python
from zepp_cloud import ZeppClient

client = ZeppClient(apptoken="<HUAMI_TOKEN>", user_id="<HUAMI_USER_ID>", timezone="America/New_York")
rows = client.events.readiness(days=7, time_zone="America/New_York")
for r in rows:
    print(r.date, r.sleep_hrv, r.sleep_rhr, r.hrv_score, r.rhr_score)
client.close()
```

### CLI
```bash
zepp-cloud events readiness \
  --days 7 \
  --tz America/New_York \
  --user "$HUAMI_USER_ID" \
  --token "$HUAMI_TOKEN" \
  --pretty
```

### Field Mapping (watch_score)
- Core: `sleepHRV`, `sleepRHR`
- Component scores: `hrvScore`, `rhrScore`, `skinTempScore`, `rdnsScore`, `phyScore`, `mentScore`, `ahiScore`
- Baselines: `hrvBaseline`, `rhrBaseline`, `skinTempBaseLine`, `mentBaseLine`, `phyBaseline`, `ahiBaseline`, `afibBaseLine`
- Other: `status`, `algVer`, `algSubVer`, optional `deviceId`
- Companion: `watch_score_data.rawData` is preserved in raw for future decode

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
