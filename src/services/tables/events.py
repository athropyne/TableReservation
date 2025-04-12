from fastapi import Depends
from faststream.redis import StreamSub
from faststream.redis.fastapi import RedisRouter

from src.core import config
from src.services.tables.dto.events import TableCreatedEvent, ReceivedTableListEvent, TableDeletedEvent
from src.services.tables.logs import CreateTableServiceLog, GetTableListServiceLog, DeleteTableServiceLog

table_log_router = RedisRouter(f"redis://{config.settings.REDIS_SOCKET}")


@table_log_router.subscriber(stream=StreamSub("table_created", group="loggers", consumer="1"))
async def table_created_log(event: TableCreatedEvent,
                            logger: CreateTableServiceLog = Depends()):
    await logger(event)


@table_log_router.subscriber(stream=StreamSub("table_list_received", group="loggers", consumer="1"))
async def table_list_received_log(event: ReceivedTableListEvent,
                                  logger: GetTableListServiceLog = Depends()):
    await logger(event)


@table_log_router.subscriber(stream=StreamSub("table_deleted", group="loggers", consumer="1"))
async def table_deleted_log(event: TableDeletedEvent,
                            logger: DeleteTableServiceLog = Depends()):
    await logger(event)
