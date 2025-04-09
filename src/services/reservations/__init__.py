from src.services.reservations.dto.events import ReservationCreatedEvent, ReceivedReservationListEvent, \
    ReservationDeletedEvent
from src.services.reservations.logs import CreateReservationServiceLog, GetReservationListServiceLog, \
    DeleteReservationServiceLog

subscribes = [
    (ReservationCreatedEvent, CreateReservationServiceLog),
    (ReceivedReservationListEvent, GetReservationListServiceLog),
    (ReservationDeletedEvent, DeleteReservationServiceLog)
]
