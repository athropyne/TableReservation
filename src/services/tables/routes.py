from fastapi import APIRouter, Depends
from starlette import status

from src.core.types import ID
from src.services.tables.dto.input import CreateTableDTO
from src.services.tables.dto.output import TableFullInfo
from src.services.tables.services import CreateTableService, GetTableListService, DeleteTableService

table_router = APIRouter(prefix="/tables", tags=["Tables"])


@table_router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    summary="Создать стол",
    response_model=TableFullInfo
)
async def create(
        model: CreateTableDTO,
        service: CreateTableService = Depends()
):
    return await service(model)


@table_router.get(
    "/",
    status_code=status.HTTP_200_OK,
    summary="Получить список столов",
    response_model=list[TableFullInfo]
)
async def get_list(
        skip: int = 0,
        limit: int = 50,
        service: GetTableListService = Depends()
):
    return await service(skip, limit)


@table_router.delete(
    "/{table_id}",
    status_code=status.HTTP_204_NO_CONTENT,
    summary="Удалить стол"
)
async def delete(
        table_id: ID,
        service: DeleteTableService = Depends()
):
    await service(table_id)
