from src.core.exc import NotFound, ClientError
from src.core.types import ID


class ReservationNotFound(NotFound):
    def __init__(self, reservation_id: ID):
        super().__init__(f"Бронь с ID {reservation_id} не найдена")


class TableAlreadyReserved(ClientError):
    def __init__(self, table_id: ID):
        super().__init__(f"Столик с ID {table_id} уже забронирован на это время")
