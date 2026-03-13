"""Connection pool sample with SQLAlchemy engine."""

from sqlalchemy import create_engine, text


def main() -> None:
    engine = create_engine(
        "postgresql+psycopg://learning:learning@127.0.0.1:5432/learning",
        pool_size=5,
        max_overflow=10,
        pool_pre_ping=True,
    )
    with engine.connect() as conn:
        print(conn.execute(text("SELECT 1")).scalar_one())


if __name__ == "__main__":
    main()
