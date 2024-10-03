from pydantic import BaseModel, ConfigDict


class PostItemDTO(BaseModel):
    model_config = ConfigDict(extra="forbid")

    name: str
    price: float
