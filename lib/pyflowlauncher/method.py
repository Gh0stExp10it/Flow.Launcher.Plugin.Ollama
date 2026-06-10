from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .models.json_rpc import JsonRPCRequest, JsonRPCResponse
from .result import Result, send_results
from .base import pyFlowLauncherObject


class Method(pyFlowLauncherObject, ABC):

    def __init__(self) -> None:
        super().__init__()
        self._results: list[Result] = []

    def add_result(self, result: Result) -> None:
        self._results.append(result)

    def return_results(self, settings: Optional[Dict[str, Any]] = None) -> JsonRPCResponse:
        return send_results(self._results, settings)

    @abstractmethod
    def __call__(self, *args, **kwargs) -> JsonRPCResponse | JsonRPCRequest:
        pass
