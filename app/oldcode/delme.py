from fastapi import FastAPI
import uvicorn
from subprocess import PIPE, Popen, run
import time


app = FastAPI()


@app.get("/get_m3u8", )
def get_m3u8():
    proc = Popen(f'docker run --rm -it rayou/streamlink:latest --stream-url "https://www.twitch.tv/nix" best', shell=True, stdin=PIPE, stdout=PIPE)
    time.sleep(5)
    out, err = proc.communicate()
    return {"out": out, "err": err}

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=7777)