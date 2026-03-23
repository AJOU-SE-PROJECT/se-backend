import re
from db.model import Sentence
from post.repository import PostRepository
from post.schemas import PostChapterCreate


class PostService:
    def __init__(self, repository: PostRepository):
        self.repository = repository
    
    def post_sentences(self, dto: PostChapterCreate) -> list[Sentence]:
        
        sentences = dto.content
        bookId = dto.bookId
        chapter = dto.chapter
        saved_sentences = []

        # 빈 문자열 제거
        split_sentences = [
            s.strip()
            for s in re.split(r"[.?]", sentences)
            if s.strip()
        ]

        for sentence in split_sentences:
            saved = self.repository.create({
                "chapter": chapter,
                "content": sentence,
                "book_id": bookId,
            })
            saved_sentences.append(saved)

        # 마지막 문장은 다음 문장이 없으므로 len - 1까지만
        for i in range(len(saved_sentences) - 1):
            saved_sentences[i].after_id = saved_sentences[i + 1].id
            self.repository.update(saved_sentences[i])

        return saved_sentences
            
