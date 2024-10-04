from HW_2.item.entities.item import Item
from HW_2.item_cart.entities.item_cart import ItemCart


class ItemMapper:
    @staticmethod
    def to_item_cart(item: Item) -> ItemCart:
        return ItemCart(id=item.id, name=item.name, quantity=1, available=not item.deleted)
