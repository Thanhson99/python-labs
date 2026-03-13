"""Consumer contract schema check sample."""


REQUIRED_KEYS = {"id", "email", "status"}


def validate_contract(payload: dict) -> bool:
    return REQUIRED_KEYS.issubset(set(payload))


if __name__ == "__main__":
    print(validate_contract({"id": "u1", "email": "a@b.com", "status": "active"}))
