from typing import Optional, List

from HW_2.core.repos.item_repo.interface_item_repo import InterfaceItemRepo
from HW_2.core.repos.item_repo.dto.post_item_dto import PostItemDTO
from HW_2.core.repos.item_repo.dto.put_item_dto import PutItemDTO
from HW_2.core.repos.item_repo.dto.patch_item_dto import PatchItemDTO
from HW_2.core.entities.item import Item


class ItemRepo(InterfaceItemRepo):
    def __init__(self) -> None:
        self._items = []

    async def post_item(self, item_dto: PostItemDTO) -> Optional[Item]:
        item = Item(id=len(self._items), name=item_dto.name,
                    price=item_dto.price, deleted=False)
        self._items.append(item)

        return item

    async def get_item_by_id(self, id: int) -> Optional[Item]:
        try:
            item = self._items[id]
            return item
        except IndexError:
            return None

    async def get_items(self,
                        offset: Optional[int] = 0,
                        limit: Optional[int] = 10,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None,
                        show_deleted: Optional[bool] = False) -> List[Item]:

        try:
            items = self._items[offset:offset + min(limit, len(self._items) - offset)]
        except IndexError:
            return None

        if not show_deleted:
            items = [item for item in items if not item.deleted]

        if min_price is not None:
            items = [item for item in items if item.price >= min_price]

        if max_price is not None:
            items = [item for item in items if item.price <= max_price]

        return items

    async def put_item(self, item_id: int,
                       item_dto: PutItemDTO) -> Optional[Item]:
        try:
            replaced_item = self._items[item_id]
        except IndexError:
            raise ValueError("Wrong item_id!")

        self._items[item_id].name = item_dto.name
        self._items[item_id].price = item_dto.price

        return replaced_item

    async def patch_item(self, item_id: int, item_dto: PatchItemDTO) -> Item:
        try:
            updated_item = self._items[item_id]
        except IndexError:
            return None

        if item_dto.name is not None:
            updated_item.name = item_dto.name

        if item_dto.price is not None:
            updated_item.price = item_dto.price

        self._items[item_id] = updated_item

        return updated_item

    async def delete_item(self, item_id: int) -> Item:
        try:
            deleted_item = self._items[item_id]
        except IndexError:
            return None

        deleted_item.deleted = True

        self._items[item_id] = deleted_item

        return deleted_item
