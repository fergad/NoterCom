import uvicorn
from fastapi import FastAPI



from fastapi.staticfiles import StaticFiles
from app.settings import static_dir
from routers import notes, users, UI
from app.db.Get_db_engine import create_db_and_tables


app = FastAPI()
app.mount("/static", StaticFiles(directory=static_dir), name="static")
print("Fastapi init ened")




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
    create_db_and_tables()
    uvicorn.run(app, host="127.0.0.1", port=8000)
