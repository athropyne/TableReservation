from src.services.tables.dto.events import TableCreatedEvent, ReceivedTableListEvent, TableDeletedEvent
from src.services.tables.logs import CreateTableServiceLog, GetTableListServiceLog, DeleteTableServiceLog

subscribes = [
    (TableCreatedEvent, CreateTableServiceLog),
    (ReceivedTableListEvent, GetTableListServiceLog),
    (TableDeletedEvent, DeleteTableServiceLog)
]