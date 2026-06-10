import logging


def _setup_file_logger() -> logging.Logger:
    log = logging.getLogger('pyflowlauncher')
    if not log.handlers:
        handler = logging.FileHandler('plugin.log')
        handler.setLevel(logging.WARNING)
        handler.setFormatter(logging.Formatter('%(asctime)s %(name)s %(levelname)s %(message)s'))
        log.addHandler(handler)
        log.setLevel(logging.WARNING)
        log.propagate = False
    return log


_setup_file_logger()


class pyFlowLauncherObject:
    """Base class for all pyFlowLauncher objects."""

    def __init__(self):
        self.logger = logging.getLogger(f'pyflowlauncher.{self.__class__.__name__}')
