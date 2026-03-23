from pydantic import BaseModel, ConfigDict, constr


class CommentCreate(BaseModel):
    content: constr(strip_whitespace=True, min_length=1, max_length=500)


class CommentResponse(BaseModel):
    id: int
    content: str
    user_id: int
    sentence_id: int

    model_config = ConfigDict(from_attributes=True)
