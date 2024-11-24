# -*- encoding: utf-8 -*-
import errno
import gzip
import logging.handlers
import os
import shutil
import sys
import time
from datetime import datetime, timedelta


def get_stream_handler(
    level: int,
    formatter: logging.Formatter,
) -> logging.StreamHandler:

    stream_hdlr = logging.StreamHandler()
    stream_hdlr.setFormatter(formatter)
    stream_hdlr.setLevel(level)
    return stream_hdlr


def get_logger_and_formatter(
    name: str,
     datefmt: str,
     show_location: bool,
     utc: bool,
) -> [logging.Logger, logging.Formatter]:

    logger = logging.getLogger(name)
    for handler in logger.handlers[:]:
        logger.removeHandler(handler)

    formatt = get_format(show_location, name)
    formatter = logging.Formatter(formatt, datefmt=datefmt)
    if utc:
        formatter.converter = time.gmtime
    return logger, formatter


def check_filename_instance(filenames: list | tuple) -> None:
    if not isinstance(filenames, list | tuple):
        err_msg = (
            "Unable to parse filenames. "
            "Filename instance is not list or tuple. | "
            f"{filenames}"
        )
        write_stderr(err_msg)
        raise TypeError(err_msg)


def check_directory_permissions(directory_path: str) -> None:
    if os.path.isdir(directory_path) and not os.access(directory_path, os.R_OK | os.W_OK | os.X_OK):
        write_stderr(f"Unable to access directory | {directory_path}")
        raise OSError(errno.EACCES)

    try:
        if not os.path.isdir(directory_path):
            os.makedirs(directory_path, mode=0o755, exist_ok=True)
    except OSError as e:
        err_msg = f"Unable to create directory | {directory_path}"
        write_stderr(f"{err_msg} | {repr(e)}")
        raise e


def remove_old_logs(logs_dir: str, days_to_keep: int) -> None:
    files_list = list_files(logs_dir, ends_with=".gz")
    for file in files_list:
        try:
            if is_older_than_x_days(file, days_to_keep):
                delete_file(file)
        except Exception as e:
            write_stderr(
                f"Unable to delete passed {days_to_keep} days logs | "
                f"{file} | "
                f"{repr(e)}"
            )


def list_files(directory: str, ends_with: str) -> tuple:
    """
    List all files in the given directory and returns them in a list sorted by creation time in ascending order
    :param directory:
    :param ends_with:
    :return: tuple
    """

    try:
        result: list = []
        if os.path.isdir(directory):
            result: list = [os.path.join(directory, f) for f in os.listdir(directory) if
                            f.lower().endswith(ends_with)]
            result.sort(key=os.path.getmtime)
        return tuple(result)
    except Exception as e:
        write_stderr(repr(e))
        raise e


def delete_file(path: str) -> bool:
    """
    Remove the given file and returns True if the file was successfully removed
    :param path:
    :return: True
    """
    try:
        if os.path.isfile(path):
            os.remove(path)
        elif os.path.exists(path):
            shutil.rmtree(path)
        else:
            raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)
    except OSError as e:
        write_stderr(repr(e))
        raise e
    return True


def is_older_than_x_days(path: str, days: int) -> bool:
    """
    Check if a file or directory is older than the specified number of days
    :param path:
    :param days:
    :return:
    """

    if not os.path.exists(path):
        raise FileNotFoundError(errno.ENOENT, os.strerror(errno.ENOENT), path)

    try:
        if int(days) in (0, 1):
            cutoff_time = datetime.today()
        else:
            cutoff_time = datetime.today() - timedelta(days=int(days))
    except ValueError as e:
        write_stderr(repr(e))
        raise e

    file_timestamp = os.stat(path).st_mtime
    file_time = datetime.fromtimestamp(file_timestamp)

    if file_time < cutoff_time:
        return True
    return False


def write_stderr(msg: str) -> None:
    """
    Write msg to stderr
    :param msg:
    :return: None
    """

    dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    sys.stderr.write(f"[{dt}]:[ERROR]:{msg}\n")


def write_stdout(msg: str) -> None:
    """
    Write msg to stdout
    :param msg:
    :return: None
    """

    dt = datetime.now().strftime("%Y-%m-%dT%H:%M:%S.%f")[:-3]
    sys.stdout.write(f"[{dt}]:[WARNING]:{msg}\n")


def get_level(level: str) -> logging:
    """
    Get logging level
    :param level:
    :return: level
    """

    if not isinstance(level, str):
        write_stderr(
            "Unable to get log level. "
            "Setting default level to: 'INFO' "
            f"({logging.INFO})")
        return logging.INFO

    match level.lower():
        case "debug":
            return logging.DEBUG
        case "warning" | "warn":
            return logging.WARNING
        case "error":
            return logging.ERROR
        case "critical" | "crit":
            return logging.CRITICAL
        case _:
            return logging.INFO


def get_log_path(directory: str, filename: str) -> str:
    """
    Get log file path
    :param directory:
    :param filename:
    :return: path as str
    """

    log_file_path = str(os.path.join(directory, filename))

    try:
        open(log_file_path, "a+").close()
    except IOError as e:
        write_stderr(f"Unable to open log file for writing | {log_file_path} | {repr(e)}")
        raise e

    # try:
    #     if os.path.isfile(log_file_path):
    #         os.chmod(log_file_path , 0o755)
    # except OSError as e:
    #     write_stderr(f"Unable to set log file permissions | {repr(e)} | {log_file_path}")
    #     raise e

    return log_file_path


def get_format(show_location: bool, name: str | None) -> str:
    _debug_fmt = ""
    _logger_name = ""

    if name:
        _logger_name = f"[{name}]:"

    if show_location:
        _debug_fmt = "[%(filename)s:%(funcName)s:%(lineno)d]:"

    fmt = f"[%(asctime)s.%(msecs)03d]:[%(levelname)s]:{_logger_name}{_debug_fmt}%(message)s"
    return fmt


def gzip_file(source, output_partial_name) -> gzip:
    """
    gzip file
    :param source:
    :param output_partial_name:
    :return: gzip
    """

    if os.path.isfile(source) and os.stat(source).st_size > 0:
        sfname, sext = os.path.splitext(source)
        renamed_dst = f"{sfname}_{output_partial_name}{sext}.gz"

        try:
            with open(source, "rb") as fin:
                with gzip.open(renamed_dst, "wb") as fout:
                    fout.writelines(fin)
        except Exception as e:
            write_stderr(f"Unable to zip log file | {source} | {repr(e)}")
            raise e

        # try:
        #     if os.path.isfile(renamed_dst):
        #         os.chmod(renamed_dst , 0o755)
        # except OSError as e:
        #     write_stderr(f"Unable to set log file permissions | {repr(e)} | {renamed_dst}")
        #     raise e

        try:
            delete_file(source)
        except OSError as e:
            write_stderr(f"Unable to delete_file old source log file | {source} | {repr(e)}")
            raise e
