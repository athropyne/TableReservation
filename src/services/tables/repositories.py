from sqlalchemy import CursorResult, select

from src.core.interfaces import BaseSQLRepository
from src.core.schemas import tables
from src.core.types import ID
from src.core.utils import catch
from src.services.tables.dto.output import TableFullInfo
from src.services.tables.exc import TableNotFound


class CreateNewTableCommand(BaseSQLRepository):
    @catch
    async def __call__(self, data: dict) -> TableFullInfo:
        stmt = tables.insert().values(data).returning(tables)
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(stmt)
            await connection.commit()
        result = cursor.mappings().fetchone()
        return TableFullInfo(**result)


class GetTableListQuery(BaseSQLRepository):
    @catch
    async def __call__(self, skip: int, limit: int) -> list[TableFullInfo]:
        stmt = select(tables).offset(skip).limit(limit)
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(stmt)
        result = cursor.mappings().fetchall()
        return [TableFullInfo(**row) for row in result]


class DeleteTableCommand(BaseSQLRepository):
    @catch
    async def __call__(self, table_id: ID) -> None:
        stmt = tables.delete().where(tables.c.id == table_id)
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(stmt)
            if cursor.rowcount == 0:
                raise TableNotFound(table_id)
            await connection.commit()
