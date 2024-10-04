from pydantic import BaseModel, ConfigDict


class PatchItemDTO(BaseModel):
    name: str | None = None
    price: float | None = None

    model_config = ConfigDict(extra="forbid")
