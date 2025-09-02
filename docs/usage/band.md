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

