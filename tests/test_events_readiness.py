import httpx
import respx

from zepp_cloud.client import ZeppClient


@respx.mock
def test_events_readiness_parses_watch_score():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit-us2.zepp.com"
        url = f"{base}/users/{client.user_id}/events"
        items = [
            {
                "timestamp": 1724100000000,
                "subtype": "watch_score",
                "sleepHRV": 28,
                "sleepRHR": 50,
                "hrvScore": 70,
                "rhrScore": 80,
                "skinTempScore": 60,
                "rdnsScore": 65,
                "phyScore": 75,
                "mentScore": 72,
                "ahiScore": 90,
                "hrvBaseline": 30,
                "rhrBaseline": 48,
                "skinTempBaseLine": 0.2,
                "mentBaseLine": 68,
                "phyBaseline": 70,
                "ahiBaseline": 85,
                "afibBaseLine": 0,
                "status": "ok",
                "algVer": "1.2",
                "algSubVer": "a",
                "deviceId": "D1",
            }
        ]
        respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))
        rows = client.events.readiness(days=1, time_zone="UTC")
    finally:
        client.close()

    assert len(rows) == 1
    r = rows[0]
    assert r.sleep_hrv == 28 and r.sleep_rhr == 50
    assert r.hrv_score == 70 and r.rhr_score == 80 and r.skin_temp_score == 60
    assert r.status == "ok" and r.alg_ver == "1.2"
