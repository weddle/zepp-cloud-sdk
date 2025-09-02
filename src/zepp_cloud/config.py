from __future__ import annotations

from dataclasses import dataclass, field


@dataclass(frozen=True)
class ZeppConfig:
    """Configuration values for the Zepp Cloud SDK.

    These values provide sensible defaults and can be overridden per-client.
    """

    # Default base URLs (can vary by region; callers may override)
    band_base: str = "https://api-mifit.huami.com"
    events_base: str = "https://api-mifit-us2.zepp.com"

    # Pacing: minimum delay between requests to the same host
    rate_ms: int = 700

    # Retry/backoff
    max_retries: int = 3
    backoff_base_seconds: float = 0.5

    # Timeouts (seconds)
    timeout_connect: float = 5.0
    timeout_read: float = 30.0
    timeout_total: float = 60.0

    # Headers
    app_platform: str = "web"
    app_name: str = "com.xiaomi.hm.health"
    user_agent: str = field(
        default_factory=lambda: "zepp-cloud-sdk/0.x (+https://github.com/your-org/zepp-cloud-sdk)"
    )

