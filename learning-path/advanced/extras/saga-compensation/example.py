"""Saga compensation flow."""


def reserve_inventory():
    return "reserved"


def charge_payment():
    raise RuntimeError("payment failed")


def release_inventory():
    return "released"


if __name__ == "__main__":
    try:
        reserve_inventory()
        charge_payment()
    except Exception as exc:  # noqa: BLE001
        print(f"failure: {exc}")
        print(release_inventory())
