import asyncio
from typing import Type

from src.core.interfaces import Event, Observer, Singleton


class EventBus(Singleton):
    def __init__(self):
        self._subscribers: dict[Type[Event], list[Type[Observer]]] = {}

    def subscribe(self, event: Type[Event], observer: Type[Observer]):
        if event not in self._subscribers:
            self._subscribers[event] = []
        self._subscribers[event].append(observer)

    async def publish(self, event: Event):
        event_type = type(event)
        if event_type in self._subscribers:
            await asyncio.gather(*[observer()(event) for observer in self._subscribers[event_type]])

