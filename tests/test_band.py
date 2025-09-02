import base64
import json

import httpx
import respx

from zepp_cloud.client import ZeppClient


def _b64(obj) -> str:
    raw = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


@respx.mock
def test_band_summary_parses_list_items():
    client = ZeppClient(apptoken="T", user_id="U", timezone="America/New_York")
    try:
        url = "https://api-mifit.huami.com/v1/data/band_data.json"
        payload = {
            "data": [
                {
                    "date": "2025-08-20",
                    "summary": _b64(
                        {
                            "stp": {"ttl": 1234, "dis": 890, "cal": 45},
                            "slp": {
                                "st": 1724100000000,
                                "ed": 1724130000000,
                                "dp": 50,
                                "lt": 300,
                                "rhr": 56,
                            },
                        }
                    ),
                },
                {
                    "date": "2025-08-21",
                    "sum": _b64({
                        "stp": {"ttl": 4321, "dis": 98, "cal": 54},
                        "slp": {"st": 1724186400000, "ed": 1724212800000, "dp": 40, "lt": 200},
                    }),
                },
            ]
        }
        respx.get(url).mock(return_value=httpx.Response(200, json=payload))
        rows = client.band.get_summary("2025-08-20", "2025-08-21")
    finally:
        client.close()

    assert len(rows) == 2
    a, b = rows
    assert a.date == "2025-08-20"
    assert a.steps_total == 1234
    assert a.distance_m == 890
    assert a.calories_kcal == 45
    assert a.resting_hr == 56
    assert b.date == "2025-08-21"
    assert b.resting_hr is None


@respx.mock
def test_band_summary_parses_dict_items_with_date_keys():
    client = ZeppClient(apptoken="T", user_id="U", timezone="America/New_York")
    try:
        url = "https://api-mifit.huami.com/v1/data/band_data.json"
        payload = {
            "data": {
                "2025-08-20": {
                    "summary": _b64({
                        "stp": {"ttl": 100, "dis": 200, "cal": 300},
                        "slp": {"st": 1, "ed": 2, "dp": 3, "lt": 4, "rhr": 60},
                    })
                }
            }
        }
        respx.get(url).mock(return_value=httpx.Response(200, json=payload))
        rows = client.band.get_summary("2025-08-20", "2025-08-20")
    finally:
        client.close()

    assert len(rows) == 1
    r = rows[0]
    assert r.date == "2025-08-20"
    assert r.steps_total == 100
    assert r.distance_m == 200
    assert r.calories_kcal == 300
