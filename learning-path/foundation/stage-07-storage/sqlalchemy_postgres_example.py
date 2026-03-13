"""Stage 07: SQLAlchemy + PostgreSQL structure sample."""

from sqlalchemy import String, create_engine
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column, sessionmaker


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True)
    email: Mapped[str] = mapped_column(String(200), unique=True)


def run() -> None:
    # Example URL only. Replace credentials for local environment.
    engine = create_engine("postgresql+psycopg://user:pass@127.0.0.1:5432/app")
    SessionLocal = sessionmaker(bind=engine)

    Base.metadata.create_all(engine)

    with SessionLocal() as session:
        session.add(User(email="owner@example.com"))
        session.commit()


if __name__ == "__main__":
    run()
