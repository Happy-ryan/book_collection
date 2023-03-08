from odmantic import Model


class BookModel(Model):
    keyword: str
    publisher: str
    price: int
    image: str

    class Config:
        collection = "books"
        
# db: fastapi-pj-> collection:books -> document {
#    keyword:str, publisher: str, price:str, age:str
# }