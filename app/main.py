from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel

BASE_URL = Path(__file__).resolve().parent

app = FastAPI()

templates = Jinja2Templates(directory=BASE_URL / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    book = BookModel(keyword= "python", publisher="BJPublic", price="1200", image="me.png")
    print(await mongodb.engine.save(book)) # DB에 저장
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "콜렉터북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    print(q)
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "콜렉터북북이", "keyword": q}
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    print("bye server")
    mongodb.close()
