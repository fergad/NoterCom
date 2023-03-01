from settings import databse_dir
from sqlmodel import create_engine, SQLModel


print(databse_dir)
engine = create_engine("sqlite:///" + databse_dir, echo=True)

