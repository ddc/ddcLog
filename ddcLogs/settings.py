# -*- encoding: utf-8 -*-
from enum import Enum
from dotenv import load_dotenv
from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional


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
    load_dotenv()

    level: Optional[LogLevel] = Field(default=LogLevel.INFO)
    name: Optional[str] = Field(default="app")
    directory: Optional[str] = Field(default="/app/logs")
    filename: Optional[str] = Field(default="app.log")
    encoding: Optional[str] = Field(default="UTF-8")
    date_format: Optional[str] = Field(default="%Y-%m-%dT%H:%M:%S")
    days_to_keep: Optional[int] = Field(default=14)
    utc: Optional[bool] = Field(default=True)
    stream_handler: Optional[bool] = Field(default=True) # Add stream handler along with file handler
    show_location: Optional[bool] = Field(default=False) # This will show the filename and the line number where the message originated

    # SizeRotatingLog
    max_file_size_mb: Optional[int] = Field(default=10)

    # TimedRotatingLog
    rotating_when: Optional[str] = Field(default="midnight")
    rotating_file_sufix: Optional[str] = Field(default="%Y%m%d")

    model_config = SettingsConfigDict(env_prefix="LOG_", env_file=".env", extra="allow")
