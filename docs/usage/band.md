# Band Summaries

Fetch daily summaries from `/v1/data/band_data.json` and parse activity and sleep totals.

## Prerequisites
- apptoken (HUAMI_TOKEN)
- user_id (HUAMI_USER_ID)
- IANA timezone for local day handling (e.g., `America/New_York`)

## Quick Example
```python
from zepp_cloud import ZeppClient

client = ZeppClient(
    apptoken="<HUAMI_TOKEN>",
    user_id="<HUAMI_USER_ID>",
    timezone="America/New_York",
)

rows = client.band.get_summary("2025-08-20", "2025-08-21")
for r in rows:
    print(r.date, r.steps_total, r.distance_m, r.calories_kcal, r.resting_hr)

client.close()
```

## Returned Model
`client.band.get_summary()` returns a `list[BandDailySummary]` with:
- `date`: `YYYY-MM-DD`
- `steps_total`, `distance_m`, `calories_kcal`
- `sleep_start_ms`, `sleep_end_ms` (epoch ms)
- `sleep_deep_min`, `sleep_light_min`, `resting_hr` (optional)
- `raw_summary`: the decoded `summary` Base64 JSON
- `raw_item`: the original item from the server response

Notes
- The server may use `summary` or `sum`; the SDK supports both.
- Some devices omit `rhr` (resting HR); it will be `None` in that case.

## Configuration and Regions
Change the base host if your account is tied to a regional variant:
```python
from zepp_cloud.config import ZeppConfig
from zepp_cloud import ZeppClient

cfg = ZeppConfig(band_base="https://api-mifit-de2.huami.com")
client = ZeppClient(apptoken="...", user_id="...", timezone="Europe/Berlin", config=cfg)
```

## HTTP/Headers
The SDK injects required headers per request:
- `apptoken: <HUAMI_TOKEN>`
- `appPlatform: web`
- `appname: com.xiaomi.hm.health`

## Troubleshooting
- Empty results: verify `user_id`, date range, timezone, and region base.
- Errors/429: the SDK retries and paces requests; widen date windows if needed.

## CLI
You can fetch summaries via the CLI.

JSON Lines (default):
```bash
zepp-cloud band summary \
  --from 2025-08-20 \
  --to 2025-08-21 \
  --token "$HUAMI_TOKEN" \
  --user "$HUAMI_USER_ID"
```

Pretty-printed JSON array:
```bash
zepp-cloud band summary \
  --from 2025-08-20 \
  --to 2025-08-21 \
  --token "$HUAMI_TOKEN" \
  --user "$HUAMI_USER_ID" \
  --pretty
```

Detail (HR curve):
```bash
zepp-cloud band detail \
  --from 2025-08-20 \
  --to 2025-08-21 \
  --token "$HUAMI_TOKEN" \
  --user "$HUAMI_USER_ID" \
  --pretty
```

- To include invalid samples (254/255/0) as `null` values in the curve, add `--keep-invalid`.

### HR Decoding Notes
- For devices that return `data_hr` as a Base64 blob, the SDK decodes to 1440 per‑minute samples for the day.
- Values `254` and `255` indicate no reading or not-required; `0` is also treated as invalid.
- By default invalid samples are dropped; with `--keep-invalid`, they appear as `null` BPM.
- Timestamps are anchored to local midnight of the item’s date in your selected timezone and emitted as epoch milliseconds at 1‑minute intervals.

### Device Variance
- Some devices/firmware provide a JSON HR array under `detail.hr`; others only provide binary `data_hr`.
- Sampling frequency can differ when `detail.hr` is present (e.g., finer than 1‑minute); when available, the SDK preserves those native timestamps.
- Binary `data_hr` is interpreted as per‑minute BPM; values `254`, `255`, and `0` are treated as invalid by default.

### Timezone Alignment
- CLI uses `--tz` (defaults to `$TZ` or `UTC`) to align days and generate timestamps.
- Per‑minute `data_hr` timestamps anchor to local midnight in the provided timezone, then convert to epoch ms.
- DST transitions: local days may be 23 or 25 hours; the SDK still emits 1440 per‑minute slots from local midnight, which may not perfectly align with wall‑clock anomalies. If you need strict UTC anchoring, set `--tz UTC`.
