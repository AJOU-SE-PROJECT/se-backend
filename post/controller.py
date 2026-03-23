from fastapi import APIRouter, Depends, status
from db.database import get_db
from db.model import Sentence, User
from sqlalchemy.orm import Session

from post.repository import PostRepository, PostgresqlPostRepository
from post.schemas import PostChapterCreate, PostChapterResponse
from post.service import PostService

router = APIRouter(prefix="/book", tags=["books"])

class PostController:
    def __init__(self, service: PostService):
        self.service = service

    def post(self, dto: PostChapterCreate):
        created: list[Sentence] = self.service.post_sentences(dto)
        result = list(map(lambda i : PostChapterResponse(i.id), created))
        return result

def get_post_repository(db: Session = Depends(get_db)) -> PostRepository:
    return PostgresqlPostRepository(db)

def get_post_service(
        repository: PostRepository = Depends(get_post_repository)
) -> PostService:
    return PostService(repository)

def get_post_controller(
        service: PostService = Depends(get_post_service)
) -> PostController:
    return PostController(service)

@router.post("/chapter", response_model=PostChapterResponse, status_code=status.HTTP_201_CREATED)
def post_chapter(
    dto: PostChapterCreate, controller: PostController = Depends(get_post_controller)
) -> list[PostChapterResponse]:
    return controller.post(dto)
