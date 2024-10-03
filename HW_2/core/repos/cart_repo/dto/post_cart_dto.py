from pydantic import BaseModel
from typing import List

from HW_2.core.entities.item import Item


class PostCartDTO(BaseModel):
    name: str
    items: List[Item]
    price: float
