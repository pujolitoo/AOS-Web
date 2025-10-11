from pydantic import BaseModel


class Product(BaseModel):
    name: str
    desc: str
    price: float
