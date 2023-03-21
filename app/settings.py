from pathlib import Path
BASE_PATH = Path(__file__).resolve().parent

databse_dir=str(BASE_PATH / 'db' / "database.db")

templates_dir = str(BASE_PATH / "templates")
static_dir = str(BASE_PATH / "static")
#templates = Jinja2Templates(directory=str(BASE_PATH.parent / "templates"))
addr="http://192.168.1.78"
host_port = "8000"
host_addr =addr+":"+host_port

ACCESS_TOKEN_EXPIRE_MINUTES = 1#60*24*7
ALGORITHM = "HS256"




#app.mount("/static", StaticFiles(directory="static"), name="static")
#app.mount('/static', StaticFiles(directory=os.path.join(current_dir, 'static')), name='static')
"""
BASE_PATH = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=str(BASE_PATH / "templates"))
app.mount("/static", StaticFiles(directory=str(BASE_PATH / "static")), name="static")
"""