from fastapi import APIRouter

router = APIRouter(
    prefix="/api/weak_test",
    tags=['weak_test']
)


"""
def fill_db():
    users = []
    first = User(name="First", email='first@x.com', password='123456', age=31)

    users.append(first)
    users.append(User(name='Second', email='second@x.com', password='223456', age=32))
    users.append(User(name='Third', email='third@x.com', password='323456', age=33))
    users.append(User(name='Second', email='fourth@x.com', password='423456', age=34))
    users.append(User(name='Second', email='fifth@x.com', password='523456', age=35))

    posts = []

    posts.append(Post(title="Penguins", body="Penguins are a group of aquatic flightless birds!"))

    posts.append(
    Post(title="Tigers", body="Tigers are the largest living cat species and a memeber of the genus panthera!"))
    posts.append(Post(title="Koalas", body="Koala is arboreal herbivorous maruspial native to Australia!"))
    posts.append(Post(title="Dogs", body="Dogs are human's bests friends!"))
    posts.append(Post(title="Cows", body="Cows are sacred in India!"))

    with Session(engine) as session:
        for u in users:
            session.add(u)
        session.commit()

        for p in posts:
            session.add(p)
            
@router.get("/fill_db")
def fill_empty_db():
    return fill_db()

"""
