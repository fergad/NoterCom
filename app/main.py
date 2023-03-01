import uvicorn
from fastapi import FastAPI

from sqlmodel import SQLModel

from fastapi.staticfiles import StaticFiles
from app.settings import static_dir
from routers import notes, users, UI
from app.db.Tables.TablesModels import engine

app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
print("Fastapi init ened")

SQLModel.metadata.create_all(engine)


app.include_router(users.router)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>USERS INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
app.include_router(notes.router)
print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>notes INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")
#app.include_router(UI.router)
#print(">>>>>>>>>>>>>>>>>>>>>>>>>>>>UI_notes INCLUDED<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<")



@app.get("/", tags=["test"])
def greet():
    return {"hello": "world!."}


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
