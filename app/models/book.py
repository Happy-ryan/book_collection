from odmantic import Model


class BookModel(Model):
    keyword: str
    title: str
    author: str
    publisher: str
    dis: int
    image: str

    class Config:
        collection = "books"


# db: fastapi-pj-> collection:books -> document {
#    keyword:str, publisher: str, price:str, age:str
# }
