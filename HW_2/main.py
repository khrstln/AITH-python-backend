from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from HW_2.infrastructure.api.routers import all_routers

app = FastAPI(title="Shop API",
              swagger_ui_parameters={"defaultModelsExpandDepth": -1})

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

for router in all_routers:
    app.include_router(router)
