from pydantic import BaseModel, Field, PositiveInt


class CreateTableDTO(BaseModel):
    name: str = Field(..., max_length=20, description="Название стола")
    seats: PositiveInt = Field(..., description="Количество мест")
    location: str = Field(..., max_length=200, description="Локация")
