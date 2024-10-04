from typing import Optional, List

from HW_2.cart.entities.cart import Cart
from HW_2.cart.repos.interface.interface_cart_repo import InterfaceCartRepo
from HW_2.cart.services.interface.interface_cart_service import InterfaceCartService
from HW_2.item.services.interface.interface_item_service import InterfaceItemService

from HW_2.exceptions.base_error import NegativeValueError, NonPositiveValueError, MinMaxError


class CartService(InterfaceCartService):
    def __init__(self, cart_repo: InterfaceCartRepo, item_repo: InterfaceItemService) -> None:
        self._item_repo = item_repo
        self._cart_repo = cart_repo

    def post_cart(self) -> id:
        return self._cart_repo.post_cart()

    def get_cart_by_id(self, cart_id: int) -> Cart:
        return self._cart_repo.get_cart_by_id(cart_id)

    def get_carts(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        min_quantity: Optional[int] = None,
        max_quantity: Optional[int] = None,
    ) -> List[Cart]:
        if offset < 0:
            raise NegativeValueError

        if limit <= 0:
            raise NonPositiveValueError

        if min_price is not None and min_price < 0:
            raise NegativeValueError

        if max_price is not None and max_price < 0:
            raise NegativeValueError

        if min_price is not None and max_price is not None and min_price > max_price:
            MinMaxError

        if min_quantity is not None and min_quantity < 0:
            raise NegativeValueError

        if max_quantity is not None and max_quantity < 0:
            raise NegativeValueError

        if min_quantity is not None and max_quantity is not None and min_quantity > max_quantity:
            MinMaxError

        return self._cart_repo.get_carts(offset, limit, min_price, max_price, min_quantity, max_quantity)

    def post_item_to_cart(self, item_id: int, cart_id: int) -> Cart:
        item = self._item_repo.get_item_by_id(item_id)

        return self._cart_repo.post_item_to_cart(item, cart_id)