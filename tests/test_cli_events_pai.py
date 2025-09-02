import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


@respx.mock
def test_cli_events_pai_pretty(capsys):
    base = "https://api-mifit-us2.zepp.com"
    url = f"{base}/users/U/events"
    items = [
        {"timestamp": 1, "dailyPai": 6, "totalPai": 60, "restHr": 50, "maxHr": 180},
        {"timestamp": 2, "dailyPai": 4, "totalPai": 64, "restHr": 52, "maxHr": 180},
    ]
    respx.get(url).mock(return_value=httpx.Response(200, json={"items": items}))

    try:
        cli_main([
            "events",
            "pai",
            "--days",
            "1",
            "--tz",
            "UTC",
            "--token",
            "T",
            "--user",
            "U",
            "--pretty",
        ])
    except SystemExit as e:
        assert e.code == 0

    out = capsys.readouterr().out
    arr = json.loads(out)
    assert isinstance(arr, list) and len(arr) == 2
