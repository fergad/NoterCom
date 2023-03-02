print("UsersCRUD begin")

from sqlmodel import Session, select
from app.db.Tables.TablesModels import User
from app.db.Tables.Schemas import Create_User, UserLoginSchema
#from app.db.Tables.TablesModels import engine
from app.db.Get_db_engine import engine



def create_user(user: Create_User):
    with Session(engine) as session:
        session.add(User(**user.dict()))
        session.commit()
        return


def delete_user(user_id: int):
    db = Session(engine)
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        return -1

    target_user.delete(synchronize_session=False)
    db.commit()
    return 1


def get_users():
    elem = User
    with Session(engine) as session:
        statement = select(elem)  #.where(User.name == "Spider-Boy")
        return session.exec(statement).all()


def check_user(visiter: UserLoginSchema):
    with Session(engine) as session:
        statement = select(User).where(User.email == visiter.email)
        result = session.exec(statement).first()
        if result.password == visiter.password:
            return True
        else:
            return False
