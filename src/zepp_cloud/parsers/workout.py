from __future__ import annotations

from typing import Any, Optional, Union

from ..models.workout import WorkoutDetail, WorkoutSummary


def _get(d: dict[str, Any], *keys: str) -> Any:
    for k in keys:
        if k in d:
            return d[k]
    return None


def _to_int(v: Any) -> int | None:
    try:
        return int(v) if v is not None else None
    except Exception:
        return None


def parse_history_item(item: dict[str, Any]) -> Optional[WorkoutSummary]:
    if not isinstance(item, dict):
        return None
    trackid = _get(item, "trackid", "trackId", "id")
    source = _get(item, "source", "src", "server")
    if trackid is None or source is None:
        return None
    start_ms = _to_int(_get(item, "starttime", "start_time", "start", "startMs"))
    end_ms = _to_int(_get(item, "endtime", "end_time", "end", "endMs"))
    duration_s = _to_int(_get(item, "duration", "dur"))
    distance_m = _to_int(_get(item, "distance", "dis", "dist"))
    calories_kcal = _to_int(_get(item, "calories", "kcal"))
    sport_mode = _get(item, "sportMode", "sport_mode", "mode")

    return WorkoutSummary(
        trackid=trackid,
        source=str(source),
        start_ms=start_ms,
        end_ms=end_ms,
        duration_s=duration_s,
        distance_m=distance_m,
        calories_kcal=calories_kcal,
        sport_mode=sport_mode,
        raw_item=item,
    )


def parse_detail(trackid: Union[str, int], source: str, body: dict[str, Any]) -> WorkoutDetail:
    # Many shapes exist; try common keys
    summary_item = body.get("summary") or body.get("data") or {}
    series = body.get("series") or body.get("detail") or None
    track = body.get("track") or None

    summary = parse_history_item(summary_item) or WorkoutSummary(
        trackid=trackid,
        source=source,
        raw_item=summary_item if isinstance(summary_item, dict) else {},
    )
    return WorkoutDetail(
        trackid=trackid,
        source=source,
        summary=summary,
        series=series if isinstance(series, dict) else None,
        track=track if isinstance(track, list) else None,
        raw_detail=body,
    )

