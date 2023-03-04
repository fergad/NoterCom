from settings import databse_dir
from sqlmodel import create_engine, SQLModel, Session


print(databse_dir)
engine = create_engine("sqlite:///" + databse_dir, echo=True)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_db():
    db = Session(engine)
    try:
        yield db
    finally:
        db.close()