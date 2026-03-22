from fastapi import Depends, FastAPI, status
from sqlalchemy.orm import Session

from author.controller import AuthorController
from author.repository import AuthorRepository, SQLAlchemyAuthorRepository
from author.schemas import AuthorCreate, AuthorResponse
from author.service import AuthorService
from db.database import SessionLocal

app = FastAPI(title="Author Service")


def get_db() -> Session:
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_author_repository(db: Session = Depends(get_db)) -> AuthorRepository:
    """Provide a repository wired with the active DB session."""
    return SQLAlchemyAuthorRepository(db)


def get_author_service(
    repository: AuthorRepository = Depends(get_author_repository),
) -> AuthorService:
    """Provide an AuthorService using the repository abstraction."""
    return AuthorService(repository)


def get_author_controller(
    service: AuthorService = Depends(get_author_service),
) -> AuthorController:
    """Provide an AuthorController wired with dependencies."""
    return AuthorController(service)


@app.post("/authors", response_model=AuthorResponse, status_code=status.HTTP_201_CREATED)
def register_author(
    author: AuthorCreate, controller: AuthorController = Depends(get_author_controller)
):
    """REST endpoint for author registration via the controller."""
    return controller.register_author(author)
