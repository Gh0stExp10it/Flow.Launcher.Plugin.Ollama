from typing import Optional

from .result import JsonRPCAction

NAME_SPACE = 'Flow.Launcher'


def _send_action(method: str, *parameters) -> JsonRPCAction:
    return {"method": f"{NAME_SPACE}.{method}", "parameters": parameters}


def change_query(query: str, requery: bool = False) -> JsonRPCAction:
    """Change the query in Flow Launcher."""
    return _send_action("ChangeQuery", query, requery)


def shell_run(command: str, filename: str = 'cmd.exe') -> JsonRPCAction:
    """Run a shell command."""
    return _send_action("ShellRun", command, filename)


def close_app() -> JsonRPCAction:
    """Close Flow Launcher."""
    return _send_action("CloseApp")


def hide_app() -> JsonRPCAction:
    """Hide Flow Launcher."""
    return _send_action("HideApp")


def show_app() -> JsonRPCAction:
    """Show Flow Launcher."""
    return _send_action("ShowApp")


def show_msg(title: str, sub_title: str, ico_path: str = "") -> JsonRPCAction:
    """Show a message in Flow Launcher."""
    return _send_action("ShowMsg", title, sub_title, ico_path)


def open_setting_dialog() -> JsonRPCAction:
    """Open the settings window in Flow Launcher."""
    return _send_action("OpenSettingDialog")


def start_loading_bar() -> JsonRPCAction:
    """Start the loading bar in Flow Launcher."""
    return _send_action("StartLoadingBar")


def stop_loading_bar() -> JsonRPCAction:
    """Stop the loading bar in Flow Launcher."""
    return _send_action("StopLoadingBar")


def reload_plugins() -> JsonRPCAction:
    """Reload the plugins in Flow Launcher."""
    return _send_action("ReloadPlugins")


def copy_to_clipboard(text: str, direct_copy: bool = False, show_default_notification=True) -> JsonRPCAction:
    """Copy text to the clipboard."""
    return _send_action("CopyToClipboard", text, direct_copy, show_default_notification)


def open_directory(directory_path: str, filename_or_filepath: Optional[str] = None) -> JsonRPCAction:
    """Open a directory."""
    return _send_action("OpenDirectory", directory_path, filename_or_filepath)


def open_url(url: str, in_private: bool = False) -> JsonRPCAction:
    """Open a URL."""
    return _send_action("OpenUrl", url, in_private)


def open_uri(uri: str) -> JsonRPCAction:
    """Open a URI."""
    return _send_action("OpenAppUri", uri)
