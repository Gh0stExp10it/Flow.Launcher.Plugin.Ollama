from __future__ import annotations

from abc import ABC, abstractmethod
from typing import Any, Dict, Optional

from .result import JsonRPCAction, Result, ResultResponse, send_results
from .shared import logger


class Method(ABC):

    def __init__(self) -> None:
        self._logger = logger(self)
        self._results: list[Result] = []

    def add_result(self, result: Result) -> None:
        self._results.append(result)

    def return_results(self, settings: Optional[Dict[str, Any]] = None) -> ResultResponse:
        return send_results(self._results, settings)

    @abstractmethod
    def __call__(self, *args, **kwargs) -> ResultResponse | JsonRPCAction:
        pass
