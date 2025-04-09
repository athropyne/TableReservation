import datetime

from pydantic import BaseModel, Field, PositiveInt

from src.core.types import ID


class CreateReservationDTO(BaseModel):
    customer_name: str = Field(..., max_length=100, description="Имя заказчика")
    table_id: ID = Field(..., description="ID стола")
    reservation_time: datetime.datetime = Field(...)
    duration_minutes: PositiveInt = Field(...)
