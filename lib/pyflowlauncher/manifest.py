from __future__ import annotations

from dataclasses import dataclass, field
import json
from pathlib import Path
import sys

if sys.version_info < (3, 11):
    from typing_extensions import Self
else:
    from typing import Self

from .models.plugin_manifest import FILE_NAME, PluginMetadata


@dataclass
class Manifest:
    id: str
    name: str
    author: str
    version: str
    language: str
    description: str
    website: str
    execute_file_name: str
    ico_path: str
    action_keyword: str
    action_keywords: list[str] = field(default_factory=list)

    @classmethod
    def from_json(cls, json_data: PluginMetadata) -> Self:
        """Create a Manifest instance from a JSON dictionary."""
        return cls(
            id=json_data['ID'],
            name=json_data['Name'],
            author=json_data['Author'],
            version=json_data['Version'],
            language=json_data['Language'],
            description=json_data['Description'],
            website=json_data['Website'],
            execute_file_name=json_data['ExecuteFileName'],
            ico_path=json_data['IcoPath'],
            action_keyword=json_data['ActionKeyword'],
            action_keywords=json_data.get('ActionKeywords', []),
        )

    @classmethod
    def from_file(cls, path: Path) -> Self:
        """Load the manifest from a JSON file."""
        with open(path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return cls.from_json(data)

    @classmethod
    def from_dir(cls, dir_path: Path) -> Self:
        """Load the manifest from a directory containing a plugin.json file."""
        return cls.from_file(Path(dir_path) / FILE_NAME)

    def to_json(self) -> PluginMetadata:
        """Convert the manifest to a JSON-serializable dictionary."""
        return {
            "ID": self.id,
            "Name": self.name,
            "Author": self.author,
            "Version": self.version,
            "Language": self.language,
            "Description": self.description,
            "Website": self.website,
            "ExecuteFileName": self.execute_file_name,
            "IcoPath": self.ico_path,
            "ActionKeyword": self.action_keyword,
            "ActionKeywords": self.action_keywords,
        }

    def save(self, path: Path) -> None:
        """Save the manifest to a JSON file."""
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.to_json(), f, ensure_ascii=False, indent=4)
