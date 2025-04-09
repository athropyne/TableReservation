import psycopg
import sqlalchemy
from sqlalchemy import CursorResult, select

from src.core.interfaces import BaseSQLRepository
from src.core.schemas import reservations
from src.core.types import ID
from src.core.utils import catch
from src.services.reservations.dto.output import ReservationFullInfo
from src.services.reservations.exc import ReservationNotFound, TableAlreadyReserved
from src.services.tables.exc import TableNotFound


class CreateReservationCommand(BaseSQLRepository):
    @catch
    async def __call__(self, data: dict) -> ReservationFullInfo:
        stmt = reservations.insert().values(data).returning(reservations)
        async with self.engine.connect() as connection:
            try:
                cursor: CursorResult = await connection.execute(stmt)
            except sqlalchemy.exc.ProgrammingError as e:
                if isinstance(e.orig, psycopg.errors.RaiseException):
                    raise TableAlreadyReserved(data["table_id"])
            except sqlalchemy.exc.IntegrityError as e:
                if isinstance(e.orig, psycopg.errors.ForeignKeyViolation):
                    raise TableNotFound(data["table_id"])
            await connection.commit()
        result = cursor.mappings().fetchone()
        return ReservationFullInfo(**result)


class GetReservationListQuery(BaseSQLRepository):
    @catch
    async def __call__(self, skip: int, limit: int) -> list[ReservationFullInfo]:
        stmt = select(reservations).offset(skip).limit(limit)
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(stmt)
        result = cursor.mappings().fetchall()
        return [ReservationFullInfo(**row) for row in result]


class DeleteReservationCommand(BaseSQLRepository):
    @catch
    async def __call__(self, reservation_id: ID) -> None:
        stmt = reservations.delete().where(reservations.c.id == reservation_id)
        async with self.engine.connect() as connection:
            cursor: CursorResult = await connection.execute(stmt)
            if cursor.rowcount == 0:
                raise ReservationNotFound(reservation_id)
            await connection.commit()
