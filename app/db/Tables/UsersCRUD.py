print("UsersCRUD begin")

from sqlmodel import Session, select
from app.db.Tables.TablesModels import User
from app.db.Tables.Schemas import CreateUser, UserLoginSchema


from fastapi import HTTPException


def create_user(user: CreateUser, db: Session):
    new_user = User.from_orm(user)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


def get_users(db: Session):
    elem = User
    statement = select(elem)  #.where(User.name == "Spider-Boy")
    result = db.exec(statement).all()
    if not result:
        raise HTTPException(status_code=404, detail="Item not found")
    return result


def delete_user(user_id: int, db: Session):
    target_user = db.query(User).filter(User.id == user_id).first()
    if not target_user:
        raise HTTPException(status_code=404, detail="Item not found")
    target_user.delete(synchronize_session=False)
    db.commit()
    return target_user


def check_user(visitor: UserLoginSchema, db: Session):
    statement = select(User).where(User.email == visitor.email)
    result = db.exec(statement).first()
    if result.password == visitor.password:
        return True
    else:
        return False

