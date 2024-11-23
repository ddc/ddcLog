# -*- encoding: utf-8 -*-
import logging.handlers
import os
from dotenv import load_dotenv
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_level,
    get_log_path,
    get_logger_and_formatter,
    get_stream_handler,
    gzip_file,
    remove_old_logs
)
from .settings import LogSettings


load_dotenv()
settings = LogSettings()


class TimedRotatingLog:
    def __init__(
        self,
        level: str = settings.level,
        name: str = settings.name,
        directory: str = settings.directory,
        filenames: list | tuple = (settings.filename,),
        encoding: str = settings.encoding,
        datefmt: str = settings.date_format,
        days_to_keep: int = int(settings.days_to_keep),
        utc: bool = settings.utc,
        stream_handler: bool = settings.stream_handler,
        show_location: bool = settings.show_location,
        sufix: str =  settings.rotating_file_sufix,
        when: str = settings.rotating_when,
    ):
        self.level = get_level(level)
        self.name = name
        self.directory = directory
        self.filenames = filenames
        self.encoding = encoding
        self.datefmt = datefmt
        self.days_to_keep = days_to_keep
        self.utc = utc
        self.stream_handler = stream_handler
        self.show_location = show_location
        self.sufix = sufix
        self.when = when

    def init(self):
        check_filename_instance(self.filenames)
        check_directory_permissions(self.directory)

        logger, formatter = get_logger_and_formatter(self.name,
                                                     self.datefmt,
                                                     self.show_location,
                                                     self.utc)
        logger.setLevel(self.level)

        for file in self.filenames:
            log_file_path = get_log_path(self.directory, file)

            file_handler = logging.handlers.TimedRotatingFileHandler(
                filename=log_file_path,
                encoding=self.encoding,
                when=self.when,
                utc=self.utc,
                backupCount=self.days_to_keep
            )
            file_handler.suffix = self.sufix
            file_handler.rotator = GZipRotatorTimed(
                self.directory,
                self.days_to_keep
            )
            file_handler.setFormatter(formatter)
            file_handler.setLevel(self.level)
            logger.addHandler(file_handler)

        if self.stream_handler:
            stream_hdlr = get_stream_handler(self.level, formatter)
            logger.addHandler(stream_hdlr)

        return logger


class GZipRotatorTimed:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        remove_old_logs(self.dir, self.days_to_keep)
        output_dated_name = os.path.splitext(dest)[1].replace(".", "")
        gzip_file(source, output_dated_name)
