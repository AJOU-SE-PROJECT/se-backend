
class PostChapterCreate:
    userId: int
    content: str
    bookId: int
    chapter: int

class PostChapterResponse:
    idList: list[int]

class ModifySentenceRequest: 
    sentenceId: int
    content: str

class ModifySenteceResponse:
    result: str

class AddSentenceRequest:
    beforeId: int
    afterId: int
    content: str

class DeletetSenteceRequest:
    sentenceId: int