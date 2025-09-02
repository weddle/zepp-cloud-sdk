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

