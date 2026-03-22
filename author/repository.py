from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from db.model import Author


class AuthorRepository(ABC):
    """Repository interface describing author persistence behavior."""

    @abstractmethod
    def create(self, author_data: dict) -> Author:
        """Persist a new author and return the stored entity."""


class PostgresqlAuthorRepository(AuthorRepository):
    """SQLAlchemy-backed implementation of the AuthorRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, author_data: dict) -> Author:
        author = Author(**author_data)
        self.session.add(author)
        self.session.commit()
        self.session.refresh(author)
        return author
