import httpx
import respx

from zepp_cloud.client import ZeppClient


@respx.mock
def test_workouts_history_paginates():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit.huami.com"
        url = f"{base}/v1/sport/run/history.json"
        # First page
        respx.get(url).mock(side_effect=[
            httpx.Response(200, json={
                "data": {"items": [
                    {"trackid": "A", "source": "s", "starttime": 1, "endtime": 2},
                ], "next": 123}
            }),
            httpx.Response(200, json={
                "data": {"items": [
                    {"trackid": "B", "source": "s", "starttime": 3, "endtime": 4},
                ], "next": -1}
            })
        ])
        rows = list(client.workouts.iter_history())
    finally:
        client.close()
    assert [r.trackid for r in rows] == ["A", "B"]


@respx.mock
def test_workouts_detail_maps_fields():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit.huami.com"
        url = f"{base}/v1/sport/run/detail.json"
        respx.get(url).mock(return_value=httpx.Response(200, json={
            "summary": {"trackid": "Z", "source": "s", "distance": 1000, "calories": 50},
            "series": {"hr": [70, 72]},
            "track": [[0.0, 0.0], [0.1, 0.1]],
        }))
        d = client.workouts.detail("Z", "s")
    finally:
        client.close()
    assert d.summary.distance_m == 1000 and d.summary.calories_kcal == 50
    assert isinstance(d.series, dict)
