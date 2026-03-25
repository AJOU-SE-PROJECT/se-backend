from abc import ABC, abstractmethod
from typing import List

from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, status

from db.model import Comment

class CommentRepository(ABC):
    """Repository interface describing comment persistence behavior."""

    @abstractmethod
    def create(self, comment_data: dict) -> Comment:
        """Persist a new comment and return the stored entity."""

    @abstractmethod
    def get_by_sentence(self, sentence_id: int) -> List[Comment]:
        """Return comments for a specific sentence, most recent first."""

class PostgresqlCommentRepository(CommentRepository):
    """SQLAlchemy-backed implementation of the CommentRepository."""

    def __init__(self, session: Session):
        self.session = session

    def create(self, comment_data: dict) -> Comment:
        comment = Comment(**comment_data)
        self.session.add(comment)
        try:
            self.session.commit()
            self.session.refresh(comment)
            return comment
        # ✨ 핵심 포인트: DB에서 외래키(문장)를 찾을 수 없을 때 404 에러로 우아하게 변환!
        except IntegrityError: 
            self.session.rollback()
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, 
                detail="해당 문장을 찾을 수 없습니다."
            )

    def get_by_sentence(self, sentence_id: int) -> List[Comment]:
        return (
            self.session.query(Comment)
            .filter(Comment.sentence_id == sentence_id)
            .order_by(Comment.id.desc())
            .all()
        )