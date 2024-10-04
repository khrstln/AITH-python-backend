from typing import Optional, List

from HW_2.item.entities.item import Item
from HW_2.item.repos.interface.interface_item_repo import InterfaceItemRepo
from HW_2.item.repos.dto.post_item_dto import PostItemDTO
from HW_2.item.repos.dto.put_item_dto import PutItemDTO
from HW_2.item.repos.dto.patch_item_dto import PatchItemDTO
from HW_2.item.services.interface.interface_item_service import InterfaceItemService

from HW_2.exceptions.base_error import NegativeValueError, NonPositiveValueError, MinMaxError


class ItemService(InterfaceItemService):
    def __init__(self, item_repo: InterfaceItemRepo):
        self._item_repo = item_repo

    def post_item(self, item_dto: PostItemDTO) -> Item:
        return self._item_repo.post_item(item_dto)

    def get_item_by_id(self, item_id: int) -> Item:
        existing_item = self._item_repo.get_item_by_id(item_id)

        if existing_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        if existing_item.deleted:
            raise TypeError(f"Item with ID {item_id} is deleted so cannot be returned.")

        return existing_item

    def get_items(
        self,
        offset: Optional[int] = 0,
        limit: Optional[int] = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        show_deleted: Optional[bool] = False,
    ) -> List[Item]:
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

        return self._item_repo.get_items(offset, limit, min_price, max_price, show_deleted)

    def put_item(self, item_id: int, item_dto: PutItemDTO) -> Item:
        return self._item_repo.put_item(item_id, item_dto)

    def patch_item(self, item_id: int, item_dto: PatchItemDTO) -> Item:
        existing_item = self._item_repo.get_item_by_id(item_id)
        if existing_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        if existing_item.deleted:
            raise TypeError(f"Item with ID {item_id} is deleted so cannot be modified.")

        patched_item = self._item_repo.patch_item(item_id, item_dto)
        if patched_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        return patched_item

    def delete_item(self, item_id: int) -> Item:
        deleted_item = self._item_repo.delete_item(item_id)

        if deleted_item is None:
            raise ValueError(f"Item with ID {item_id} not found.")

        return deleted_item
