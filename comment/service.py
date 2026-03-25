from typing import List

from db.model import Comment
from comment.repository import CommentRepository


class CommentService:
    """Service layer for comment related operations."""

    def __init__(self, repository: CommentRepository):
        self.repository = repository

    def create_comment(self, comment_data: dict) -> Comment:
        """Persist a new comment into DB."""
        return self.repository.create(comment_data)

    def get_comments_by_sentence(self, sentence_id: int) -> List[Comment]:
        """Fetch comments for a sentence in descending order (newest first)."""
        return self.repository.get_by_sentence(sentence_id)
