from pydantic import BaseModel, ConfigDict


class PostItemDTO(BaseModel):
    name: str
    price: float

    model_config = ConfigDict(extra="forbid")
