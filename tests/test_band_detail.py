import httpx
import respx

from zepp_cloud.client import ZeppClient


@respx.mock
def test_band_detail_parses_hr_pair_list():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        url = "https://api-mifit.huami.com/v1/data/band_data.json"
        payload = {
            "data": [
                {
                    "date": "2025-08-20",
                    "detail": {"hr": [[1724100000000, 60], [1724100300000, 62]]},
                }
            ]
        }
        respx.get(url).mock(return_value=httpx.Response(200, json=payload))
        rows = client.band.get_detail("2025-08-20", "2025-08-20")
    finally:
        client.close()
    assert len(rows) == 1
    d = rows[0]
    assert d.date == "2025-08-20"
    assert d.hr_points[:2] == [(1724100000000, 60), (1724100300000, 62)]


@respx.mock
def test_band_detail_parses_hr_dict_list_and_handles_missing():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        url = "https://api-mifit.huami.com/v1/data/band_data.json"
        payload = {
            "data": {
                "2025-08-21": {
                    "detail": {
                        "hr": [
                            {"time": 1, "value": 70},
                            {"ts": 2, "bpm": 72},
                            {"timestamp": 3, "hr": 74},
                            {"value": 75},  # ignored
                        ]
                    }
                },
                "2025-08-22": {"detail": {}},
            }
        }
        respx.get(url).mock(return_value=httpx.Response(200, json=payload))
        rows = client.band.get_detail("2025-08-21", "2025-08-22")
    finally:
        client.close()

    assert len(rows) == 2
    a, b = rows
    assert a.date == "2025-08-21"
    assert a.hr_points[:3] == [(1, 70), (2, 72), (3, 74)]
    assert b.date == "2025-08-22"
    assert b.hr_points == []
