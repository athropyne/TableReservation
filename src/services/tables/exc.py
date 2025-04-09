from src.core.exc import NotFound
from src.core.types import ID


class TableNotFound(NotFound):
    def __init__(self, table_id: ID):
        super().__init__(detail=f"Стола с ID {table_id} не существует")
