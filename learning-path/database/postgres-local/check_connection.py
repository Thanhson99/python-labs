"""Check PostgreSQL connectivity with psycopg."""

import os

import psycopg


def main() -> None:
    dsn = os.getenv("DATABASE_URL", "postgresql://learning:learning@127.0.0.1:5432/learning")
    with psycopg.connect(dsn) as conn:
        with conn.cursor() as cur:
            cur.execute("SELECT version()")
            print(cur.fetchone()[0])


if __name__ == "__main__":
    main()
