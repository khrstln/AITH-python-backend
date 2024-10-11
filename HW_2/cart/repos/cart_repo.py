from typing import Optional, List

from HW_2.cart.repos.interface.interface_cart_repo import InterfaceCartRepo
from HW_2.cart.entities.cart import Cart
from HW_2.item.entities.item import Item
from HW_2.item.mappers.item_mapper import ItemMapper


class CartRepo(InterfaceCartRepo):
    def __init__(self) -> None:
        self._carts: List[Cart] = []

    def post_cart(self) -> int:
        cart = Cart(id=len(self._carts), items=[], price=0.0)
        self._carts.append(cart)

        return cart.id

    def get_cart_by_id(self, cart_id: int) -> Optional[Cart]:
        try:
            cart = self._carts[cart_id]
            return cart
        except IndexError:
            return None

    def get_carts(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
    ) -> List[Cart]:
        try:
            carts = self._carts[offset : offset + min(limit, len(self._carts) - offset)]  # noqa E203
        except IndexError:
            return []

        if min_price is not None:
            carts = [cart for cart in carts if cart.price >= min_price]

        if max_price is not None:
            carts = [cart for cart in carts if cart.price <= max_price]

        if min_quantity is not None:
            carts = [cart for cart in self._carts if len(cart.items) >= min_quantity]

        if max_quantity is not None:
            carts = [cart for cart in self._carts if len(cart.items) <= max_quantity]

        return carts

    def post_item_to_cart(self, item: Item, cart_id: int) -> Optional[Cart]:
        try:
            cart = self._carts[cart_id]
        except IndexError:
            return None

        item_cart = ItemMapper.to_item_cart(item)

        if item.id not in [item_cart.id for item_cart in cart.items]:
            cart.items.append(item_cart)
        else:
            target_index = cart.items.index(item_cart)
            cart.items[target_index] += item_cart

        cart.price += item.price

        return cart
