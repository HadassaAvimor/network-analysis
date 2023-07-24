from requests import Request

from fastapi import FastAPI
import uvicorn

from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import requests

app = FastAPI()


@app.get('/maps')
def maps():
    return "hiiiii haddasa"


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)


def pr():
    print("hiii")
