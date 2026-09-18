from __future__ import annotations

from typing import TYPE_CHECKING, Any, Callable, Coroutine, Optional

from .command import Command

if TYPE_CHECKING:
    from .string_matcher import MatchData

NAME_SPACE = 'Flow.Launcher'


class NotSupportedError(Exception):
    """Raised when an operation is not supported by the active protocol version."""


def _send_action(method: str, *parameters) -> Command:
    return Command({"Method": f"{NAME_SPACE}.{method}", "Parameters": list(parameters)})


_FuzzySearchFn = Callable[[str, str], Coroutine[Any, Any, "MatchData"]]


class Api:
    """Flow Launcher API, accessible via ``plugin.launcher.api``.

    Builder methods return inert ``Command`` values; ``fuzzy_search`` and
    ``invoke`` are the launcher-bound calls.
    """

    def __init__(
        self,
        fuzzy_search_fn: Optional[_FuzzySearchFn] = None,
        invoke_fn: Optional[Callable[["Command"], Coroutine[Any, Any, Any]]] = None,
    ) -> None:
        self._fuzzy_search_fn = fuzzy_search_fn
        self._invoke_fn = invoke_fn

    def change_query(self, query: str, requery: bool = False) -> Command:
        """Change the query in Flow Launcher."""
        return _send_action("ChangeQuery", query, requery)

    def shell_run(self, command: str, filename: str = 'cmd.exe') -> Command:
        """Run a shell command."""
        return _send_action("ShellRun", command, filename)

    def close_app(self) -> Command:
        """Close Flow Launcher."""
        return _send_action("CloseApp")

    def hide_app(self) -> Command:
        """Hide Flow Launcher."""
        return _send_action("HideApp")

    def show_app(self) -> Command:
        """Show Flow Launcher."""
        return _send_action("ShowApp")

    def show_msg(self, title: str, sub_title: str, ico_path: str = "") -> Command:
        """Show a message in Flow Launcher."""
        return _send_action("ShowMsg", title, sub_title, ico_path)

    def open_setting_dialog(self) -> Command:
        """Open the settings window in Flow Launcher."""
        return _send_action("OpenSettingDialog")

    def start_loading_bar(self) -> Command:
        """Start the loading bar in Flow Launcher."""
        return _send_action("StartLoadingBar")

    def stop_loading_bar(self) -> Command:
        """Stop the loading bar in Flow Launcher."""
        return _send_action("StopLoadingBar")

    def reload_plugins(self) -> Command:
        """Reload the plugins in Flow Launcher."""
        return _send_action("ReloadPlugins")

    def copy_to_clipboard(self, text: str, direct_copy: bool = False,
                          show_default_notification: bool = True) -> Command:
        """Copy text to the clipboard."""
        return _send_action("CopyToClipboard", text, direct_copy, show_default_notification)

    def open_directory(self, directory_path: str,
                       filename_or_filepath: Optional[str] = None) -> Command:
        """Open a directory."""
        return _send_action("OpenDirectory", directory_path, filename_or_filepath)

    def open_url(self, url: str, in_private: bool = False) -> Command:
        """Open a URL."""
        return _send_action("OpenUrl", url, in_private)

    def open_uri(self, uri: str) -> Command:
        """Open a URI."""
        return _send_action("OpenAppUri", uri)

    async def fuzzy_search(self, query: str, text: str) -> "MatchData":
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

    async def invoke(self, command: Command) -> Any:
        """Send a command to Flow Launcher now and return its response.

        Supported on Flow Launcher V2 only; on V1 the launcher-provided
        ``invoke_fn`` raises ``NotSupportedError``.
        """
        if self._invoke_fn is None:
            raise RuntimeError(
                "invoke is unavailable: this Api was created without an "
                "invoke_fn. Use the launcher-provided instance via "
                "plugin.launcher.api instead of constructing Api() directly."
            )
        return await self._invoke_fn(command)


# Backwards-compatible module-level builders (pyflowlauncher.api.change_query, ...).
# Bound to a default Api instance; builders are pure and ignore instance state.
_default_api = Api()
change_query = _default_api.change_query
shell_run = _default_api.shell_run
close_app = _default_api.close_app
hide_app = _default_api.hide_app
show_app = _default_api.show_app
show_msg = _default_api.show_msg
open_setting_dialog = _default_api.open_setting_dialog
start_loading_bar = _default_api.start_loading_bar
stop_loading_bar = _default_api.stop_loading_bar
reload_plugins = _default_api.reload_plugins
copy_to_clipboard = _default_api.copy_to_clipboard
open_directory = _default_api.open_directory
open_url = _default_api.open_url
open_uri = _default_api.open_uri
