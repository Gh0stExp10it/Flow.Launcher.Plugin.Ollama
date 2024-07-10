import logging
import sys
from pathlib import Path
from typing import Any

_logger = logging.getLogger(__name__)


def logger(obj: Any) -> logging.Logger:
    module_file = sys.modules[obj.__module__].__file__
    if module_file is not None:
        module_name = Path(module_file).stem
        return logging.getLogger(f"{module_name}.{obj.__class__.__name__}")
    return logging.getLogger(f"{obj.__module__}.{obj.__name__}")
