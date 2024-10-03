from typing import Optional, List

from HW_2.core.entities.cart import Cart
from HW_2.core.services.interface.interface_cart_service \
    import InterfaceCartService
from HW_2.infrastructure.data.repos.cart_repo.cart_repo import CartRepo

from HW_2.core.exceptions.base_error import NegativeValueError, \
                                            NonPositiveValueError, \
                                            MinMaxError


class CartService(InterfaceCartService):
    def __init__(self, cart_repo: CartRepo) -> None:
        self._cart_repo = cart_repo

    async def post_cart(self) -> id:
        return await self._cart_repo.post_cart()

    async def get_cart_by_id(self, cart_id: int) -> Cart:
        # TO DO: добавить исключение для случая, когда cart_id
        # не существует
        return await self._cart_repo.get_cart_by_id(cart_id)

    async def get_carts(self,
                        offset: Optional[int] = 0,
                        limit: Optional[int] = 10,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None,
                        min_quantity: Optional[int] = None,
                        max_quantity: Optional[int] = None) -> List[Cart]:
        if offset < 0:
            raise NegativeValueError

        if limit <= 0:
            raise NonPositiveValueError

        if min_price is not None and min_price < 0:
            raise NegativeValueError

        if max_price is not None and max_price < 0:
            raise NegativeValueError

        if min_price is not None and max_price is not None and \
                min_price > max_price:
            MinMaxError

        if min_quantity is not None and min_quantity < 0:
            raise NegativeValueError

        if max_quantity is not None and max_quantity < 0:
            raise NegativeValueError

        if min_quantity is not None and max_quantity is not None and \
                min_quantity > max_quantity:
            MinMaxError

        return await self._cart_repo.get_carts(offset,
                                               limit,
                                               min_price,
                                               max_price,
                                               min_quantity,
                                               max_quantity)

    async def post_item_to_cart(self, item_id: int, cart_id: int) -> Cart:
        # TO DO: добавить исключение для случая, когда cart_id
        # или item_id не существует
        return await self._cart_repo.post_item_to_cart(item_id, cart_id)
