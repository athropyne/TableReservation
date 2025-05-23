from fastapi import Depends
from faststream.redis.annotations import RedisBroker

from src.core.infrastructures.faststream import broker
from src.core.interfaces import BaseService
from src.core.types import ID
from src.services.reservations.dto.events import ReservationCreatedEvent, ReceivedReservationListEvent, \
    ReservationDeletedEvent
from src.services.reservations.dto.input import CreateReservationDTO
from src.services.reservations.dto.output import ReservationFullInfo
from src.services.reservations.repositories import CreateReservationCommand, GetReservationListQuery, \
    DeleteReservationCommand


class CreateReservationService(BaseService):
    def __init__(self,
                 repo: CreateReservationCommand = Depends(),
                 event_bus: RedisBroker = Depends(lambda: broker)):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self,
                       model: CreateReservationDTO) -> ReservationFullInfo:
        result = await self.repo(model.model_dump())
        await self.event_bus.publish(ReservationCreatedEvent(id=result.id), stream="reservation_created")
        return result


class GetReservationListService(BaseService):
    def __init__(self,
                 repo: GetReservationListQuery = Depends(),
                 event_bus: RedisBroker = Depends(lambda: broker)):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self,
                       skip: int,
                       limit: int) -> list[ReservationFullInfo]:
        result = await self.repo(skip, limit)
        await self.event_bus.publish(ReceivedReservationListEvent(), stream="reservation_list_received")
        return result


class DeleteReservationService(BaseService):
    def __init__(self,
                 repo: DeleteReservationCommand = Depends(),
                 event_bus: RedisBroker = Depends(lambda: broker)):
        self.repo = repo
        self.event_bus = event_bus

    async def __call__(self, reservation_id: ID) -> None:
        await self.repo(reservation_id)
        await self.event_bus.publish(ReservationDeletedEvent(id=reservation_id), stream="reservation_deleted")

