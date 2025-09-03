import json

import httpx
import respx

from zepp_cloud.cli import main as cli_main


@respx.mock
def test_cli_workouts_history_pretty(capsys):
    url = "https://api-mifit.huami.com/v1/sport/run/history.json"
    respx.get(url).mock(return_value=httpx.Response(200, json={
        "data": {"items": [
            {"trackid": "A", "source": "s"},
            {"trackid": "B", "source": "s"},
        ], "next": -1}
    }))
    try:
        cli_main(["workouts", "history", "--token", "T", "--user", "U", "--pretty"])
    except SystemExit as e:
        assert e.code == 0
    out = capsys.readouterr().out
    arr = json.loads(out)
    assert isinstance(arr, list) and len(arr) == 2


@respx.mock
def test_cli_workouts_detail_pretty(capsys):
    url = "https://api-mifit.huami.com/v1/sport/run/detail.json"
    respx.get(url).mock(return_value=httpx.Response(200, json={
        "summary": {"trackid": "Z", "source": "s"},
        "series": {"hr": [60, 61]},
    }))
    try:
        cli_main([
            "workouts",
            "detail",
            "--token",
            "T",
            "--user",
            "U",
            "--trackid",
            "Z",
            "--source",
            "s",
            "--pretty",
        ])
    except SystemExit as e:
        assert e.code == 0
    out = capsys.readouterr().out
    obj = json.loads(out)
    assert obj["trackid"] == "Z"
