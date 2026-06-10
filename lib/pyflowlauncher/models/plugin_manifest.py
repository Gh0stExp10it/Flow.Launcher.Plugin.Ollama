import sys
from typing import List

if sys.version_info < (3, 11):
    from typing_extensions import NotRequired, TypedDict
else:
    from typing import NotRequired, TypedDict


FILE_NAME = 'plugin.json'


class PluginMetadata(TypedDict):
    ID: str
    Name: str
    Author: str
    Version: str
    Language: str
    Description: str
    Website: str
    ExecuteFileName: str
    IcoPath: str
    ActionKeyword: str
    ActionKeywords: NotRequired[List[str]]
