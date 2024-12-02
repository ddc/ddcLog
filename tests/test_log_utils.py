# -*- encoding: utf-8 -*-
import os
import tempfile
from datetime import datetime
from ddcLogs import BasicLog, SizeRotatingLog, TimedRotatingLog
from ddcLogs.log_utils import delete_file


class TestLogs:
    @classmethod
    def setup_class(cls):
        pass

    @classmethod
    def teardown_class(cls):
        pass
