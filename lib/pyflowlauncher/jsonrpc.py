from __future__ import annotations

import asyncio
import json
import logging
import sys
from typing import Any, Mapping, Optional

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict

_logger = logging.getLogger(__name__)


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


class JsonRPCV2Client:

    DEFAULT_REQUEST_TIMEOUT = 10.0

    def __init__(self) -> None:
        self._pending: dict = {}
        self._counter: int = 0

    async def messages(self):
        """Async generator yielding parsed JSON-RPC request dicts from stdin.

        Responses to plugin-initiated calls (no 'method' key) are routed to
        their waiting Future and not yielded.
        """
        loop = asyncio.get_running_loop()
        while True:
            line = await loop.run_in_executor(None, sys.stdin.readline)
            if not line:
                self._fail_pending(ConnectionError(
                    "JSON-RPC stream closed before a response arrived"))
                return
            line = line.strip()
            if not line:
                continue
            try:
                msg = json.loads(line)
            except json.JSONDecodeError:
                _logger.warning("Bad JSON-RPC line: %r", line)
                continue
            if 'method' not in msg:
                req_id = msg.get('id')
                fut = self._pending.pop(req_id, None)
                if fut is None:
                    _logger.warning(
                        "Discarding JSON-RPC response with unknown id: %r", req_id)
                elif not fut.done():
                    fut.set_result(msg.get('result'))
                continue
            yield msg

    def _fail_pending(self, exc: Exception) -> None:
        while self._pending:
            _, fut = self._pending.popitem()
            if not fut.done():
                fut.set_exception(exc)

    async def request(
        self, method: str, params: list,
        timeout: Optional[float] = DEFAULT_REQUEST_TIMEOUT,
    ) -> Any:
        """Send a JSON-RPC call to Flow Launcher and await the response.

        Raises asyncio.TimeoutError if no response arrives within `timeout`
        seconds, and ConnectionError if the stream closes first.
        """
        self._counter += 1
        req_id = self._counter
        fut: asyncio.Future = asyncio.get_running_loop().create_future()
        self._pending[req_id] = fut
        self.send({'id': req_id, 'method': method, 'params': params})
        try:
            return await asyncio.wait_for(fut, timeout)
        finally:
            self._pending.pop(req_id, None)

    def send(self, data: dict) -> None:
        sys.stdout.write(json.dumps(data) + '\n')
        sys.stdout.flush()
