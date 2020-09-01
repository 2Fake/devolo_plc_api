# devolo PLC API

[![GitHub Workflow Status](https://img.shields.io/github/workflow/status/2Fake/devolo_plc_api/Python%20package)](https://github.com/2Fake/devolo_plc_api/actions?query=workflow%3A%22Python+package%22)
[![PyPI - Downloads](https://img.shields.io/pypi/dd/devolo-plc-api)](https://pypi.org/project/devolo-plc-api/)
[![Code Climate maintainability](https://img.shields.io/codeclimate/maintainability/2Fake/devolo_plc_api)](https://codeclimate.com/github/2Fake/devolo_plc_api)
[![Coverage Status](https://coveralls.io/repos/github/2Fake/devolo_plc_api/badge.svg?branch=development)](https://coveralls.io/github/2Fake/devolo_plc_api?branch=development)

This project implements parts of the devolo PLC devices API in Python. Communication to the devices is formatted in protobuf and the IDLs were kindly provided by devolo. Nevertheless, we might miss updates to the IDLs. If you discover a breakage, please feel free to [report an issue](https://github.com/2Fake/devolo_plc_api/issues).

## System requirements

Defining the system requirements with exact versions typically is difficult. But there is a tested environment:

* Linux
* Python 3.7.8
* pip 20.0.2
* httpx 0.14.2
* protobuf 3.11.4
* zeroconf 0.27.0

Other versions and even other operating systems might work. Feel free to tell us about your experience. If you want to run our unit tests, you also need:

* pytest 5.4.3
* pytest-asyncio 0.14.0
* pytest-mock 3.2.0
* asynctest 0.13.0

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

If you want to run out tests, change to the tests directory and start pytest via setup.py.

```bash
python setup.py test
```

## Usage

All features we currently support are shown in our examples. If you want to use the package asynchronously, please check [example_async.py](https://github.com/2Fake/devolo_plc_api/blob/master/example_async.py). If you want to use it synchronously, please check [example_sync.py](https://github.com/2Fake/devolo_plc_api/blob/master/example_sync.py).
