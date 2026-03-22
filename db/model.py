from os import name
from sqlalchemy import BIGINT, Column, Enum, ForeignKey, Integer, String, Text
from sqlalchemy.orm import relationship
from db.database import Base
from enum import Enum as PyEnum

class Gender(PyEnum):
    MALE = "male"
    FEMALE = "female"

class User(Base):
    __tablename__ = "authors"

    id= Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    name = Column(String(10), nullable=False)
    gender = Column(Enum(Gender), nullable=False)
    age = Column(Integer, nullable=False)
    intro = Column(Text, nullable=False)
    email = Column(String(50), nullable=False)


class Book(Base):
    __tablename__ = "books"

    id= Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    name = Column(String, nullable=False)

    author_id = Column(BIGINT, ForeignKey("authors.id"))

class Sentence(Base):
    __tablename__ = "sentences"

    id= Column(BIGINT, primary_key=True, autoincrement=True, index=True)
    chapter = Column(Integer, nullable=False)

    after_id = Column(BIGINT, ForeignKey("sentences.id"))
    book_id = Column(BIGINT, ForeignKey("books.id"))
    
    after_sentence = relationship(
        "Sentence",
        foreign_keys=[after_id],
        remote_side=[id],
        uselist=False
    )

    