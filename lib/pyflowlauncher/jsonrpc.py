from __future__ import annotations

import json
import sys
from typing import Any, Mapping

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict


class JsonRPCRequest(TypedDict):
    method: str
    parameters: list
    settings: NotRequired[dict[Any, Any]]


class JsonRPCClient:

    def send(self, data: Mapping) -> None:
        json.dump(data, sys.stdout)

    def recieve(self) -> JsonRPCRequest:
        try:
            return json.loads(sys.argv[1])
        except (IndexError, json.JSONDecodeError):
            return {'method': 'query', 'parameters': ['']}
