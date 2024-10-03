from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from starlette.responses import JSONResponse

from HW_2.core.repos.cart_repo.dto.post_cart_dto import PostCartDTO
from HW_2.core.services.cart_service.cart_service import CartService
from HW_2.infrastructure.data.repos.cart_repo.cart_repo import CartRepo

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)

cart_service = CartService(CartRepo())


@router.post("")
async def post_cart(
    cart_dto: PostCartDTO
):
    try:
        cart = await cart_service.post_cart()
        return JSONResponse(
            content={"id": cart},
            headers={"location": f"/cart/{cart}"},
            status_code=201,
        )
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным cart_id
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{id}")
async def get_cart_by_id(
    id: int
):
    try:
        cart = await cart_service.get_cart_by_id(id)
        return cart.model_dump()
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным cart_id
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("")
async def get_carts(
    offset: int = Query(0, ge=0, description="Non-negative integer, offset."),
    limit: int = Query(10, gt=0, description="Positive integer, maxial number \
                       of carts."),
    min_price: Optional[float] = Query(None, ge=0, description="Minimal \
                                       price."),
    max_price: Optional[float] = Query(None, ge=0, description="Maximal \
                                       price."),
    min_quantity: Optional[int] = Query(None, ge=0, description="Minimal \
                                        quantity."),
    max_quantity: Optional[int] = Query(None, ge=0, description="Maximal \
                                        quantity."),
):
    try:
        carts = await cart_service.get_carts(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
        )
        return [cart.model_dump() for cart in carts]
    except ValueError as e:  # TO DO: Написать исключения
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.post("/{cart_id}/add/{item_id}")
async def add_item_to_cart(
    cart_id: int,
    item_id: int
):
    try:
        cart = await cart_service.post_item_to_cart(cart_id, item_id)
        return cart.model_dump()
    except ValueError as e:  # TO DO: Написать исключения
        raise HTTPException(status_code=400, detail=str(e)) from e
