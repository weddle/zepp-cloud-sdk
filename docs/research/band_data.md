# `/v1/data/band_data.json` — Band Daily Summaries and Detail

Validated endpoint for daily activity and sleep totals (and optional detail windows).

## Base and Path
- Host: `https://api-mifit.huami.com` (regional variants exist; keep configurable)
- Path: `/v1/data/band_data.json`

## Required Headers
- `apptoken: <HUAMI_TOKEN>`
- `appPlatform: web`
- `appname: com.xiaomi.hm.health`

## Required Query Parameters
- `query_type`: `summary` or `detail`
- `device_type`: `android_phone`
- `userid`: `<HUAMI_USER_ID>`
- `from_date`: `YYYY-MM-DD`
- `to_date`: `YYYY-MM-DD`

## Response Shape
- HTTP 200 JSON envelope with a `data` field:
  - `data` may be a list of per-day items, or a dict keyed by date
- Each item includes a Base64 string under `summary` (or `sum`) that decodes to JSON:
  - `stp` (steps/activity): `ttl` (steps), `dis` (meters), `cal` (kcal), plus staged segments
  - `slp` (sleep totals): `st` (start ms), `ed` (end ms), `dp` (deep minutes), `lt` (light minutes), optional `rhr` (resting HR)

## Decoding and Mapping
- Base64 decode the `summary` string, parse as JSON, then map fields:
  - `steps_total = stp.ttl`, `distance_m = stp.dis`, `calories_kcal = stp.cal`
  - `sleep_start_ms = slp.st`, `sleep_end_ms = slp.ed`, `sleep_deep_min = slp.dp`, `sleep_light_min = slp.lt`, `resting_hr = slp.rhr?`
- Keep the decoded JSON as `raw_summary` and original item as `raw_item` for provenance.

### Detail and `data_hr`
- Some devices provide an explicit JSON HR array under `detail.hr`. When present, the SDK normalizes it into `(ts_ms, bpm)` pairs.
- Many devices provide HR detail as a Base64-encoded `data_hr` bytestring instead of JSON:
  - 1440 bytes (per minute across the day)
  - Byte values: `254`/`255` → invalid/no reading (often due to sampling frequency), `0` → invalid
  - Other byte values map directly to BPM
- Timestamps are generated at one‑minute intervals anchored to local midnight (`date`/`date_time`) using the same timezone configured in the client/CLI.
- The SDK drops invalid samples by default; pass `--keep-invalid` via CLI to include them as `null` BPM values (or set `keep_invalid=True` when using the resource API).

### Device Variance and Timezones
- Devices/firmware may emit either JSON `detail.hr` (with native timestamps and variable cadence) or only binary `data_hr` (fixed 1440/minute cadence).
- `summary` remains Base64‑encoded JSON with daily totals regardless of device.
- The `date` may appear as `date` or `date_time`. The SDK supports both.
- Timezone alignment: we align per‑day series to local midnight in the configured timezone. On DST transitions, local day length differs; per‑minute `data_hr` still provides 1440 samples. Consumers needing wall‑clock fidelity should treat timestamps with care around transitions or set timezone to `UTC`.

## Example Request (curl)
```bash
curl -sS 'https://api-mifit.huami.com/v1/data/band_data.json' \
  -H 'apptoken: '"$HUAMI_TOKEN" -H 'appPlatform: web' -H 'appname: com.xiaomi.hm.health' \
  --get --data-urlencode 'query_type=summary' \
  --data-urlencode 'device_type=android_phone' \
  --data-urlencode 'userid='"$HUAMI_USER_ID" \
  --data-urlencode 'from_date=2025-08-20' \
  --data-urlencode 'to_date=2025-08-30'
```

## Notes
- Devices and firmware differ; fields like `rhr` may be absent.
- If you consistently see empty results, try a regional base host and confirm your `userid` is correct.
