from pydantic import BaseModel
from typing import Optional


class PatchItemDTO(BaseModel):
    name: Optional[str]
    price: Optional[float]
