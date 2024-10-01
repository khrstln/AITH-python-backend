from abc import ABC, abstractmethod
from typing import Optional

from entities.item import Item
from HW_2.core.repos.item_repo.dto.post_item_dto import PostItemDTO
from HW_2.core.repos.item_repo.dto.patch_item_dto import PatchItemDTO
from HW_2.core.repos.item_repo.dto.put_item_dto import PutItemDTO


class InterfaceItemService(ABC):
    @abstractmethod
    async def create_item(self, item_dto: PostItemDTO) -> Item:
        """
        Creates a new item

        Args:
            item_dto (PostItemDTO): information about the item to be created

        Returns:
            Item: created item
        """

    @abstractmethod
    async def get_item_by_id(self, item_id: int) -> Item:
        """
        Returns an item by its id

        Args
            item_id (int): id of the item

        Returns:
            Item: found item
        """

    @abstractmethod
    async def get_items(
        self,
        offset: int = 0,
        limit: int = 10,
        min_price: Optional[float] = None,
        max_price: Optional[float] = None,
        show_deleted: bool = False,
    ) -> list[Item]:
        """
        Returns a list of items using filters

        Args:
            offset (int): offset by the list, defaults to 0
            limit (int): limit on the number of, defaults to 10
            min_price (float): minimal price, defaults to None
            max_price (float): maximal price, defaults to None
            show_deleted (bool): whether to show deleted items,
                                 defaults to False

        Returns:
            List[Item]: list of items using filters
        """

    @abstractmethod
    async def put_item(self, item_id: int, put_item_dto: PutItemDTO) -> Item:
        """
        Replace an item by its id

        Args:
            item_id (int): id of the item
            put_item_dto (PutItemDTO): information about the item to be updated

        Returns:
            Item: replaced item
        """

    @abstractmethod
    async def patch_item(self, item_id: int,
                         patch_item_dto: PatchItemDTO) -> Item:
        """
        Updates an item

        Args:
            tem_id (int): id of the item
            patch_item_dto (PatchItemDTO): information about the item
                                           to be updated

        Returns:
            Item: updated item
        """

    @abstractmethod
    async def delete_item(self, item_id: int) -> Item:
        """
        Deletes an item

        Returns:
            item_id: id of the item

        Returns:
            Item: deleted item
        """
