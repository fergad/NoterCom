import uvicorn
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from app.routers import notes
from app.routers import UI
from app.routers import users
from app.db.Get_db_engine import create_db_and_tables
from app.settings import static_dir

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
print("Fastapi init ened")


app.include_router(UI.router)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>UI_notes INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
app.include_router(UI.router_without_auth)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>UI_notes INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
app.include_router(notes.router)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>notes INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
app.include_router(users.router)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>users INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
app.include_router(users.router_without_auth)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>users:/login INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")

@app.get("/", tags=["test"])
def greet():
    return {"msg": "Hello World!"}




if __name__ == "__main__":
    create_db_and_tables()
    #uvicorn.run(app, host="127.0.0.1", port=8000)
    uvicorn.run(app, host="0.0.0.0", port=8000)
