# Easy logs with rotations

[![License](https://img.shields.io/pypi/l/ddclogs)](https://github.com/ddc/ddcLogs/blob/master/LICENSE)
[![Python](https://img.shields.io/pypi/pyversions/ddclogs.svg)](https://www.python.org)
[![PyPi](https://img.shields.io/pypi/v/ddcLogs.svg)](https://pypi.python.org/pypi/ddcLogs)
[![PyPI Downloads](https://static.pepy.tech/badge/ddcLogs)](https://pepy.tech/projects/ddclogs)
[![codecov](https://codecov.io/github/ddc/ddcLogs/graph/badge.svg?token=3MEPITZKYN)](https://codecov.io/github/ddc/ddcLogs)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcLogs/badge?ref=main&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcLogs/goto?ref=main)



# Logs
+ Parameters for all classes are declared as OPTIONAL 
+ If any [.env](./ddcLogs/.env.example) variable is omitted, it falls back to default values here: [settings.py](ddcLogs/settings.py)
+ timezone parameter can also accept `localtime`, default to `UTC`
  + This parameter is only to display the timezone datetime inside the log file
  + For timed rotation, only UTC and localtime are supported, meaning it will rotate at UTC or localtime
    + env variable to change between UTC and localtime is `LOG_ROTATE_AT_UTC` and default to True
+ streamhandler parameter will add stream handler along with file handler
+ showlocation parameter will show the filename and the line number where the message originated




# Install
```shell
pip install ddcLogs
```



# BasicLog
+ Setup Logging
     + This is just a basic log, it does not use any file
```python
from ddcLogs import BasicLog
logger = BasicLog(
    level="debug",
    name="app",
    encoding="UTF-8",
    datefmt="%Y-%m-%dT%H:%M:%S",
    timezone="America/Sao_Paulo",
    showlocation=False,
).init()
logger.warning("This is a warning example")
```
#### Example of output
`[2024-10-08T19:08:56.918-0300]:[WARNING]:[app]:This is a warning example`





# SizeRotatingLog
+ Setup Logging
    + Logs will rotate based on the file size using the `maxmbytes` variable
    + Rotated logs will have a sequence number starting from 1: `app.log_1.gz, app.log_2.gz`
    + Logs will be deleted based on the `daystokeep` variable, defaults to 30
```python
from ddcLogs import SizeRotatingLog
logger = SizeRotatingLog(
    level="debug",
    name="app",
    directory="/app/logs",
    filenames=["main.log", "app1.log"],
    maxmbytes=5,
    daystokeep=7,
    encoding="UTF-8",
    datefmt="%Y-%m-%dT%H:%M:%S",
    timezone="America/Chicago",
    streamhandler=True,
    showlocation=False
).init()
logger.warning("This is a warning example")
```
#### Example of output
`[2024-10-08T19:08:56.918-0500]:[WARNING]:[app]:This is a warning example`





# TimedRotatingLog
+ Setup Logging
    + Logs will rotate based on `when` variable to a `.gz` file, defaults to `midnight`
    + Rotated log will have the sufix variable on its name: `app_20240816.log.gz`
    + Logs will be deleted based on the `daystokeep` variable, defaults to 30
    + Current 'when' events supported:
        + midnight — roll over at midnight
        + W{0-6} - roll over on a certain day; 0 - Monday
```python
from ddcLogs import TimedRotatingLog
logger = TimedRotatingLog(
    level="debug",
    name="app",
    directory="/app/logs",
    filenames=["main.log", "app2.log"],
    when="midnight",
    sufix="%Y%m%d",
    daystokeep=7,
    encoding="UTF-8",
    datefmt="%Y-%m-%dT%H:%M:%S",
    timezone="UTC",
    streamhandler=True,
    showlocation=False
).init()
logger.warning("This is a warning example")
```
#### Example of output
`[2024-10-08T19:08:56.918-0000]:[WARNING]:[app]:This is a warning example`





## Env Variables
```
LOG_LEVEL=DEBUG
LOG_TIMEZONE=America/Chicago
LOG_ENCODING=UTF-8
LOG_APPNAME=app
LOG_FILENAME=app.log
LOG_DIRECTORY=/app/logs
LOG_DAYS_TO_KEEP=30
LOG_STREAM_HANDLER=True
LOG_SHOW_LOCATION=False
LOG_DATE_FORMAT=%Y-%m-%dT%H:%M:%S

# SizeRotatingLog
LOG_MAX_FILE_SIZE_MB=10

# TimedRotatingLog
LOG_ROTATE_WHEN=midnight
LOG_ROTATE_AT_UTC=True
LOG_ROTATE_FILE_SUFIX=%Y%m%d
```




# Source Code
### Build
```shell
poetry build -f wheel
```



# Run Tests and Get Coverage Report using Poe
```shell
poetry update --with test
poe tests
```



# License
Released under the [MIT License](LICENSE)




# Buy me a cup of coffee
+ [GitHub Sponsor](https://github.com/sponsors/ddc)
+ [ko-fi](https://ko-fi.com/ddcsta)
+ [Paypal](https://www.paypal.com/ncp/payment/6G9Z78QHUD4RJ)
