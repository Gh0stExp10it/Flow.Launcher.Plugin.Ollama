from __future__ import annotations

import inspect
from typing import Any, Generator, Union

from .result import Result, send_results
from .models.json_rpc import JsonRPCRequest, JsonRPCResponse


def handle_response(result: Any) -> Union[JsonRPCResponse, JsonRPCRequest, None]:
    """Normalize a method's return value into a JSON-RPC response.

    Accepts: Result, list of Result, generator of Result/list, JsonRPCRequest,
    JsonRPCResponse, coroutine, async generator, or None.
    Coroutines and async generators are returned as-is for the event loop to handle.
    """
    if result is None:
        return None
    if isinstance(result, Result):
        return send_results([result])
    if isinstance(result, list):
        return send_results([r for r in result if isinstance(r, Result)])
    if inspect.isgenerator(result):
        return _collect_generator(result)
    return result


def _collect_item(item: Any) -> list[Result]:
    if isinstance(item, Result):
        return [item]
    if isinstance(item, list):
        return [r for r in item if isinstance(r, Result)]
    return []


def _collect_generator(gen: Generator) -> JsonRPCResponse:
    results = []
    for item in gen:
        results.extend(_collect_item(item))
    return send_results(results)
