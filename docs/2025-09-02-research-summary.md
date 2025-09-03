# Zepp/Amazfit Cloud APIs — Working Endpoints Summary (as of 2025-09-02)

This document consolidates everything we validated as “working” across our development and research. It covers authentication, base hosts, query parameters, response decoding, and practical parsing for endpoints that returned data. Only confirmed‑working endpoints are included here.

Use the scripts in this repo as reference implementations:
- `scripts/band_data_dump.py` — daily summaries and detail via `band_data.json`
- `scripts/events_dump.py` — health/event endpoints (stress, SpO₂, PAI, readiness)
- `scripts/readiness_export.py` — normalize readiness to CSV


## 1) Authentication and Headers

Token source
- We use the Huami/Zepp “apptoken” captured from the GDPR export/download flow or the OAuth server callback. See `README.md` (Get Huami Token and User ID) and `scripts/zepp_login.py` for capturing tokens from an `account.huami.com/v1/accounts/connect/huami/callback?...` URL.

Required values
- `HUAMI_TOKEN` — the long token used as the app token
- `HUAMI_USER_ID` — your numeric user id (needed for `/users/<user_id>/events` and as `userid` for `band_data.json`)

Working header set (used across endpoints)
- `apptoken: <HUAMI_TOKEN>`
- `appPlatform: web`
- `appname: com.xiaomi.hm.health`
- `User-Agent: amazfit-download/0.1` (or similar)

Notes
- For all endpoints below, the `apptoken` header is accepted. We do not rely on `Authorization: Bearer` for these.
- Cookie mode (setting `apptoken`/`userid` as cookies) is not required for the working endpoints documented here.
- Validate your token safely with `scripts/verify_token.py`.


## 2) Hosts and Regions

Observed working bases
- Band data and workouts: `https://api-mifit.huami.com` (region variants like `api-mifit-de2.huami.com` may also work)
- Events (stress, SpO₂, PAI, readiness): `https://api-mifit-us2.zepp.com` (region variants like `api-mifit-de2.zepp.com` exist)

Guidance
- Keep the base host configurable. If you see redirects or 404s, try the region host tied to your account.


## 3) Daily Summary and Detail — `/v1/data/band_data.json` (Huami)

Base
- Host: `https://api-mifit.huami.com`
- Path: `/v1/data/band_data.json`

Auth headers
- `apptoken`, `appPlatform: web`, `appname: com.xiaomi.hm.health`

Required query parameters
- `query_type`: `summary` or `detail` (both confirmed working)
- `device_type`: `android_phone`
- `userid`: `<HUAMI_USER_ID>`
- `from_date`: `YYYY-MM-DD`
- `to_date`: `YYYY-MM-DD`

Response shape (confirmed)
- HTTP 200 with JSON envelope:
  - When `data` is a list: per‑day objects
  - When `data` is a dict keyed by date: values are the same per‑day objects
- Each item includes a Base64 string under `summary` (or `sum`) which decodes to JSON with at least:
  - `stp` (steps/activity totals): e.g., `ttl` (steps), `dis` (meters), `cal` (kcal), plus staged segments
  - `slp` (sleep totals/stages): e.g., `st` (start epoch), `ed` (end epoch), `dp` (deep minutes), `lt` (light minutes), `stage` array; many devices include `rhr` (resting HR)

Decoding
- Base64 decode `summary` and parse JSON. See `decode_summary_b64` in `scripts/band_data_dump.py`.

Practical parsing
- Aggregate daily rows from decoded `summary`:
  - Steps: `stp.ttl`, `stp.dis`, `stp.cal`
  - Sleep: `slp.st`, `slp.ed`, `slp.dp`, `slp.lt`, and optionally `slp.rhr`
- For “HR during sleep”, pair `query_type=detail` with the sleep window from `slp` and downsample or window the per‑minute HR curve contained in the detail blob.

Example (Python request skeleton)
```
GET https://api-mifit.huami.com/v1/data/band_data.json
  headers: apptoken, appPlatform=web, appname=com.xiaomi.hm.health
  params: {
    query_type: summary | detail,
    device_type: android_phone,
    userid: <HUAMI_USER_ID>,
    from_date: YYYY-MM-DD,
    to_date: YYYY-MM-DD
  }
```

Reference
- Implementation: `scripts/band_data_dump.py`
- Sample outputs saved under `data/processed/` (band_data)


## 4) Health Events — `GET /users/<user_id>/events` (Zepp)

Base
- Host: `https://api-mifit-us2.zepp.com`
- Path: `/users/<HUAMI_USER_ID>/events`

Auth headers
- `apptoken`, with `appPlatform: web`, `appname: com.xiaomi.hm.health`

Required query parameters
- `eventType`: one of the working types documented below
- `from`: window start, epoch milliseconds
- `to`: window end, epoch milliseconds
- `timeZone`: IANA zone matching how you want the data windowed (e.g., `America/New_York`)
- `limit`: typically `1000` (split windows or paginate if needed)

Notes
- The server returns HTTP 200 with `{ items: [...] }`. Treat “working” as “returns non‑empty items for your account/window”.
- Use consistent time zone logic: derive the local day from the top‑level `timestamp` using the same `timeZone` you send.

Working event types

4.a) Stress — `eventType=all_day_stress`
- Shape: per‑day items, each with a JSON string in `data` containing an array of `{ time: <epoch_ms>, value: <int> }` at ~5‑minute cadence.
- Optional top‑level summaries on the item: `minStress`, `maxStress`, `mediumProportion`.
- Parsing: load `data` as JSON, convert `time` using `timeZone`, compute daily stats (count/min/max/avg). See `docs/research/stress_endpoint.md`.

4.b) Blood Oxygen — `eventType=blood_oxygen`
- Subtypes observed in returned items:
  - `click` — manual measurements; values in `extra` JSON (e.g., `spo2`, `spo2History`).
  - `osa_event` — discrete desaturation events during sleep; `extra.spo2_decrease` magnitude present.
  - `odi` — nightly ODI summary with fields like `odi`, `odiNum`, `valid`, `score`, `dispCode`.
- Parsing: group `odi` per local day; tally `osa_event` counts/magnitudes; record `click` measurements. See `docs/research/blood_oxygen_endpoint.md`.

4.c) PAI — `eventType=PaiHealthInfo`
- Daily summary with keys including `dailyPai`, `totalPai`, `restHr`, `maxHr`, zone thresholds (`low/medium/high` bpm) and zone minutes.
- Parsing: produce a per‑day table of PAI totals and HR zone minutes/thresholds. See `docs/research/pai_endpoint.md`.

4.d) Readiness — `eventType=readiness`
- Returned items include two subtypes:
  - `watch_score` — numeric fields: `sleepHRV`, `sleepRHR`, component scores (`hrvScore`, `rhrScore`, `skinTempScore`, `rdnsScore`, `phyScore`, `mentScore`, `ahiScore`) and baselines (`hrvBaseline`, `rhrBaseline`, `skinTempBaseLine`, `mentBaseLine`, `phyBaseline`, `ahiBaseline`, `afibBaseLine`), plus `status`, `algVer`, `algSubVer`, etc.
  - `watch_score_data` — companion object with `rawData` (opaque/encoded); kept for future decoding.
- Parsing: prefer `watch_score` for analytics; normalize numeric fields, derive ISO time from `timestamp` (ms). Implementation: `scripts/readiness_export.py`. See `docs/research/readiness_endpoint.md`.

Example (Python request skeleton)
```
GET https://api-mifit-us2.zepp.com/users/<HUAMI_USER_ID>/events
  headers: apptoken, appPlatform=web, appname=com.xiaomi.hm.health
  params: {
    eventType: all_day_stress | blood_oxygen | PaiHealthInfo | readiness,
    from: <epoch_ms>,
    to: <epoch_ms>,
    timeZone: America/New_York,
    limit: 1000
  }
```

Reference
- Generic fetcher: `scripts/events_dump.py`
- Normalizer: `scripts/readiness_export.py` (readiness CSV/JSON)
- Sample outputs: `data/processed/*_events_<type>_*.json`


## 5) Workouts — `/v1/sport/run/history.json` and `/v1/sport/run/detail.json` (Huami)

Base
- Host: `https://api-mifit.huami.com`
- Paths:
  - History: `/v1/sport/run/history.json`
  - Detail: `/v1/sport/run/detail.json`

Auth headers
- `apptoken`, `appPlatform: web`, `appname: com.xiaomi.hm.health`

Usage
- History: optional `trackid` query for pagination; response `data.next` provides the next `trackid` until `-1`.
- Detail: requires `trackid` and `source` from a history item (e.g., `run.mifit.huami.com`).

Notes
- These endpoints are validated via code and captures from the community `zepp-fit-extractor`; we mirror the same header pattern. See `docs/research/zepp_fit_extractor.md`.


## 6) Practical Implementation Notes

Time handling
- Always interpret timestamps (ms) using the same `timeZone` passed in the request for events. Align “day” labels to local time.

Rate limiting and retries
- Space requests by ~500–1000 ms. Backoff and retry on 429/5xx; our `scripts/batch_probe.py` shows an approach.

Decoding patterns
- `band_data.json`: Base64 → JSON (`summary` field)
- Stress events: JSON string in `data` → parse into point array
- Readiness: normalize numerics; prefer `watch_score`; keep `rawData` for future

Environment and scripts
- Set `HUAMI_TOKEN` and `HUAMI_USER_ID` in `.env`. Examples and wrappers:
  - Verify token: `scripts/verify_token.py`
  - Curl helper: `scripts/auth_curl.sh --as apptoken <URL-or-path>`
  - Band data: `python3 scripts/band_data_dump.py --from-date YYYY-MM-DD --to-date YYYY-MM-DD --query-type detail`
  - Events: `python3 scripts/events_dump.py --base https://api-mifit-us2.zepp.com --event-type readiness --days 10`
  - Readiness export: `python3 scripts/readiness_export.py --days 7`


## 7) What’s intentionally excluded here

This summary omits endpoints that returned 404/400 or consistently empty items for our account/window (e.g., dedicated HRV, temperature, and certain sleep metrics). See `docs/endpoints.md` and dated research logs for those probes; they are not required to reproduce the working flows above.


## 8) Quick Reimplementation Checklist

1) Acquire `HUAMI_TOKEN` and `HUAMI_USER_ID` (see repo README). Validate with `scripts/verify_token.py`.
2) Call `band_data.json` for your date window to get daily steps/sleep (and RHR if present):
   - host: `api-mifit.huami.com`; headers: `apptoken` (+ `appPlatform`, `appname`); params: `query_type`, `device_type`, `userid`, `from_date`, `to_date`.
   - Base64‑decode `summary` and parse `stp`/`slp`.
3) Call events for health series/aggregates from `api-mifit-us2.zepp.com`:
   - `all_day_stress` → per‑minute stress points
   - `blood_oxygen` → `click` measurements, `osa_event` detections, `odi` nightly summaries
   - `PaiHealthInfo` → PAI daily totals, RHR, zone mins/thresholds
   - `readiness` → nightly `watch_score` aggregates (HRV/RHR and component scores)
4) For workouts, paginate `/v1/sport/run/history.json` and fetch `/v1/sport/run/detail.json` using `trackid`/`source`.
