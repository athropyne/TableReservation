from fastapi import Depends
from faststream.redis import StreamSub
from faststream.redis.fastapi import RedisRouter

from src.core import config
from src.services.reservations.dto.events import ReservationCreatedEvent, ReceivedReservationListEvent, \
    ReservationDeletedEvent
from src.services.reservations.logs import CreateReservationServiceLog, GetReservationListServiceLog, \
    DeleteReservationServiceLog

reservation_log_router = RedisRouter(f"redis://{config.settings.REDIS_SOCKET}")


@reservation_log_router.subscriber(stream=StreamSub("reservation_created", group="loggers", consumer="1"))
async def reservation_created_log(event: ReservationCreatedEvent,
                                  logger: CreateReservationServiceLog = Depends()):
    await logger(event)


@reservation_log_router.subscriber(stream=StreamSub("reservation_list_received", group="loggers", consumer="1"))
async def reservation_list_received_log(event: ReceivedReservationListEvent,
                                        logger: GetReservationListServiceLog = Depends()):
    await logger(event)


@reservation_log_router.subscriber(stream=StreamSub("reservation_deleted", group="loggers", consumer="1"))
async def reservation_deleted_log(event: ReservationDeletedEvent,
                                  logger: DeleteReservationServiceLog = Depends()):
    await logger(event)
