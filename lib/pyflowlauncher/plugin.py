from __future__ import annotations

import sys
from functools import cached_property, wraps
from typing import Any, Callable, Iterable, Optional, Type, List
from pathlib import Path
import asyncio

from .base import pyFlowLauncherObject

from .event import EventHandler
from .jsonrpc import JsonRPCClient, JsonRPCRequest
from .models.plugin_manifest import FILE_NAME
from .manifest import Manifest


Method = Callable[..., Any]


class Plugin(pyFlowLauncherObject):

    def __init__(self, methods: list[Method] | None = None) -> None:
        super().__init__()
        self._client = JsonRPCClient()
        self._event_handler = EventHandler()
        self._settings: dict[str, Any] = {}
        if methods:
            self.add_methods(methods)

    def add_method(self, method: Method) -> str:
        """Add a method to the event handler."""
        setattr(method, '_is_registered_method', True)
        return self._event_handler.add_event(method)

    def add_methods(self, methods: Iterable[Method]) -> None:
        self._event_handler.add_events(methods)

    def on_method(self, method: Method) -> Method:
        @wraps(method)
        def wrapper(*args, **kwargs):
            return method(*args, **kwargs)
        self.add_method(wrapper)
        return wrapper

    def method(self, method: Method) -> Method:
        """Register a method to be called when the plugin is run."""
        return self.on_method(method)

    def add_exception_handler(self, exception: Type[Exception], handler: Callable[..., Any]) -> None:
        """Add exception handler to be called when an exception is raised in a method."""
        self._event_handler.add_exception_handler(exception, handler)

    def on_except(self, exception: Type[Exception]) -> Callable[..., Any]:
        @wraps(exception)
        def wrapper(handler: Callable[..., Any]) -> Callable[..., Any]:
            self.add_exception_handler(exception, handler)
            return handler
        return wrapper

    def action(self, method: Method, parameters: Optional[List] = None) -> JsonRPCRequest:
        """Register a method and return a JsonRPCRequest that calls it."""
        method_name = self.add_method(method)
        return {"method": method_name, "parameters": parameters or []}

    @property
    def settings(self) -> dict:
        if self._settings is None:
            self._settings = {}
        self._settings = self._client.recieve().get('settings', {})
        return self._settings

    def run(self) -> None:
        request = self._client.recieve()
        method = request["method"]
        parameters = request.get('parameters', [])
        if sys.version_info >= (3, 10, 0):
            feedback = asyncio.run(self._event_handler.trigger_event(method, *parameters))
        else:
            loop = asyncio.get_event_loop()
            feedback = loop.run_until_complete(self._event_handler.trigger_event(method, *parameters))
        if not feedback:
            return
        self._client.send(feedback)

    @property
    def run_dir(self) -> Path:
        """Return the run directory of the plugin."""
        return Path(sys.argv[0]).resolve().parent

    @cached_property
    def root_dir(self) -> Path:
        """Return the root directory of the plugin."""
        current_dir = self.run_dir
        for part in current_dir.parts:
            if current_dir.joinpath(FILE_NAME).exists():
                return current_dir
            current_dir = current_dir.parent
        raise FileNotFoundError(f"Could not find {FILE_NAME} in {self.run_dir} or any parent directory.")

    @cached_property
    def manifest_path(self) -> Path:
        """Return the path to the plugin manifest."""
        return self.root_dir / FILE_NAME

    @cached_property
    def manifest(self) -> Manifest:
        """Return the plugin manifest."""
        return Manifest.from_file(self.manifest_path)
