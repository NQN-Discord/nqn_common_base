from contextvars import ContextVar
from logging import Logger


class _LogHelper:
    def __init__(self):
        self._log = ContextVar("_global_log")

    @property
    def log(self) -> Logger:
        return self._log.get()

    @log.setter
    def log(self, logger: Logger):
        self._log.set(logger)


logger = _LogHelper()
