from typing import Annotated, Optional

from fastapi import APIRouter, Depends, HTTPException, Query
from starlette.responses import JSONResponse

from HW_2.infrastructure.api.dependencies import cart_service
from HW_2.core.repos.cart_repo.dto.post_cart_dto import PostCartDTO
from HW_2.core.services.cart_service.cart_service import CartService

router = APIRouter(
    prefix="/cart",
    tags=["Cart"],
)


@router.post("")
async def post_cart(
    post_cart_dto: PostCartDTO,
    cart_service: Annotated[CartService, Depends(cart_service)],
):
    try:
        cart_id = await cart_service.post_cart(post_cart_dto)
        return JSONResponse(
            content={"id": cart_id},
            headers={"location": f"/cart/{cart_id}"},
            status_code=201,
        )
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным cart_id
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.get("/{id}")
async def get_cart_by_id(
    id: int,
    cart_service: Annotated[CartService, Depends(cart_service)],
):
    try:
        cart = await cart_service.get_cart_by_id(id)
        return cart.model_dump()
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным cart_id
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("")
async def get_carts(
    cart_service: Annotated[CartService, Depends(cart_service)],
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
    item_id: int,
    cart_service: Annotated[CartService, Depends(cart_service)],
):
    try:
        cart = await cart_service.post_item_to_cart(cart_id, item_id)
        return cart.model_dump()
    except ValueError as e:  # TO DO: Написать исключения
        raise HTTPException(status_code=400, detail=str(e)) from e
