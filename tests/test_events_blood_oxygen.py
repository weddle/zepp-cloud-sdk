import httpx
import respx

from zepp_cloud.client import ZeppClient


@respx.mock
def test_events_blood_oxygen_parses_subtypes():
    client = ZeppClient(apptoken="T", user_id="U", timezone="UTC")
    try:
        base = "https://api-mifit-us2.zepp.com"
        url = f"{base}/users/{client.user_id}/events"
        items = [
            {"timestamp": 1724100000000, "subtype": "click", "extra": {"spo2": 98}},
            {"timestamp": 1724100300000, "subtype": "osa_event", "extra": {"spo2_decrease": 7}},
            {
                "timestamp": 1724100600000,
                "odi": 2.5,
                "odiNum": 12,
                "valid": True,
                "score": 75,
                "dispCode": "OK",
            },
        ]
        respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))
        data = client.events.blood_oxygen(days=1, time_zone="UTC")
    finally:
        client.close()

    assert set(data.keys()) == {"click", "osa_event", "odi"}
    assert len(data["click"]) == 1
    assert len(data["osa_event"]) == 1
    assert len(data["odi"]) == 1
    assert data["click"][0].spo2 == 98
    assert data["osa_event"][0].spo2_decrease == 7
    assert data["odi"][0].odi == 2.5
