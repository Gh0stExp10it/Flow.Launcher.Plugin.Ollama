from typing import TypedDict, Literal

MANIFEST_FILE = 'plugin.json'

Languages = Literal[
    'Python',
    'CSharp',
    'FSharp',
    'Executable',
    'TypeScript',
    'JavaScript',
]


class PluginManifestSchema(TypedDict):
    ID: str
    ActionKeyword: str
    Name: str
    Description: str
    Author: str
    Version: str
    Language: Languages
    Website: str
    IcoPath: str
    ExecuteFileName: str
