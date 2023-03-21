from settings import databse_dir
from sqlmodel import create_engine, SQLModel, Session


print(databse_dir)
engine = create_engine("sqlite:///" + databse_dir, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    with Session(engine) as session:
        yield session


def get_db_like_that():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()

def db_clear_metadata():
    SQLModel.metadata.clear()
