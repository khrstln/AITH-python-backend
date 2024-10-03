from HW_2.infrastructure.api.cart import router as cart_router
from HW_2.infrastructure.api.item import router as item_router

all_routers = [
    item_router,
    cart_router,
]
