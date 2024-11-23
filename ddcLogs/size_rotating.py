# -*- encoding: utf-8 -*-
import logging.handlers
import os
from .log_utils import (
    check_directory_permissions,
    check_filename_instance,
    get_exception,
    get_level,
    get_log_path,
    get_logger_and_formatter,
    get_stream_handler,
    gzip_file,
    list_files,
    remove_old_logs,
    write_stderr
)
from .settings import LogSettings


class SizeRotatingLog:
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
        max_mbytes: int = None,

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
        self.max_mbytes = int(_settings.max_file_size_mb) if not max_mbytes else int(max_mbytes)

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

            file_handler = logging.handlers.RotatingFileHandler(
                filename=log_file_path,
                mode="a",
                maxBytes=self.max_mbytes * 1024 * 1024,
                backupCount=self.days_to_keep,
                encoding=self.encoding,
                delay=False,
                errors=None
            )
            file_handler.rotator = GZipRotatorSize(
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


class GZipRotatorSize:
    def __init__(self, dir_logs: str, days_to_keep: int):
        self.directory = dir_logs
        self.days_to_keep = days_to_keep

    def __call__(self, source: str, dest: str) -> None:
        remove_old_logs(self.directory, self.days_to_keep)
        if os.path.isfile(source) and os.stat(source).st_size > 0:
            source_filename, _ = os.path.basename(source).split(".")
            new_file_number = 1
            previous_gz_files = list_files(self.directory, ends_with=".gz")
            for gz_file in previous_gz_files:
                if source_filename in gz_file:
                    try:
                        oldest_file_name = gz_file.split(".")[0].split("_")
                        if len(oldest_file_name) > 1:
                            new_file_number = int(oldest_file_name[1]) + 1
                    except ValueError as e:
                        write_stderr(
                            "Unable to get previous gz log file number | "
                            f"{gz_file} | "
                            f"{get_exception(e)}"
                        )
                        raise

            if os.path.isfile(source):
                gzip_file(source, new_file_number)
