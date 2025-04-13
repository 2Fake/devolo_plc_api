# devolo PLC API

[![GitHub Workflow Status](https://img.shields.io/github/actions/workflow/status/2Fake/devolo_plc_api/pythonpackage.yml?branch=main)](https://github.com/2Fake/devolo_plc_api/actions?query=workflow%3A%22Python+package%22)
[![PyPI - Downloads](https://img.shields.io/pypi/dd/devolo-plc-api)](https://pypi.org/project/devolo-plc-api/)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/2Fake/devolo_plc_api)](https://codeclimate.com/github/2Fake/devolo_plc_api)
[![Coverage Status](https://coveralls.io/repos/github/2Fake/devolo_plc_api/badge.svg?branch=development)](https://coveralls.io/github/2Fake/devolo_plc_api?branch=development)

This project implements parts of the devolo PLC devices API in Python. Communication to the devices is formatted in protobuf and the IDLs were kindly provided by devolo. Nevertheless, we might miss updates to the IDLs. If you discover a breakage, please feel free to [report an issue](https://github.com/2Fake/devolo_plc_api/issues).

## System requirements

Defining the system requirements with exact versions typically is difficult. But there is a tested environment:

* Linux
* Python 3.9.22
* pip 25.0.1
* ifaddr 0.2.0
* httpx 0.28.1
* protobuf 5.28.3
* segno 1.6.1
* tenacity 9.0.0
* zeroconf 0.146.1

Other versions and even other operating systems might work. Feel free to tell us about your experience. If you want to run our unit tests, you also need:

* pytest 7.4.4
* pytest-asyncio 0.26.0
* pytest-httpx 0.35.0
* syrupy 4.9.1

## Versioning

In our versioning we follow [Semantic Versioning](https://semver.org/).

## Installing for usage

The Python Package Index takes care for you. Just use pip.

```bash
pip install devolo-plc-api
```

## Installing for development

First, you need to get the sources.

```bash
git clone git@github.com:2Fake/devolo_plc_api.git
```

Then you need to take care of the requirements.

```bash
cd devolo_plc_api
python setup.py install
```

If you want to run out tests, install the extra requirements and start pytest.

```bash
pip install -e .[test]
pytest
```

## Usage

All features we currently support on device basis are shown in our examples. If you want to use the package asynchronously, please check [example_async.py](https://github.com/2Fake/devolo_plc_api/blob/master/example_async.py). If you want to use it synchronously, please check [example_sync.py](https://github.com/2Fake/devolo_plc_api/blob/master/example_sync.py).

If you don't know the IP addresses of your devices, you can discover them. You will get a dictionary with the device's serial number as key. The connections to the devices will be already established, but you will have to take about disconnecting.

```python
from devolo_plc_api.network import async_discover_network

devices = await async_discover_network()
await asyncio.gather(*[device.async_connect() for device in _devices.values()])
# Do your magic
await asyncio.gather(*[device.async_disconnect() for device in devices.values()])
```

Or in a synchronous setup:

```python
from devolo_plc_api.network import discover_network

devices = discover_network()
for device in _devices.values():
        device.connect()
# Do your magic
[device.disconnect() for device in devices.values()]
```

## Supported device

The following devolo devices were queried with at least one call to verify functionality:

* Magic 2 WiFi next
* Magic 2 WiFi 2-1
* Magic 2 LAN triple
* Magic 2 DinRail
* Magic 2 LAN 1-1
* Magic 1 WiFi mini
* Magic 1 WiFi 2-1
* Magic 1 LAN 1-1
* Repeater 5400
* Repeater 3000
* Repeater 1200
* Repeater ac+
* Repeater ac
* dLAN 1200+ WiFi ac
* dLAN 550+ Wifi
* dLAN 550 WiFi

However, other devices might work, some might have a limited functionality. Also firmware version will matter. If you discover something weird, [we want to know](https://github.com/2Fake/devolo_plc_api/issues).
