from loguru import logger

from src.core.interfaces import BaseLog, Observer
from src.services.reservations.dto.events import ReservationCreatedEvent, ReceivedReservationListEvent, ReservationDeletedEvent


class CreateReservationServiceLog(BaseLog, Observer):
    async def __call__(self, event: ReservationCreatedEvent):
        logger.success(f"Бронь с ID {event.id} создана")


class GetReservationListServiceLog(BaseLog, Observer):
    async def __call__(self, event: ReceivedReservationListEvent):
        logger.success(f"Список броней получен")


class DeleteReservationServiceLog(BaseLog, Observer):
    async def __call__(self, event: ReservationDeletedEvent):
        logger.success(f"Бронь с ID {event.id} удалена")
