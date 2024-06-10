# -*- encoding: utf-8 -*-
import os
import tempfile
from datetime import datetime
from ddcLogs import SizeRotatingLog, TimedRotatingLog
from ddcLogs.log_utils import remove


class TestLogs:
    @classmethod
    def setup_class(cls):
        cls.level = "debug"
        cls.directory = tempfile.gettempdir()
        cls.filename = "test.log"
        cls.file_path = os.path.join(cls.directory, cls.filename)

    @classmethod
    def teardown_class(cls):
        remove(str(os.path.join(cls.directory, cls.filename)))

    def test_timed_rotating_log(self):
        year = 2020
        month = 10
        day = 10

        log = TimedRotatingLog(directory=self.directory, level=self.level, filename=self.filename).init()
        log.debug("start")
        epoch_times = datetime(year, month, day, 1, 1, 1).timestamp()
        os.utime(self.file_path, (epoch_times, epoch_times))

        log = TimedRotatingLog(directory=self.directory, level=self.level, filename=self.filename).init()
        log.debug("end")
        gz_file_name = f"{os.path.splitext(self.filename)[0]}_{year}{month}{day}.log.gz"
        gz_file_path = os.path.join(tempfile.gettempdir(), gz_file_name)
        assert os.path.exists(gz_file_path)
        remove(str(gz_file_path))

    def test_sized_rotating_log(self):
        # creating file with 2MB
        with open(self.file_path, "wb") as f:
            f.seek((2 * 1024 * 1024) - 1)
            f.write(b"\0")

        max_mbytes = 1
        log = SizeRotatingLog(directory=self.directory,
                              level=self.level,
                              filename=self.filename,
                              max_mbytes=max_mbytes).init()
        log.debug("test")
        gz_file_name = f"{os.path.splitext(self.filename)[0]}_1.log.gz"
        gz_file_path = os.path.join(tempfile.gettempdir(), gz_file_name)
        assert os.path.exists(gz_file_path)
        remove(str(gz_file_path))
