from typing import Optional
from fastapi import FastAPI, HTTPException, Query, Request
from fastapi.responses import JSONResponse
from prometheus_client import Counter, Histogram
from prometheus_fastapi_instrumentator import Instrumentator
from starlette.middleware.cors import CORSMiddleware

from HW_2.item.repos.dto.post_item_dto import PostItemDTO
from HW_2.item.repos.dto.put_item_dto import PutItemDTO
from HW_2.item.repos.dto.patch_item_dto import PatchItemDTO
from HW_2.cart.services.cart_service import CartService
from HW_2.item.services.item_service import ItemService
from HW_2.cart.repos.cart_repo import CartRepo
from HW_2.item.repos.item_repo import ItemRepo

app = FastAPI(title="Shop API", swagger_ui_parameters={"defaultModelsExpandDepth": -1})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

REQUEST_COUNT = Counter("app_requests_total", "Total number of requests")
REQUEST_DURATION = Histogram("app_request_duration_seconds", "Duration of requests in seconds")
ERROR_COUNT = Counter("app_errors_total", "Total number of errors")


@app.middleware("http")
async def add_prometheus_metrics(request: Request, call_next):
    REQUEST_COUNT.inc()
    with REQUEST_DURATION.time():
        try:
            response = await call_next(request)
            if response.status_code >= 400:
                ERROR_COUNT.inc()
            return response
        except Exception as e:
            ERROR_COUNT.inc()
            raise e


Instrumentator().instrument(app).expose(app)


item_repo = ItemRepo()
item_service = ItemService(item_repo)
cart_service = CartService(CartRepo(), item_repo)


@app.post("/cart")
async def post_cart():
    try:
        cart = cart_service.post_cart()
        return JSONResponse(
            content={"id": cart},
            headers={"location": f"/cart/{cart}"},
            status_code=201,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.get("/cart/{id}")
async def get_cart_by_id(id: int):
    try:
        cart = cart_service.get_cart_by_id(id)
        if cart is None:
            raise HTTPException(status_code=404)
        return cart.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get("/cart")
async def get_carts(
    offset: int = Query(0, ge=0, description="Non-negative integer, offset."),
    limit: int = Query(
        10,
        gt=0,
        description="Positive integer, maxial number of carts.",
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Minimal price.",
    ),
    max_price: Optional[float] = Query(
        None,
        ge=0,
        description="Maximal price.",
    ),
    min_quantity: Optional[int] = Query(
        None,
        ge=0,
        description="Minimal quantity.",
    ),
    max_quantity: Optional[int] = Query(
        None,
        ge=0,
        description="Maximal quantity.",
    ),
):
    try:
        carts = cart_service.get_carts(
            offset=offset,
            limit=limit,
            min_price=min_price,
            max_price=max_price,
            min_quantity=min_quantity,
            max_quantity=max_quantity,
        )
        return [cart.model_dump() for cart in carts]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/cart/{cart_id}/add/{item_id}")
async def add_item_to_cart(cart_id: int, item_id: int):
    try:
        cart = cart_service.post_item_to_cart(item_id, cart_id)
        if cart is None:
            raise HTTPException(status_code=400)
        return cart.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.post("/item")
async def add_item(item_dto: PostItemDTO):
    item = item_service.post_item(item_dto)
    return JSONResponse(content=item.model_dump(), status_code=201)


@app.get("/item/{item_id}")
async def get_item_by_id(item_id: int):
    try:
        item = item_service.get_item_by_id(item_id)
        return item
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except TypeError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.get("/item")
async def get_items(
    offset: int = Query(0, ge=0, description="Non-negative integer, offset."),
    limit: int = Query(
        10,
        gt=0,
        description="Positive integer, limit of items.",
    ),
    min_price: Optional[float] = Query(
        None,
        ge=0,
        description="Non-negative number, minimal price for item.",
    ),
    max_price: Optional[float] = Query(
        None,
        gt=0,
        description="Non-negative number, maximal price for item.",
    ),
    show_deleted: Optional[bool] = Query(
        False,
        description="Whether to show deleted items.",
    ),
):
    try:
        items = item_service.get_items(
            offset=offset, limit=limit, min_price=min_price, max_price=max_price, show_deleted=show_deleted
        )
        return [item.model_dump() for item in items]
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.put("/item/{item_id}")
async def update_item(item_id: int, item_dto: PutItemDTO):
    try:
        replaced_item = item_service.put_item(item_id, item_dto)
        return replaced_item.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e


@app.patch("/item/{item_id}")
async def patch_item(item_id: int, item_dto: PatchItemDTO):
    try:
        updated_item = item_service.patch_item(item_id, item_dto)
        return updated_item.model_dump()
    except TypeError as e:
        raise HTTPException(status_code=304, detail=str(e)) from e
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e


@app.delete("/item/{item_id}")
async def delete_item(item_id: int):
    try:
        deleted_item = item_service.delete_item(item_id)
        return deleted_item.model_dump()
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except TypeError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
