from typing import Optional, List

from entities.cart import Cart
from interface.interface_cart_service import IntefaceCartService
from HW_2.core.repos.cart_repo.interface_cart_repo import InterfaceCartRepo


class IntefaceCartService(IntefaceCartService):
    # TO DO: написать реализацию всех методов
    def __init__(self, cart_repo: InterfaceCartRepo) -> None:
        self._cart_repo = cart_repo

    async def post_cart(self) -> id:
        raise NotImplementedError

    async def get_cart_by_id(self) -> Cart:
        raise NotImplementedError

    async def get_cart(self,
                       offset: Optional[int],
                       limit: Optional[int],
                       min_price: Optional[float],
                       max_price: Optional[float],
                       min_quantity: Optional[int],
                       max_quantity: Optional[int]) -> List[Cart]:
        raise NotImplementedError

    async def post_item_to_cart(self, item_id: int, cart_id: int) -> Cart:
        raise NotImplementedError
