import time
from enum import Enum
import datetime
class LogType(Enum):
    DEBUG = "DEBUG"
    INFO = "INFO"
    WARNING = "WARNING"
    ERROR = "ERROR"




class Logger:
    def __init__(self, name: str, defaultLogType: LogType = LogType.INFO):
        self._defaultLogType = defaultLogType
        self._LOG_NAME = f"{name}_{ time.time() }.botlog"
        print(f"Logfile location: {self._LOG_NAME}")
        open(self._LOG_NAME, "w").close()

    def print(self, content: str, logType: LogType | None = None):
        if logType is None: logType = self._defaultLogType
        log = f"[{logType.value} {time.time()}] {content}"
        print(log)
        with open(self._LOG_NAME, "a", encoding="utf-8") as f:
            f.write(log)
            f.write("\n")



