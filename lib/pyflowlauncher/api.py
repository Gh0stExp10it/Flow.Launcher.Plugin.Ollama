from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional

from .models.json_rpc import JsonRPCRequest

if TYPE_CHECKING:
    from .string_matcher import MatchData

NAME_SPACE = 'Flow.Launcher'


def _send_action(method: str, *parameters) -> JsonRPCRequest:
    return {"Method": f"{NAME_SPACE}.{method}", "Parameters": list(parameters)}


def change_query(query: str, requery: bool = False) -> JsonRPCRequest:
    """Change the query in Flow Launcher."""
    return _send_action("ChangeQuery", query, requery)


def shell_run(command: str, filename: str = 'cmd.exe') -> JsonRPCRequest:
    """Run a shell command."""
    return _send_action("ShellRun", command, filename)


def close_app() -> JsonRPCRequest:
    """Close Flow Launcher."""
    return _send_action("CloseApp")


def hide_app() -> JsonRPCRequest:
    """Hide Flow Launcher."""
    return _send_action("HideApp")


def show_app() -> JsonRPCRequest:
    """Show Flow Launcher."""
    return _send_action("ShowApp")


def show_msg(title: str, sub_title: str, ico_path: str = "") -> JsonRPCRequest:
    """Show a message in Flow Launcher."""
    return _send_action("ShowMsg", title, sub_title, ico_path)


def open_setting_dialog() -> JsonRPCRequest:
    """Open the settings window in Flow Launcher."""
    return _send_action("OpenSettingDialog")


def start_loading_bar() -> JsonRPCRequest:
    """Start the loading bar in Flow Launcher."""
    return _send_action("StartLoadingBar")


def stop_loading_bar() -> JsonRPCRequest:
    """Stop the loading bar in Flow Launcher."""
    return _send_action("StopLoadingBar")


def reload_plugins() -> JsonRPCRequest:
    """Reload the plugins in Flow Launcher."""
    return _send_action("ReloadPlugins")


def copy_to_clipboard(text: str, direct_copy: bool = False, show_default_notification=True) -> JsonRPCRequest:
    """Copy text to the clipboard."""
    return _send_action("CopyToClipboard", text, direct_copy, show_default_notification)


def open_directory(directory_path: str, filename_or_filepath: Optional[str] = None) -> JsonRPCRequest:
    """Open a directory."""
    return _send_action("OpenDirectory", directory_path, filename_or_filepath)


def open_url(url: str, in_private: bool = False) -> JsonRPCRequest:
    """Open a URL."""
    return _send_action("OpenUrl", url, in_private)


def open_uri(uri: str) -> JsonRPCRequest:
    """Open a URI."""
    return _send_action("OpenAppUri", uri)


_FuzzySearchFn = Callable[[str, str], Coroutine[Any, Any, "MatchData"]]


class Api:
    """Flow Launcher API calls, accessible via plugin.launcher.api."""
    change_query = staticmethod(change_query)
    shell_run = staticmethod(shell_run)
    close_app = staticmethod(close_app)
    hide_app = staticmethod(hide_app)
    show_app = staticmethod(show_app)
    show_msg = staticmethod(show_msg)
    open_setting_dialog = staticmethod(open_setting_dialog)
    start_loading_bar = staticmethod(start_loading_bar)
    stop_loading_bar = staticmethod(stop_loading_bar)
    reload_plugins = staticmethod(reload_plugins)
    copy_to_clipboard = staticmethod(copy_to_clipboard)
    open_directory = staticmethod(open_directory)
    open_url = staticmethod(open_url)
    open_uri = staticmethod(open_uri)

    def __init__(self, fuzzy_search_fn: Optional[_FuzzySearchFn] = None) -> None:
        self._fuzzy_search_fn = fuzzy_search_fn

    async def fuzzy_search(self, query: str, text: str) -> MatchData:
        """Match query against text.

        On V2 delegates to Flow Launcher's own FuzzySearch over JSON-RPC so
        search precision settings are respected. On V1 falls back to the
        bundled Python string_matcher.
        """
        if self._fuzzy_search_fn is None:
            raise RuntimeError(
                "fuzzy_search is unavailable: this Api was created without a "
                "fuzzy_search_fn. Use the launcher-provided instance via "
                "plugin.launcher.api instead of constructing Api() directly."
            )
        return await self._fuzzy_search_fn(query, text)
