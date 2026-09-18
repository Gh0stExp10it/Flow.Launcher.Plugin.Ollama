from __future__ import annotations


class Command(dict):
    """An inert Flow Launcher action (Method + Parameters).

    Built by ``pyflowlauncher.api`` builders. Subclasses ``dict`` so it
    serializes directly to the JsonRPCAction shape and compares equal to the
    plain dict, while remaining distinguishable via ``isinstance`` for
    ``Result.add_action`` and the response collectors.
    """
