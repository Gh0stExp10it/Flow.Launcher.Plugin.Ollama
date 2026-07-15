from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import sys
from typing import Any, Callable, Dict, Iterable, List, Optional, Union, cast

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

from .types import Method
from .models.result import Glyph, PreviewInfo
from .models.json_rpc import JsonRPCResult, JsonRPCRequest, JsonRPCResponse


class MethodNotRegisteredError(Exception):
    """Exception raised when trying to add an action with a method that is not registered as a plugin method."""

    def __init__(self, method: Callable[..., Any]):
        self.method = method
        super().__init__(
            f"Method {method.__name__} is not registered as a plugin method. "
            "Please use the @plugin.on_method decorator to register it."
        )


@dataclass
class Result:
    title: str
    subtitle: Optional[str] = None
    icon: Optional[Union[str, Path]] = None
    score: int = 0
    json_rpc_action: Optional[JsonRPCRequest] = None
    context_data: Optional[Iterable] = None
    glyph: Optional[Glyph] = None
    copy_text: Optional[str] = None
    auto_complete_text: Optional[str] = None
    rounded_icon: bool = False
    preview: Optional[PreviewInfo] = None
    title_highlight_data: Optional[List[int]] = None

    def add_action(
        self, method: Method, parameters: Optional[Iterable[Any]] = None, dont_hide_after_action: bool = False
    ) -> Self:
        """Adds a JsonRPC action to the result."""
        if not getattr(method, '_is_registered_method', False):
            raise MethodNotRegisteredError(method)
        self.json_rpc_action = {
            'Method': method.__name__,
            'Parameters': list(parameters) if parameters else [],
            'DontHideAfterAction': dont_hide_after_action,
        }
        return self

    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__

    @staticmethod
    def from_json(json_result: JsonRPCResult) -> Result:
        """Creates a Result instance from a JsonRPCResult dictionary."""
        if 'Title' not in json_result:
            raise ValueError("JsonRPCResult must have a 'Title' field")
        return Result(
            title=json_result['Title'],
            subtitle=json_result.get('SubTitle'),
            icon=json_result.get('IcoPath'),
            score=json_result.get('Score', 0),
            json_rpc_action=json_result.get('JsonRPCAction'),
            context_data=json_result.get('ContextData'),
            glyph=json_result.get('Glyph'),
            copy_text=json_result.get('CopyText'),
            auto_complete_text=json_result.get('AutoCompleteText'),
            rounded_icon=json_result.get('RoundedIcon', False),
            preview=json_result.get('Preview'),
            title_highlight_data=list(json_result.get('TitleHighlightData', []))
        )

    def to_json(self) -> JsonRPCResult:
        """Converts the Result instance to a JsonRPCResult dictionary"""
        return cast(JsonRPCResult, {
            'Title': self.title,
            'SubTitle': self.subtitle,
            'IcoPath': str(self.icon) if self.icon else None,
            'Score': self.score,
            'JsonRPCAction': self.json_rpc_action,
            'ContextData': self.context_data,
            'Glyph': self.glyph,
            'CopyText': self.copy_text,
            'AutoCompleteText': self.auto_complete_text,
            'RoundedIcon': self.rounded_icon,
            'Preview': self.preview,
            'TitleHighlightData': self.title_highlight_data,
        })


def send_results(results: Iterable[Result], settings: Optional[Dict[str, Any]] = None) -> JsonRPCResponse:
    """Formats and returns results as a JsonRPCResponse"""
    return {'Result': [result.to_json() for result in results], 'SettingsChange': settings}
