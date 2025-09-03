import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


@respx.mock
def test_cli_events_readiness_pretty(capsys):
    base = "https://api-mifit-us2.zepp.com"
    url = f"{base}/users/U/events"
    items = [
        {"timestamp": 1, "subtype": "watch_score", "sleepHRV": 30, "sleepRHR": 55},
        {"timestamp": 2, "subtype": "watch_score", "sleepHRV": 28, "sleepRHR": 50},
    ]
    respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))

    try:
        cli_main(
            [
                "events",
                "readiness",
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
    arr = json.loads(out)
    assert isinstance(arr, list) and len(arr) == 2
