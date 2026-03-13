"""Phase F: JWT flow structure sample."""

import base64
import json
from datetime import datetime, timedelta, timezone


def build_unsigned_jwt_like_payload(user_id: str) -> str:
    """Build a lab-only token-like string (not secure, for flow demo only)."""
    header = {"alg": "none", "typ": "JWT"}
    payload = {
        "sub": user_id,
        "exp": int((datetime.now(timezone.utc) + timedelta(minutes=15)).timestamp()),
    }

    h = base64.urlsafe_b64encode(json.dumps(header).encode()).decode().rstrip("=")
    p = base64.urlsafe_b64encode(json.dumps(payload).encode()).decode().rstrip("=")
    return f"{h}.{p}."


if __name__ == "__main__":
    print(build_unsigned_jwt_like_payload("user-1"))
