from src.core.interfaces import Event
from src.core.types import ID


class ReservationCreatedEvent(Event):
    id: ID


class ReceivedReservationListEvent(Event):
    pass


class ReservationDeletedEvent(Event):
    id: ID
