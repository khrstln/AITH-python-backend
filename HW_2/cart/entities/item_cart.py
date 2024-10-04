from pydantic import BaseModel


class ItemCart(BaseModel):
    id: int
    name: str
    quantity: int
    available: bool

    def __add__(self, other: "ItemCart") -> "ItemCart":
        if self.id == other.id:
            self.quantity += other.quantity
            return self
        else:
            raise ValueError

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, ItemCart):
            return NotImplemented
        return self.id == other.id
