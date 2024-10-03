from HW_2.core.repos.cart_repo.interface_cart_repo import InterfaceCartRepo
from HW_2.core.repos.item_repo.interface_item_repo import InterfaceItemRepo
from HW_2.core.services.cart_service.cart_service import CartService
from HW_2.core.services.item_service.item_service import ItemService


def cart_service():
    return CartService(InterfaceCartRepo)


def item_service():
    return ItemService(InterfaceItemRepo)
