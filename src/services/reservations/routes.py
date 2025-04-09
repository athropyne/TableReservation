from fastapi import APIRouter, Depends
from starlette import status

from src.core.types import ID
from src.services.reservations.dto.input import CreateReservationDTO
from src.services.reservations.dto.output import ReservationFullInfo
from src.services.reservations.services import CreateReservationService, GetReservationListService, DeleteReservationService

reservation_router = APIRouter(prefix="/reservations", tags=["Reservations"])


@reservation_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать бронь",
    response_model=ReservationFullInfo
)
async def create(
        model: CreateReservationDTO,
        service: CreateReservationService = Depends()
):
    return await service(model)


@reservation_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список броней",
    response_model=list[ReservationFullInfo]
)
async def get_list(
        skip: int = 0,
        limit: int = 50,
        service: GetReservationListService = Depends()
):
    return await service(skip, limit)


@reservation_router.delete(
    "/{reservation_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить бронь"
)
async def delete(
        reservation_id: ID,
        service: DeleteReservationService = Depends()
):
    await service(reservation_id)

