from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pathlib import Path
from app.models import mongodb
from app.models.book import BookModel
from app.book_scraper import NaverBookScraper

from rich import print

BASE_URL = Path(__file__).resolve().parent

app = FastAPI()

templates = Jinja2Templates(directory=BASE_URL / "templates")


@app.get("/", response_class=HTMLResponse)
async def root(request: Request):
    # book = BookModel(keyword= "python", publisher="BJPublic", price="1200", image="me.png")
    # print(await mongodb.engine.save(book)) # DB에 저장
    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "콜렉터북북이"}
    )


@app.get("/search", response_class=HTMLResponse)
async def search(request: Request, q: str):
    keyword = q
    print("search start", keyword)
    # 1.쿼리에서 검색어 추출
    # (예외 처리)
    # 검색어가 없다면 사용자에게 검색을 요구 return
    if not keyword:
        return templates.TemplateResponse(
            "./index.html", {"request": request, "title": "콜렉터 북북이"}
        )
    # 해당 검색어에 대해 수집된 데이터가 이미 DB에 존재한다면 해당 데이터를 사용자에게 제시
    if await mongodb.engine.find_one(BookModel, BookModel.keyword == keyword):
        books = await mongodb.engine.find(BookModel, BookModel.keyward == keyword)
        return templates.TemplateResponse(
            "./index.html", {"request": request, "title": "콜렉터 북북이", "books": books}
        )
    # 2. 데이터 수집기로 해당 검색어에 대해 데이터를 수집
    naver_book_scraper = NaverBookScraper()
    books = await naver_book_scraper.search(keyword, 10)
    book_models = []
    for book in books:
        # 예외처리
        title = book["title"]
        author = book["author"]
        publisher = book["publisher"]  # if "publisher" in book else ""
        discount = book["discount"]  # if "discount" in book else -1
        image = book["image"]  # if "image" in book else ""
        # print(book)
        book_model = BookModel(
            keyword=keyword,
            title=title,
            author=author,
            publisher=publisher,
            discount=discount,
            image=image,
        )
        book_model.Config
        book_models.append(book_model)
        print(book_model)
    await mongodb.engine.save_all(book_models)
    # print(book_model)
    # 3. DB에 수집된 데이터를 저장
    # 수집된 각각의 데이터에 대해서 db에 들어갈 모델 인스턴스를 찍는다.
    # 각 모델 인스턴스를 db에 저장

    return templates.TemplateResponse(
        "./index.html", {"request": request, "title": "콜렉터북북이", "books": books}
    )


@app.on_event("startup")
def on_app_start():
    mongodb.connect()


@app.on_event("shutdown")
def on_app_shutdown():
    print("bye server")
    mongodb.close()
