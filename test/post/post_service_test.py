import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from db.database import Base
from db.model import Sentence
from post.repository import PostgresqlPostRepository
from post.schemas import PostChapterCreate
from post.service import PostService


@pytest.fixture()
def session():
    """Create an isolated in-memory DB session for each test."""
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    SessionLocal = sessionmaker(bind=engine)
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
        Base.metadata.drop_all(bind=engine)


@pytest.fixture()
def repository(session):
    return PostgresqlPostRepository(session)


@pytest.fixture()
def service(repository):
    return PostService(repository)


def make_post_chapter_dto(content: str) -> PostChapterCreate:
    dto = PostChapterCreate()
    dto.userId = 1
    dto.content = content
    dto.bookId = 42
    dto.chapter = 3
    return dto


def test_post_sentences_persists_each_sentence(service, session):
    dto = make_post_chapter_dto("첫 문장. 두 번째 문장? 마지막 문장.")

    created = service.post_sentences(dto)

    assert len(created) == 3
    assert [s.content for s in created] == [
        "첫 문장",
        "두 번째 문장",
        "마지막 문장",
    ]
    assert all(sentence.book_id == dto.bookId for sentence in created)
    assert all(sentence.chapter == dto.chapter for sentence in created)

    stored = session.query(Sentence).order_by(Sentence.id).all()
    assert len(stored) == 3


def test_post_sentences_links_after_ids(service, session):
    dto = make_post_chapter_dto("A.  B?C.")

    service.post_sentences(dto)

    stored = session.query(Sentence).order_by(Sentence.id).all()

    assert stored[0].after_id == stored[1].id
    assert stored[1].after_id == stored[2].id
    assert stored[2].after_id is None
