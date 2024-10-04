from abc import ABC, abstractmethod
from typing import Optional, List

from HW_2.cart.entities.cart import Cart
from HW_2.item.entities.item import Item


class InterfaceCartRepo(ABC):
    @abstractmethod
    def post_cart(self) -> int:
        """Creates a new cart"""

    @abstractmethod
    def get_cart_by_id(self, cart_id: int) -> Cart:
        """Returns a cart by its id"""

    @abstractmethod
    def get_carts(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
    ) -> List[Cart]:
        """Returns a list of carts using filters"""

    @abstractmethod
    def post_item_to_cart(self, items: List[Item], item_id: int, cart_id: int) -> Cart:
        """Add an item to the cart with cart_id with item_id.
        If the item is already there, then its quantity increases"""
