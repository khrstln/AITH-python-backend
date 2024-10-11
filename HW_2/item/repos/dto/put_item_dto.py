from pydantic import BaseModel, ConfigDict
from typing import Optional


class PutItemDTO(BaseModel):
    name: Optional[str]
    price: Optional[float]

    model_config = ConfigDict(extra="forbid")
