from pydantic import BaseModel
from typing import Optional


class Producto(BaseModel):
    id: int
    nombre: str
    precio: float
    stock: int

class ProductoUpdate(BaseModel):
    nombre: Optional[str] = None
    precio: Optional[float] = None
    stock: Optional[int] = None