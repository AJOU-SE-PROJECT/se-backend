from abc import ABC, abstractmethod

from sqlalchemy.orm import Session

from db.model import Sentence, User


class PostRepository(ABC):
    """Repository interface describing author persistence behavior."""

    @abstractmethod
    def create(self, post_data: dict) -> User:
        """Persist a new author and return the stored entity."""


class PostgresqlPostRepository(PostRepository):
    """SQLAlchemy-backed implementation of the AuthorRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, post_data: dict) -> Sentence:
        sentence = Sentence(**post_data)
        self.session.add(sentence)
        self.session.commit()
        self.session.refresh(sentence)
        return sentence
    
    def update(self, sentence: Sentence) -> Sentence:
        self.session.add(sentence)
        self.session.commit()
        self.session.refresh(sentence)
        return sentence
