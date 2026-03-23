
class PostChapterCreate:
    userId: int
    content: str
    bookId: int
    chapter: int

class PostChapterResponse:
    idList: list[int]