import sys
from typing import Any, Dict, List, Optional

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict

from .result import Result


class JsonRPCRequest(TypedDict):
    Method: str
    Parameters: List[str]
    DontHideAfterAction: NotRequired[bool]


class JsonRPCResponse(TypedDict):
    Result: List[Result]
    SettingsChange: NotRequired[Optional[Dict[str, Any]]]


class JsonRPCResult(Result):
    JsonRPCAction: NotRequired[JsonRPCRequest]
    SettingsChange: NotRequired[Dict[str, Any]]


class MatchResult(TypedDict, total=False):
    """Flow Launcher FuzzySearch response (camelCase keys from StreamJsonRpc)."""
    success: bool
    score: int
    rawScore: int
    matchData: List[int]
    searchPrecision: int
