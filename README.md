# Easy logs with rotations

[![License](https://img.shields.io/github/license/ddc/ddcLogs.svg)](https://github.com/ddc/ddcLogs/blob/master/LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org)
[![PyPi](https://img.shields.io/pypi/v/ddcLogs.svg)](https://pypi.python.org/pypi/ddcLogs)
[![PyPI Downloads](https://static.pepy.tech/badge/ddcLogs)](https://pepy.tech/projects/ddclogs)
[![Build Status](https://img.shields.io/endpoint.svg?url=https%3A//actions-badge.atrox.dev/ddc/ddcLogs/badge?ref=main&style=plastic&label=build&logo=none)](https://actions-badge.atrox.dev/ddc/ddcLogs/goto?ref=main)



# Logs
+ Parameters for all classes are declared as OPTIONAL 
+ If any [.env](./ddcLogs/.env.example) variable is omitted, it falls back to default values here: [settings.py](ddcLogs/settings.py)
+ Timezone parameter can also accept `localtime`, default to `UTC`
  + This parameter is only to display the timezone datetime inside the log file
  + For timed rotation, only UTC and localtime are supported, meaning it will rotate at UTC or localtime
    + env variable to change between UTC and localtime is `LOG_ROLL_OVER_AT_UTC` and default to True



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
    appname = "app",
    encoding = "UTF-8",
    datefmt = "%Y-%m-%dT%H:%M:%S",
    timezone = "America/Sao_Paulo",
    showlocation = False, # This will show the filename and the line number where the message originated
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
    level = "debug",
    appname = "app",
    directory = "/.logs",
    filenames = ["main.log", "app1.log"],
    maxmbytes = 5,
    daystokeep = 7,
    encoding = "UTF-8",
    datefmt = "%Y-%m-%dT%H:%M:%S",
    timezone = "America/Chicago",
    streamhandler = True, # Add stream handler along with file handler
    showlocation = False # This will show the filename and the line number where the message originated
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
    level = "debug",
    appname = "app",
    directory = "./logs",
    filenames = ["main.log", "app2.log"],
    when = "midnight",
    sufix = "%Y%m%d",
    daystokeep = 7,
    encoding = "UTF-8",
    datefmt = "%Y-%m-%dT%H:%M:%S",
    timezone = "UTC",
    streamhandler = True, # Add stream handler along with file handler
    showlocation = False # This will show the filename and the line number where the message originated
).init()
logger.warning("This is a warning example")
```
#### Example of output
`[2024-10-08T19:08:56.918-0000]:[WARNING]:[app]:This is a warning example`




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
