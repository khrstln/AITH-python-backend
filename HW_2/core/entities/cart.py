from pydantic import BaseModel


class Cart(BaseModel):
    id: int
    items: list
    price: float
