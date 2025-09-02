import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


@respx.mock
def test_cli_events_stress_pretty(capsys):
    base = "https://api-mifit-us2.zepp.com"
    url = f"{base}/users/U/events"
    payload = {
        "items": [
            {
                "timestamp": 1724100000000,
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

    try:
        cli_main([
            "events","stress","--days","1","--tz","UTC","--token","T","--user","U","--pretty"
        ])
    except SystemExit as e:
        assert e.code == 0

    out = capsys.readouterr().out
    data = json.loads(out)
    assert isinstance(data, list) and len(data) == 1
    assert isinstance(data[0].get("date"), str)
    assert len(data[0].get("points", [])) == 2

