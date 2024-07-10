from typing import Any, Dict
from .jsonrpc import JsonRPCClient


def settings() -> Dict[str, Any]:
    """Retrieve the settings from Flow Launcher."""
    return JsonRPCClient().recieve().get('settings', {})
