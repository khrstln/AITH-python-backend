from pydantic import BaseModel
from typing import Optional


class PutItemDTO(BaseModel):
    name: Optional[str]
    price: Optional[float]
