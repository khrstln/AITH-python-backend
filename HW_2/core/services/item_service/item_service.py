from typing import Optional, List

from HW_2.core.entities.item import Item
from HW_2.core.repos.item_repo.interface_item_repo import InterfaceItemRepo
from HW_2.core.repos.item_repo.dto.post_item_dto import PostItemDTO
from HW_2.core.repos.item_repo.dto.patch_item_dto import PatchItemDTO
from HW_2.core.repos.item_repo.dto.put_item_dto import PutItemDTO
from HW_2.core.services.interface.interface_item_service \
    import InterfaceItemService

from HW_2.core.exceptions.base_error import NegativeValueError, \
                                            NonPositiveValueError, \
                                            MinMaxError


class ItemService(InterfaceItemService):
    def __init__(self, item_repo: InterfaceItemRepo):
        self._item_repo = item_repo

    async def post_item(self, item_dto: PostItemDTO) -> Item:
        return await self._item_repo.post_item(item_dto)

    async def get_item_by_id(self, item_id: int) -> Item:
        # TO DO: Добавить исключения для случая, когда item с item_id
        # не существует
        return await self._item_repo.get_item_by_id(item_id)

    async def get_items(self,
                        offset: Optional[int] = 0,
                        limit: Optional[int] = 10,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None,
                        show_deleted: Optional[bool] = False) -> List[Item]:
        if offset < 0:
            raise NegativeValueError

        if limit <= 0:
            raise NonPositiveValueError

        if min_price < 0:
            raise NegativeValueError

        if max_price < 0:
            raise NegativeValueError

        if min_price is not None and max_price is not None and \
                min_price > max_price:
            MinMaxError

        return await self._item_repo.get_items(offset,
                                               limit,
                                               min_price,
                                               max_price,
                                               show_deleted)

    async def put_item(self, item_id: int, put_item_dto: PutItemDTO) -> Item:
        # TO DO: Добавить исключения для случая, когда item с item_id
        # не существует
        return await self._item_repo.put_item(item_id, put_item_dto)

    async def patch_item(self, item_id: int,
                         put_item_dto: PatchItemDTO) -> Item:
        # TO DO: Добавить исключения для случая, когда item с item_id
        # не существует
        return await self._item_repo.patch_item(item_id, put_item_dto)

    async def delete_item(self, item_id: int) -> Item:
        # TO DO: Добавить исключения для случая, когда item с item_id
        # не существует
        return await self._item_repo.delete_item(item_id)
