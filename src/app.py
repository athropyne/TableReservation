from contextlib import asynccontextmanager

from fastapi import FastAPI
from starlette.middleware.cors import CORSMiddleware

from src.core.event_bus import EventBus
from src.services import subscribes
from src.services.reservations.routes import reservation_router
from src.services.tables.routes import table_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    event_bus = EventBus()
    for s in subscribes:
        event_bus.subscribe(*s)
    app.dependency_overrides = {EventBus: lambda: event_bus}
    yield


app = FastAPI(lifespan=lifespan)

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
