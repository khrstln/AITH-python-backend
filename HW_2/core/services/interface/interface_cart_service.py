from abc import ABC, abstractmethod
from typing import Optional, List

from HW_2.core.entities.cart import Cart


class CartService(ABC):
    @abstractmethod
    async def post_cart(self) -> id:
        """Create a new cart"""

    @abstractmethod
    async def get_cart_by_id(self) -> Cart:
        """Returns a cart by its id"""

    @abstractmethod
    async def get_cart(self,
                       offset: Optional[int],
                       limit: Optional[int],
                       min_price: Optional[float],
                       max_price: Optional[float],
                       min_quantity: Optional[int],
                       max_quantity: Optional[int]) -> List[Cart]:
        """Returns a list of carts using filters"""

    @abstractmethod
    async def post_item_to_cart(self, item_id: int, cart_id: int) -> Cart:
        """Add an item to the cart with cart_id with item_id.
        If the item is already there, then its quantity increases"""
