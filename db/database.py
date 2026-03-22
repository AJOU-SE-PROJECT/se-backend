from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Use psycopg2 driver to avoid requiring the separate psycopg package.
DATABASE_URL = "postgresql+psycopg2://postgres:1234@localhost:5432/mydb"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
