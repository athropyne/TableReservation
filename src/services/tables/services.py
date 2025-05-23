from fastapi import Depends
from faststream.redis.annotations import RedisBroker

from src.core.infrastructures.faststream import broker
from src.core.interfaces import BaseService
from src.core.types import ID
from src.services.tables.dto.events import TableCreatedEvent, ReceivedTableListEvent, TableDeletedEvent
from src.services.tables.dto.input import CreateTableDTO
from src.services.tables.dto.output import TableFullInfo
from src.services.tables.repositories import CreateNewTableCommand, GetTableListQuery, DeleteTableCommand


class CreateTableService(BaseService):
    def __init__(self,
                 repo: CreateNewTableCommand = Depends(),
                 event_bus: RedisBroker = Depends(lambda: broker)):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self,
                       model: CreateTableDTO) -> TableFullInfo:
        result = await self.repo(model.model_dump())
        await self.event_bus.publish(TableCreatedEvent(id=result.id), stream="table_created")
        return result


class GetTableListService(BaseService):
    def __init__(self,
                 repo: GetTableListQuery = Depends(),
                 event_bus: RedisBroker = Depends(lambda: broker)):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self,
                       skip: int,
                       limit: int) -> list[TableFullInfo]:
        result = await self.repo(skip, limit)
        await self.event_bus.publish(ReceivedTableListEvent(), stream="table_list_received")
        return result


class DeleteTableService(BaseService):
    def __init__(self,
                 repo: DeleteTableCommand = Depends(),
                 event_bus: RedisBroker = Depends(lambda: broker)):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self, table_id: ID) -> None:
        await self.repo(table_id)
        await self.event_bus.publish(TableDeletedEvent(id=table_id), stream="table_deleted")
