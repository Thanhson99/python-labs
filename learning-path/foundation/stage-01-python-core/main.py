"""Stage 01: Python core syntax and function patterns."""


def normalize_user(name: str, retries: int, active: bool) -> dict:
    """Return a normalized user payload."""
    name = name.strip().lower()
    status = "active" if active else "inactive"
    retry_window = "safe" if retries <= 3 else "high"
    return {
        "user_name": name,
        "max_retries": retries,
        "status": status,
        "retry_window": retry_window,
    }


def main() -> None:
    users = [
        ("ThanhSon99", 2, True),
        ("Guest", 5, False),
    ]

    for idx, user in enumerate(users, start=1):
        payload = normalize_user(*user)
        print(f"[{idx}] {payload}")


if __name__ == "__main__":
    main()
