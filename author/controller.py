from author.schemas import AuthorCreate, AuthorResponse
from author.service import AuthorService


class AuthorController:
    """Controller handling author related endpoints."""

    def __init__(self, service: AuthorService):
        self.service = service

    def register_author(self, author: AuthorCreate) -> AuthorResponse:
        """Register a new author via the service."""
        created = self.service.register_author(author.model_dump())
        return AuthorResponse.model_validate(created)
