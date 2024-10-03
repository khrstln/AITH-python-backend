from pydantic import BaseModel
from typing import List
from HW_2.core.entities.item import Item


class Cart(BaseModel):
    id: int
    items: List[Item] | None
    price: float
