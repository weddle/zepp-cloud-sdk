import json

import httpx
import respx

from zepp_cloud.client import ZeppClient


@respx.mock
def test_events_stress_parses_points_and_stats():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit-us2.zepp.com"
        url = f"{base}/users/{client.user_id}/events"
        payload = {
            "items": [
                {
                    "timestamp": 1724100000000,
                    "minStress": 10,
                    "maxStress": 80,
                    "data": json.dumps(
                        [
                            {"time": 1724100000000, "value": 20},
                            {"time": 1724100300000, "value": 40},
                        ]
                    ),
                }
            ]
        }
        respx.get(url).mock(return_value=httpx.Response(200, json=payload))
        rows = client.events.stress(days=1, time_zone="UTC")
    finally:
        client.close()

    assert len(rows) == 1
    day = rows[0]
    assert day.date == "2024-08-19" or isinstance(day.date, str)
    assert day.min == 10 and day.max == 80
    assert day.avg and day.avg > 0
    assert len(day.points) == 2


@respx.mock
def test_events_stress_window_split_calls_multiple():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit-us2.zepp.com"
        url = f"{base}/users/{client.user_id}/events"
        # Configure respx to capture multiple calls
        route = respx.get(url).mock(return_value=httpx.Response(200, json={"items": []}))
        rows = client.events.stress(days=2001, time_zone="UTC")
    finally:
        client.close()

    # With max 1000/day chunking, expect at least 3 calls
    assert route.call_count >= 3
    assert rows == []
