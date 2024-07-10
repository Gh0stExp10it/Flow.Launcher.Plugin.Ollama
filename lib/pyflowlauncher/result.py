from __future__ import annotations

import sys
from dataclasses import dataclass
from pathlib import Path
from typing import TYPE_CHECKING, Any, Dict, Iterable, List, Optional, Union

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict


if TYPE_CHECKING:
    from .plugin import Method


class JsonRPCAction(TypedDict):
    """Flow Launcher JsonRPCAction"""
    method: str
    parameters: Iterable
    dontHideAfterAction: NotRequired[bool]


class Glyph(TypedDict):
    """Flow Launcher Glyph"""
    Glyph: str
    FontFamily: str


class PreviewInfo(TypedDict):
    """Flow Launcher Preview section"""
    PreviewImagePath: Optional[str]
    Description: Optional[str]
    IsMedia: bool
    PreviewDeligate: Optional[str]


@dataclass
class Result:
    Title: str
    SubTitle: Optional[str] = None
    IcoPath: Optional[Union[str, Path]] = None
    Score: int = 0
    JsonRPCAction: Optional[JsonRPCAction] = None
    ContextData: Optional[Iterable] = None
    Glyph: Optional[Glyph] = None
    CopyText: Optional[str] = None
    AutoCompleteText: Optional[str] = None
    RoundedIcon: bool = False
    Preview: Optional[PreviewInfo] = None
    TitleHighlightData: Optional[List[int]] = None

    def as_dict(self) -> Dict[str, Any]:
        return self.__dict__

    def add_action(self, method: Method,
                   parameters: Optional[Iterable[Any]] = None,
                   *,
                   dont_hide_after_action: bool = False) -> None:
        self.JsonRPCAction = {
            "method": method.__name__,
            "parameters": parameters or [],
            "dontHideAfterAction": dont_hide_after_action
        }


class ResultResponse(TypedDict):
    result: List[Dict[str, Any]]
    SettingsChange: NotRequired[Optional[Dict[str, Any]]]


def send_results(results: Iterable[Result], settings: Optional[Dict[str, Any]] = None) -> ResultResponse:
    """Formats and returns results as a JsonRPCResponse"""
    return {'result': [result.as_dict() for result in results], 'SettingsChange': settings}
