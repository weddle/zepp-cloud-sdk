import httpx
import respx

from zepp_cloud.config import ZeppConfig
from zepp_cloud.transport.http import HttpTransport


def make_transport(rate_ms=0):
    cfg = ZeppConfig(rate_ms=rate_ms)
    timeout = httpx.Timeout(
        timeout=cfg.timeout_total,
        connect=cfg.timeout_connect,
        read=cfg.timeout_read,
    )
    return HttpTransport(
        default_headers={"apptoken": "t", "appPlatform": cfg.app_platform, "appname": cfg.app_name},
        timeout=timeout,
        max_retries=cfg.max_retries,
        backoff_base_seconds=0.0,  # keep tests fast/deterministic
        rate_ms=rate_ms,
    )


@respx.mock
def test_retries_on_500_then_success():
    url = "https://api-mifit.huami.com/ping"
    route = respx.get(url).mock(side_effect=[httpx.Response(500), httpx.Response(200)])
    tr = make_transport()
    try:
        resp = tr.request("GET", url)
    finally:
        tr.close()
    assert resp.status_code == 200
    assert route.call_count == 2


@respx.mock
def test_retries_on_429_then_success():
    url = "https://api-mifit.huami.com/ping"
    route = respx.get(url).mock(side_effect=[httpx.Response(429), httpx.Response(200)])
    tr = make_transport()
    try:
        resp = tr.request("GET", url)
    finally:
        tr.close()
    assert resp.status_code == 200
    assert route.call_count == 2


@respx.mock
def test_host_pacing_sleeps_for_minimum_interval(monkeypatch):
    url = "https://api-mifit.huami.com/ping"
    respx.get(url).mock(return_value=httpx.Response(200))
    sleep_calls = []

    def fake_sleep(sec: float) -> None:
        sleep_calls.append(sec)

    tr = make_transport(rate_ms=100)  # 100ms
    tr._sleep = fake_sleep  # type: ignore[attr-defined]
    try:
        tr.request("GET", url)
        tr.request("GET", url)
    finally:
        tr.close()

    # Expect at least one sleep call for ~0.1s
    assert sleep_calls, "Expected pacing sleep to be called on second request"
    assert sleep_calls[0] >= 0.09
