from __future__ import annotations

import json
import sys
from functools import cached_property, wraps
from typing import Any, Callable, Iterable, Optional, Type, List
from pathlib import Path
import asyncio

from .base import pyFlowLauncherObject

from .event import EventHandler
from .launcher import Launcher, FlowLauncherV1, FlowLauncherV2
from .jsonrpc import JsonRPCRequest
from .response import handle_response
from .models.plugin_manifest import FILE_NAME
from .manifest import Manifest


from .types import Method


class Plugin(pyFlowLauncherObject):

    def __init__(self, methods: list[Method] | None = None, launcher: Optional[Launcher] = None) -> None:
        super().__init__()
        self._launcher: Launcher = launcher if launcher is not None else self._detect_launcher()
        self._event_handler = EventHandler()
        if methods:
            self.add_methods(methods)

    def _detect_launcher(self) -> Launcher:
        try:
            if (self.manifest.language or '').lower() == 'python_v2':
                return FlowLauncherV2()
        except FileNotFoundError:
            pass
        except (json.JSONDecodeError, KeyError):
            self.logger.warning(
                "Malformed plugin manifest; defaulting to V1 launcher.", exc_info=True)
        return FlowLauncherV1()

    def add_method(self, method: Method) -> str:
        """Add a method to the event handler."""
        @wraps(method)
        def wrapper(*args, **kwargs):
            return handle_response(method(*args, **kwargs))
        setattr(wrapper, '_is_registered_method', True)
        setattr(method, '_is_registered_method', True)
        return self._event_handler.add_event(wrapper)

    def add_methods(self, methods: Iterable[Method]) -> None:
        for method in methods:
            self.add_method(method)

    def on_method(self, method: Method) -> Method:
        self.add_method(method)
        return method

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
    def launcher(self) -> Launcher:
        return self._launcher

    @property
    def settings(self) -> dict:
        return self._launcher.settings

    def run(self) -> None:
        async def dispatch(method: str, parameters: list) -> Any:
            return await self._event_handler.trigger_event(method, *parameters)

        if sys.version_info >= (3, 10, 0):
            asyncio.run(self._launcher.run(dispatch))
        else:
            loop = asyncio.get_event_loop()
            loop.run_until_complete(self._launcher.run(dispatch))

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
