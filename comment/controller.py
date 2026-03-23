from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session

from comment.repository import CommentRepository, PostgresqlCommentRepository
from comment.schemas import CommentCreate, CommentResponse
from comment.service import CommentService
from db.database import SessionLocal, get_db


router = APIRouter(prefix="/sentences", tags=["comments"])


class CommentController:
    """Controller handling comment related endpoints."""

    def __init__(self, service: CommentService):
        self.service = service

    def create_comment(self, sentence_id: int, comment: CommentCreate) -> CommentResponse:
        """Create a new comment for a given sentence."""
        comment_data = {
            "content": comment.content,
            "user_id": 1,  # TODO: replace with authenticated user
            "sentence_id": sentence_id,
        }

        created = self.service.create_comment(comment_data)
        return CommentResponse.model_validate(created)

    def get_comments_by_sentence(self, sentence_id: int) -> list[CommentResponse]:
        """Get comments for a sentence ordered by most recent first."""
        comments = self.service.get_comments_by_sentence(sentence_id)
        return [CommentResponse.model_validate(c) for c in comments]


def get_comment_repository(db: Session = Depends(get_db)) -> CommentRepository:
    """Provide a repository wired with the active DB session."""
    return PostgresqlCommentRepository(db)


def get_comment_service(
    repository: CommentRepository = Depends(get_comment_repository),
) -> CommentService:
    """Provide a CommentService using the repository abstraction."""
    return CommentService(repository)


def get_comment_controller(
    service: CommentService = Depends(get_comment_service),
) -> CommentController:
    """Provide a CommentController wired with dependencies."""
    return CommentController(service)


@router.post("/{sentence_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
def create_comment(
    sentence_id: int,
    comment: CommentCreate,
    controller: CommentController = Depends(get_comment_controller),
):
    """REST endpoint to create a comment for a sentence."""
    return controller.create_comment(sentence_id, comment)


@router.get("/{sentence_id}/comments", response_model=list[CommentResponse], status_code=status.HTTP_200_OK)
def get_comments_by_sentence(
    sentence_id: int,
    controller: CommentController = Depends(get_comment_controller),
):
    """REST endpoint to fetch comments for a sentence."""
    return controller.get_comments_by_sentence(sentence_id)
