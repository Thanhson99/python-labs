"""Transaction isolation level notes and command sample."""


def main() -> None:
    print("Use SERIALIZABLE for strict correctness in critical flows.")
    print("Use READ COMMITTED for most default transactional workloads.")


if __name__ == "__main__":
    main()
