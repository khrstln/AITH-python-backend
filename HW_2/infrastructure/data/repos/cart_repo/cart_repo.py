from typing import Optional, List

from HW_2.core.repos.cart_repo.interface_cart_repo import InterfaceCartRepo
from HW_2.core.entities.cart import Cart
from HW_2.core.entities.item import Item


class CartRepo(InterfaceCartRepo):
    def __init__(self) -> None:
        self._carts = []

    async def post_cart(self) -> int:
        cart = Cart(id=len(self._carts), items=[], price=0.0)
        self._carts.append(cart)

        return cart.id

    async def get_cart_by_id(self, cart_id: int) -> Optional[Cart]:
        try:
            cart = self._carts[cart_id]
            return cart
        except IndexError:
            return None

    async def get_carts(self,
                        offset: Optional[int] = 0,
                        limit: Optional[int] = 10,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None,
                        min_quantity: Optional[int] = None,
                        max_quantity: Optional[int] = None) -> List[Cart]:
        try:
            carts = self._carts[offset:offset + \
                                min(limit, len(self._carts) - offset)]
        except IndexError:
            return None

        if min_price is not None:
            carts = [cart for cart in carts if cart.price >= min_price]

        if max_price is not None:
            carts = [cart for cart in carts if cart.price <= max_price]

        if min_quantity is not None:
            carts = [cart for cart in self._carts if len(cart.items)
                     >= min_quantity]

        if max_quantity is not None:
            carts = [cart for cart in self._carts if len(cart.items)
                     <= max_quantity]

        return carts

    async def post_item_to_cart(self, items: List[Item],  item_id: int,
                                cart_id: int) -> Optional[Cart]:
        try:
            cart = self._carts[cart_id]
        except IndexError:
            return None

        try:
            new_item = items[item_id]
        except IndexError:
            return None

        cart.items.append(new_item)

        cart.price += new_item.price

        return cart
