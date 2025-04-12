from loguru import logger

from src.core.interfaces import Observer
from src.services.reservations.dto.events import ReservationCreatedEvent, ReceivedReservationListEvent, ReservationDeletedEvent


class CreateReservationServiceLog(Observer):
    async def __call__(self, event: ReservationCreatedEvent):
        logger.success(f"Бронь с ID {event.id} создана")


class GetReservationListServiceLog(Observer):
    async def __call__(self, event: ReceivedReservationListEvent):
        logger.success(f"Список броней получен")


class DeleteReservationServiceLog(Observer):
    async def __call__(self, event: ReservationDeletedEvent):
        logger.success(f"Бронь с ID {event.id} удалена")
