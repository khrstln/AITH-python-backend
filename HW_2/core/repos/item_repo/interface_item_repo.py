from abc import ABC, abstractmethod
from typing import Optional, List

from HW_2.core.entities.item import Item
from HW_2.core.repos.item_repo.dto.post_item_dto import PostItemDTO
from HW_2.core.repos.item_repo.dto.patch_item_dto import PatchItemDTO
from HW_2.core.repos.item_repo.dto.put_item_dto import PutItemDTO


class InterfaceItemRepo(ABC):
    @abstractmethod
    async def post_item(self, item_dto: PostItemDTO) -> Item:
        """Add a new item"""

    @abstractmethod
    async def get_item_by_id(self, id: int) -> Optional[Item]:
        """Returns an item by its id"""

    @abstractmethod
    async def get_items(self,
                        offset: Optional[int] = 0,
                        limit: Optional[int] = 10,
                        min_price: Optional[float] = None,
                        max_price: Optional[float] = None,
                        show_deleted: Optional[bool] = False) -> List[Item]:
        """Returns a list of items using filters"""

    @abstractmethod
    async def put_item(self, item_id: int,
                       item_dto: PutItemDTO) -> Optional[Item]:
        """Replaces an item by its id"""

    @abstractmethod
    async def patch_item(self, item_id: int,
                         item_dto: PatchItemDTO) -> Optional[Item]:
        """Updates an item's parameters"""

    @abstractmethod
    async def delete_item(self, item_id: int) -> Optional[Item]:
        """Deletes an item"""
