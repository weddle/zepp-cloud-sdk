import base64
import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


def _b64(obj) -> str:
    raw = json.dumps(obj, separators=(",", ":")).encode("utf-8")
    return base64.b64encode(raw).decode("ascii")


@respx.mock
def test_cli_band_summary_basic(capsys):
    url = "https://api-mifit.huami.com/v1/data/band_data.json"
    payload = {
        "data": [
            {
                "date": "2025-08-20",
                "summary": _b64(
                    {"stp": {"ttl": 100, "dis": 200, "cal": 10}, "slp": {"dp": 30, "lt": 200}}
                ),
            }
        ]
    }
    respx.get(url).mock(return_value=httpx.Response(200, json=payload))

    try:
        cli_main(
            [
                "band",
                "summary",
                "--from",
                "2025-08-20",
                "--to",
                "2025-08-21",
                "--token",
                "T",
                "--user",
                "U",
                "--tz",
                "America/New_York",
            ]
        )
    except SystemExit as e:
        assert e.code == 0

    out = capsys.readouterr().out.strip().splitlines()
    assert len(out) == 1
    row = json.loads(out[0])
    assert row["date"] == "2025-08-20"
    assert row["steps_total"] == 100
    assert row["distance_m"] == 200
