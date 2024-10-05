from abc import ABC, abstractmethod
from typing import Optional, List

from HW_2.item.entities.item import Item
from HW_2.item.repos.dto.post_item_dto import PostItemDTO
from HW_2.item.repos.dto.put_item_dto import PutItemDTO
from HW_2.item.repos.dto.patch_item_dto import PatchItemDTO


class InterfaceItemRepo(ABC):
    @abstractmethod
    def post_item(self, item_dto: PostItemDTO) -> Item:
        """Add a new item"""

    @abstractmethod
    def get_item_by_id(self, id: int) -> Optional[Item]:
        """Returns an item by its id"""

    @abstractmethod
    def get_items(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        show_deleted: Optional[bool] = False,
    ) -> List[Item]:
        """Returns a list of items using filters"""

    @abstractmethod
    def put_item(self, item_id: int, item_dto: PutItemDTO) -> Item:
        """Replaces an item by its id"""

    @abstractmethod
    def patch_item(self, item_id: int, item_dto: PatchItemDTO) -> Optional[Item]:
        """Updates an item's parameters"""

    @abstractmethod
    def delete_item(self, item_id: int) -> Optional[Item]:
        """Deletes an item"""
