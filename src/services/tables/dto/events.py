from src.core.interfaces import Event
from src.core.types import ID


class TableCreatedEvent(Event):
    id: ID


class ReceivedTableListEvent(Event):
    pass


class TableDeletedEvent(Event):
    id: ID
