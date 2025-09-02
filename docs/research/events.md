# `/users/<id>/events` — Health Events

This endpoint returns health event series for various types, including stress.

## Base and Path
- Host: `https://api-mifit-us2.zepp.com` (regional variants exist; keep configurable)
- Path: `/users/<HUAMI_USER_ID>/events`

## Required Headers
- `apptoken: <HUAMI_TOKEN>`
- `appPlatform: web`
- `appname: com.xiaomi.hm.health`

## Query Parameters
- `eventType`: for stress use `all_day_stress`
- `from`: window start, epoch milliseconds
- `to`: window end, epoch milliseconds
- `timeZone`: IANA zone; use the same value for grouping on the client side
- `limit`: typically `1000` — split windows when needed to avoid truncation

## Response Shape
- HTTP 200 JSON: `{ items: [ ... ] }`
- Each item has `data` as a JSON string (e.g., stress points): `[{ "time": <ms>, "value": <int> }, ...]`
- Additional fields may include `timestamp`, `minStress`, `maxStress`, etc.

## Decoding and Grouping
- Parse `data` (JSON string) into points and group by local day using the same `timeZone` from the request.
- Compute daily min/max/avg on the grouped points.
- Sampling cadence is typically ~5 minutes but can vary by device/firmware.

## Limits and Windowing
- Respect `limit` by splitting long ranges into day-sized chunks when necessary.
- Combine results from multiple windows to cover the full requested range.

## Blood Oxygen (SpO₂) Subtypes
- eventType: `blood_oxygen`
- Subtypes and field mapping:
  - click (spot): `extra.spo2`; optional `history` may exist and is preserved in `raw_item`.
  - osa_event: `extra.spo2_decrease` (magnitude).
  - odi (nightly summary): `odi`, `odiNum`, `valid`, `score`, `dispCode`; grouped by local day using `timestamp`.
- Device variance: Some accounts emit empty arrays for `spo2`/`hr`; rely on `extra` fields where available.

## PAI Mapping
- eventType: `PaiHealthInfo`
- Fields commonly observed (naming may vary by device/firmware):
  - `dailyPai` (daily PAI)
  - `totalPai` (running total)
  - `restHr`, `maxHr`
  - HR zone thresholds and minutes, e.g., `low`/`medium`/`high` and `minutesLow`/`minutesMed`/`minutesHigh`. Some payloads use alternative keys (e.g., `lowBpm`, `medBpm`, `highBpm`, or `lowMinutes`).
- Group rows by local day using `timestamp` and the same `timeZone` you pass in the request.
- Parser should be lenient and retain unused keys in `raw_item` for provenance.

## Readiness Mapping
- eventType: `readiness`
- Prefer `watch_score` items for analytics; fields commonly observed:
  - Core: `sleepHRV`, `sleepRHR`
  - Component scores: `hrvScore`, `rhrScore`, `skinTempScore`, `rdnsScore`, `phyScore`, `mentScore`, `ahiScore`
  - Baselines: `hrvBaseline`, `rhrBaseline`, `skinTempBaseLine`, `mentBaseLine`, `phyBaseline`, `ahiBaseline`, `afibBaseLine`
  - Other: `status`, `algVer`, `algSubVer`, `deviceId`
- `watch_score_data` companion items may include a `rawData` payload; the SDK preserves it in raw for future decoding.
- Derive local `date` via `timestamp` and the same `timeZone` used in the request.
