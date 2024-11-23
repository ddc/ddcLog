# -*- encoding: utf-8 -*-
from enum import Enum
from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict


load_dotenv()


class LogLevel(str, Enum):
    """log levels"""

    CRITICAL = "CRITICAL"
    CRIT = "CRIT"
    ERROR = "ERROR"
    WARNING = "WARNING"
    WARN = "WARN"
    INFO = "INFO"
    DEBUG = "DEBUG"


class LogSettings(BaseSettings):
    """
    settings defined here with fallback to reading ENV variables
    Current 'rotating_when' events supported for TimedRotatingLogs:
        midnight - roll over at midnight
        W{0-6} - roll over on a certain day; 0 - Monday
    """

    level: LogLevel = LogLevel.INFO
    name: str = "app"
    directory: str = "/app/logs"
    filename: str = "app.log"
    encoding: str = "UTF-8"
    date_format: str = "%Y-%m-%dT%H:%M:%S"
    days_to_keep: int = 14
    utc: bool = True
    stream_handler: bool = True # Add stream handler along with file handler
    show_location: bool = False # This will show the filename and the line number where the message originated

    # SizeRotatingLog
    max_file_size_mb: int = 10

    # TimedRotatingLog
    rotating_when: str = "midnight"
    rotating_file_sufix: str = "%Y%m%d"

    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env", extra="allow")
