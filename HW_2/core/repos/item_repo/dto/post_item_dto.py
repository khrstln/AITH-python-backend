from pydantic import BaseModel


class PostItemDTO(BaseModel):
    name: str
    price: float
