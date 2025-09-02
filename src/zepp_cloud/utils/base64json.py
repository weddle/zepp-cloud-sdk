from __future__ import annotations

import base64
import json
from typing import Any


def decode_base64_json(b64: str) -> dict[str, Any]:
    """Decode a Base64 string into a JSON object (dict).

    Raises ValueError if the decoded content is not a JSON object.
    """
    data = base64.b64decode(b64)
    try:
        as_text = data.decode("utf-8")
    except UnicodeDecodeError:
        # Some payloads are pure JSON without special encoding; assume utf-8
        as_text = data.decode("utf-8", errors="replace")
    obj = json.loads(as_text)
    if not isinstance(obj, dict):
        raise ValueError("decoded Base64 summary is not a JSON object")
    return obj
