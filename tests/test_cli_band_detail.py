import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


@respx.mock
def test_cli_band_detail_pretty(capsys):
    url = "https://api-mifit.huami.com/v1/data/band_data.json"
    payload = {"data": [{"date": "2025-08-20", "detail": {"hr": [[1, 60], [2, 61]]}}]}
    respx.get(url).mock(return_value=httpx.Response(200, json=payload))

    try:
        cli_main(
            [
                "band",
                "detail",
                "--from",
                "2025-08-20",
                "--to",
                "2025-08-20",
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
    assert isinstance(data, list) and len(data) == 1
    assert data[0]["date"] == "2025-08-20"
    assert data[0]["hr_points"][0] == [1, 60] or data[0]["hr_points"][0] == (1, 60)

