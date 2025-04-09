from loguru import logger

from src.core.interfaces import BaseLog, Observer
from src.services.tables.dto.events import TableCreatedEvent, ReceivedTableListEvent, TableDeletedEvent


class CreateTableServiceLog(BaseLog, Observer):
    async def __call__(self, event: TableCreatedEvent):
        logger.success(f"Стол с ID {event.id} создан")


class GetTableListServiceLog(BaseLog, Observer):
    async def __call__(self, event: ReceivedTableListEvent):
        logger.success(f"Список столов получен")


class DeleteTableServiceLog(BaseLog, Observer):
    async def __call__(self, event: TableDeletedEvent):
        logger.success(f"Стол с ID {event.id} удален")
