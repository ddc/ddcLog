# -*- encoding: utf-8 -*-
import logging.handlers
import os
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


class TimedRotatingLog:
    def __init__(
        self,
        level: str = None,
        name: str = None,
        directory: str = None,
        filenames: list | tuple = None,
        encoding: str = None,
        datefmt: str = None,
        days_to_keep: int = None,
        utc: bool = None,
        stream_handler: bool = None,
        show_location: bool = None,
        sufix: str =  None,
        when: str = None,

    ):
        _settings = LogSettings()
        self.level = get_level(_settings.level if not level else level)
        self.name = _settings.name if not name else name
        self.directory = _settings.directory if not directory else directory
        self.filenames = (_settings.filename,) if not filenames else filenames
        self.encoding = _settings.encoding if not encoding else encoding
        self.datefmt = _settings.date_format if not datefmt else datefmt
        self.days_to_keep = int(_settings.days_to_keep) if not days_to_keep else int(days_to_keep)
        self.utc = _settings.utc if not utc else utc
        self.stream_handler = _settings.stream_handler if not stream_handler else stream_handler
        self.show_location = _settings.show_location if not show_location else show_location
        self.sufix = _settings.rotating_file_sufix if not sufix else sufix
        self.when = _settings.rotating_when if not when else when

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

        # supress logging from azure libraries (noisy)
        logging.getLogger("azure.eventhub").setLevel(logging.WARNING)
        logging.getLogger("azure.core").setLevel(logging.WARNING)

        return logger


class GZipRotatorTimed:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.dir = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        remove_old_logs(self.dir, self.days_to_keep)
        output_dated_name = os.path.splitext(dest)[1].replace(".", "")
        gzip_file(source, output_dated_name)
