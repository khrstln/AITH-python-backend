from typing import Optional

from fastapi import APIRouter, HTTPException, Query
from starlette.responses import JSONResponse

from HW_2.core.repos.item_repo.dto.post_item_dto import PostItemDTO
from HW_2.core.repos.item_repo.dto.put_item_dto import PutItemDTO
from HW_2.core.repos.item_repo.dto.patch_item_dto import PatchItemDTO
from HW_2.core.services.item_service.item_service import ItemService
from HW_2.infrastructure.data.repos.item_repo.item_repo import ItemRepo

router = APIRouter(
    prefix="/item",
    tags=["Item"],
)

item_repo = ItemRepo()
item_service = ItemService(item_repo)


@router.post("")
async def add_item(
    item_dto: PostItemDTO
):
    item = await item_service.post_item(item_dto)
    return JSONResponse(content=item.model_dump(),
                        status_code=201)


@router.get("{item_id}")
async def get_item_by_id(
    item_id: int
):
    try:
        item = await item_service.get_item_by_id(item_id)
        return item
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным item_id
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.get("")
async def get_items(
    offset: int = Query(0, ge=0, description="Non-negative integer, offset."),
    limit: int = Query(0, gt=0, description="Positive integer, limit of \
                       items."),
    min_price: Optional[float] = Query(None, ge=0, description="Non-negative \
                                       number, minimal price for item."),
    max_price: Optional[float] = Query(None, gt=0, description="Non-negative \
                                       number, maximal price for item."),
    show_deleted: Optional[bool] = Query(False, description="Whether to show \
                                         deleted items.")
):
    try:
        items = await item_service.get_items(offset=offset,
                                             limit=limit,
                                             min_price=min_price,
                                             max_price=max_price,
                                             show_deleted=show_deleted)
        return [item.model_dump() for item in items]
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным item_id
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.put("{item_id}")
async def update_item(
    item_id: int,
    item_dto: PutItemDTO
):
    try:
        replaced_item = await item_service.put_item(item_id, item_dto)
        return replaced_item.model_dump()
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным item_id
        raise HTTPException(status_code=400, detail=str(e)) from e


@router.patch("/{item_id}")
async def patch_item(
    item_id: int,
    patch_item_dto: PatchItemDTO
):
    try:
        updated_item = await item_service.patch_item(item_id, patch_item_dto)
        return updated_item.model_dump()
    except TypeError as e:
        raise HTTPException(status_code=304, detail=str(e)) from e
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным item_id
        raise HTTPException(status_code=404, detail=str(e)) from e


@router.delete("/{item_id}")
async def delete_item(
    item_id: int
):
    try:
        deleted_item = await item_service.delete_item(item_id)
        return deleted_item.model_dump()
    except ValueError as e:  # TO DO: Написать исключения в случае отсутствия
        # товара с указанным item_id
        raise HTTPException(status_code=404, detail=str(e)) from e
