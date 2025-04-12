from contextlib import asynccontextmanager

from fastapi import FastAPI
from faststream.redis import RedisBroker
from starlette.middleware.cors import CORSMiddleware

from src.core.infrastructures.faststream import broker
from src.services.reservations.events import reservation_log_router
from src.services.reservations.routes import reservation_router
from src.services.tables.events import table_log_router
from src.services.tables.routes import table_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    await broker.start()
    app.dependency_overrides = {RedisBroker: lambda: broker}
    yield


app = FastAPI(
    lifespan=lifespan,
    title="Table reservation",
    summary="Бронирование столиков"
)

##### НАСТРОИТЬ ПОД КОНКРЕТНЫЕ ИСТОЧНИКИ (вынести в конфиг)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

#####

app.include_router(table_router)
app.include_router(reservation_router)
app.include_router(table_log_router)
app.include_router(reservation_log_router)
