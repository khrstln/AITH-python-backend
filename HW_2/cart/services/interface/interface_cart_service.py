from abc import ABC, abstractmethod
from typing import Optional, List

from HW_2.cart.entities.cart import Cart


class InterfaceCartService(ABC):
    @abstractmethod
    def post_cart(self) -> int:
        """Create a new cart"""

    @abstractmethod
    def get_cart_by_id(self, cart_id: int) -> Optional[Cart]:
        """Returns a cart by its id"""

    @abstractmethod
    def get_carts(
        self,
        offset: int,
        limit: int,
        min_price: Optional[float],
        max_price: Optional[float],
        min_quantity: Optional[int],
        max_quantity: Optional[int],
    ) -> List[Cart]:
        """Returns a list of carts using filters"""

    @abstractmethod
    def post_item_to_cart(self, item_id: int, cart_id: int) -> Optional[Cart]:
        """Add an item to the cart with cart_id with item_id.
        If the item is already there, then its quantity increases"""
