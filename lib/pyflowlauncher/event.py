import asyncio
from typing import Any, Callable, Iterable, Type, Union


class EventNotFound(Exception):

    def __init__(self, event: str):
        self.event = event
        super().__init__(f"Event '{event}' not found.")


class EventHandler:

    def __init__(self):
        self._events = {}
        self._handlers = {}

    def _get_callable_name(self, method: Union[Callable[..., Any], Exception]):
        return getattr(method, '__name__', method.__class__.__name__).lower()

    def add_event(self, event: Callable[..., Any], *, name=None) -> str:
        key = name or self._get_callable_name(event)
        self._events[key] = event
        return key

    def add_events(self, events: Iterable[Callable[..., Any]]):
        for event in events:
            self.add_event(event)

    def add_exception_handler(self, exception: Type[Exception], handler: Callable[..., Any]):
        self._handlers[exception] = handler

    def get_event(self, event: str) -> Callable[..., Any]:
        try:
            return self._events[event]
        except KeyError:
            raise EventNotFound(event)

    async def _await_maybe(self, result: Any) -> Any:
        if asyncio.iscoroutine(result):
            return await result
        return result

    async def trigger_exception_handler(self, exception: Exception) -> Any:
        try:
            handler = self._handlers[exception.__class__]
            return await self._await_maybe(handler(exception))
        except KeyError:
            raise exception

    async def trigger_event(self, event: str, *args, **kwargs) -> Any:
        try:
            result = self.get_event(event)(*args, **kwargs)
            return await self._await_maybe(result)
        except Exception as e:
            return await self.trigger_exception_handler(e)
