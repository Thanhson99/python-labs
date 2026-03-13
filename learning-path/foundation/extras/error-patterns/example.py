"""Error handling patterns."""


class ExternalServiceError(Exception):
    pass


def call_external(flag: bool) -> str:
    if not flag:
        raise ExternalServiceError("provider unavailable")
    return "ok"


if __name__ == "__main__":
    try:
        print(call_external(False))
    except ExternalServiceError as exc:
        print(f"handled: {exc}")
