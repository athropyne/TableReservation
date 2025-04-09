from pydantic import BaseModel, Field


class TableFullInfo(BaseModel):
    id: int = Field(..., description="ID стола")
    name: str = Field(..., description="Название стола")
    seats: int = Field(..., description="Количество мест")
    location: str = Field(..., description="Локация")
