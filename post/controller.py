from unittest import result
from fastapi import APIRouter, Depends, status
from db.database import get_db
from db.model import Sentence, User
from sqlalchemy.orm import Session

from post.repository import PostRepository, PostgresqlPostRepository
from post.schemas import ModifySenteceResponse, ModifySentenceRequest, PostChapterCreate, PostChapterResponse
from post.service import PostService

router = APIRouter(prefix="/book", tags=["books"])

class PostController:
    def __init__(self, service: PostService):
        self.service = service

    def post(self, dto: PostChapterCreate):
        created: list[Sentence] = self.service.post_sentences(dto)
        result = list(map(lambda i : PostChapterResponse(i.id), created))
        return result
    
    def modify(self, dto: ModifySentenceRequest):
        return self.service.modify_sentence(dto)


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

@router.post("/chapter", response_model=list[PostChapterResponse], status_code=status.HTTP_201_CREATED)
def post_chapter(
    dto: PostChapterCreate, controller: PostController = Depends(get_post_controller)
) -> list[PostChapterResponse]:
    return controller.post(dto)

@router.patch("/chapter", response_class=ModifySenteceResponse, status_code=status.HTTP_200_OK)
def modify_sentence(
    dto: ModifySentenceRequest, controller: PostController = Depends(get_post_controller)
) -> ModifySenteceResponse:
    controller.modify(dto)
    return ModifySenteceResponse(result="성공적으로 수정되었습니다.")
