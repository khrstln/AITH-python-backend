from pydantic import BaseModel
from typing import List
from HW_2.cart.entities.item_cart import ItemCart


class Cart(BaseModel):
    id: int
    items: List[ItemCart]
    price: float
