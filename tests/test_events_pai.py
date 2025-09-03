import httpx
import respx

from zepp_cloud.client import ZeppClient


@respx.mock
def test_events_pai_parses_fields():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit-us2.zepp.com"
        url = f"{base}/users/{client.user_id}/events"
        items = [
            {
                "timestamp": 1724100000000,
                "dailyPai": 8,
                "totalPai": 56,
                "restHr": 52,
                "maxHr": 182,
                "low": 90,
                "medium": 120,
                "high": 150,
                "minutesLow": 12,
                "minutesMed": 20,
                "minutesHigh": 3,
            }
        ]
        respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))
        rows = client.events.pai(days=1, time_zone="UTC")
    finally:
        client.close()

    assert len(rows) == 1
    r = rows[0]
    assert r.daily_pai == 8 and r.total_pai == 56
    assert r.rest_hr == 52 and r.max_hr == 182
    assert r.zone_low_bpm == 90 and r.zone_med_bpm == 120 and r.zone_high_bpm == 150
    assert r.minutes_low == 12 and r.minutes_med == 20 and r.minutes_high == 3
