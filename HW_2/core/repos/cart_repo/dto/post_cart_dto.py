from pydantic import BaseModel
from typing import List

from entities.item import Item


class PostItemToCartDTO(BaseModel):
    name: str
    items: List[Item]
    price: str
