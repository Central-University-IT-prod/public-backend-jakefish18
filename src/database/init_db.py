from sqlalchemy.orm import Session

from src.database.session import Base, engine  # noqa: F401


def init_db() -> None:
    Base.metadata.create_all(bind=engine)
