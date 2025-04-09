from fastapi import Depends

from src.core.event_bus import EventBus
from src.core.interfaces import BaseService
from src.core.types import ID
from src.services.tables.dto.events import TableCreatedEvent
from src.services.tables.dto.input import CreateTableDTO
from src.services.tables.dto.output import TableFullInfo
from src.services.tables.repositories import CreateNewTableCommand, GetTableListQuery, DeleteTableCommand


class CreateTableService(BaseService):
    def __init__(self,
                 repo: CreateNewTableCommand = Depends(),
                 event_bus: EventBus = Depends()):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self,
                       model: CreateTableDTO) -> TableFullInfo:
        result = await self.repo(model.model_dump())
        await self.event_bus.publish(TableCreatedEvent(id=result.id))
        return result


class GetTableListService(BaseService):
    def __init__(self,
                 repo: GetTableListQuery = Depends()):
        self.repo = repo

    async def __call__(self,
                       skip: int,
                       limit: int) -> list[TableFullInfo]:
        result = await self.repo(skip, limit)
        return result


class DeleteTableService(BaseService):
    def __init__(self,
                 repo: DeleteTableCommand = Depends()):
        self.repo = repo

    async def __call__(self, table_id: ID) -> None:
        await self.repo(table_id)
