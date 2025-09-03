import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


@respx.mock
def test_cli_events_blood_oxygen_pretty_grouped(capsys):
    base = "https://api-mifit-us2.zepp.com"
    url = f"{base}/users/U/events"
    items = [
        {"timestamp": 1, "subtype": "click", "extra": {"spo2": 95}},
        {"timestamp": 2, "subtype": "osa_event", "extra": {"spo2_decrease": 6}},
        {"timestamp": 3, "odi": 1.2, "odiNum": 10, "valid": True, "score": 60},
    ]
    respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))

    try:
        cli_main(
            [
                "events",
                "blood-oxygen",
                "--days",
                "1",
                "--tz",
                "UTC",
                "--token",
                "T",
                "--user",
                "U",
                "--pretty",
            ]
        )
    except SystemExit as e:
        assert e.code == 0

    out = capsys.readouterr().out
    data = json.loads(out)
    assert set(data.keys()) == {"click", "osa_event", "odi"}
    assert len(data["click"]) == 1


@respx.mock
def test_cli_events_blood_oxygen_pretty_subtype(capsys):
    base = "https://api-mifit-us2.zepp.com"
    url = f"{base}/users/U/events"
    items = [
        {"timestamp": 1, "subtype": "click", "extra": {"spo2": 95}},
        {"timestamp": 3, "odi": 1.2, "odiNum": 10, "valid": True, "score": 60},
    ]
    respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))

    try:
        cli_main(
            [
                "events",
                "blood-oxygen",
                "--days",
                "1",
                "--tz",
                "UTC",
                "--token",
                "T",
                "--user",
                "U",
                "--pretty",
                "--subtype",
                "click",
            ]
        )
    except SystemExit as e:
        assert e.code == 0

    out = capsys.readouterr().out
    arr = json.loads(out)
    assert isinstance(arr, list) and len(arr) == 1
