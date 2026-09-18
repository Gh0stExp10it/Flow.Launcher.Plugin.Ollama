import asyncio
import inspect
from typing import Any, Callable, Iterable, Type, Union

from .command import Command
from .result import Result, send_results
from .response import _collect_item


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
            return await self._await_maybe(await result)
        if inspect.isasyncgen(result):
            results = []
            command = None
            async for item in result:
                if isinstance(item, Command):
                    command = item
                    continue
                results.extend(_collect_item(item))
            if command is not None:
                return command
            return send_results(results)
        if isinstance(result, Result):
            return send_results([result])
        if isinstance(result, list):
            return send_results([r for r in result if isinstance(r, Result)])
        return result

    def _resolve_exception_handler(self, exc_type: Type[Exception]) -> Union[Callable[..., Any], None]:
        """Find the handler registered for the closest matching ancestor.

        Walks the exception type's MRO (most specific to least specific) so a
        handler registered for a base class also catches its subclasses,
        regardless of the order handlers were registered in - unlike a plain
        `isinstance` loop over `self._handlers`, which would be sensitive to
        that order.
        """
        for klass in exc_type.__mro__:
            if klass in self._handlers:
                return self._handlers[klass]
        return None

    async def trigger_exception_handler(self, exception: Exception) -> Any:
        handler = self._resolve_exception_handler(type(exception))
        if handler is None:
            raise exception
        return await self._await_maybe(handler(exception))

    async def trigger_event(self, event: str, *args, **kwargs) -> Any:
        try:
            result = self.get_event(event)(*args, **kwargs)
            return await self._await_maybe(result)
        except Exception as e:
            return await self.trigger_exception_handler(e)
