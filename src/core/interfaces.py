from abc import ABC, abstractmethod

from fastapi import Depends
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncEngine

from src.core.infrastructures import database
from src.core.infrastructures.postgresql import Database


class BaseSQLRepository(ABC):
    def __init__(self,
                 _database: Database = Depends(lambda: database)):
        self.engine: AsyncEngine = _database()

    @abstractmethod
    async def __call__(self, *args, **kwargs):
        pass


class BaseService(ABC):
    ...


class Event(BaseModel):
    pass


class Singleton(ABC):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance


class Observer(ABC):
    @abstractmethod
    async def __call__(self, event: Event):
        pass

