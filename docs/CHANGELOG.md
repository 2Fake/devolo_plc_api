# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [v1.5.0] - 2025/04/13

### Added

- Retry mechanism for timed-out connections
- Use SPDX license identifier for project metadata

### Changed

- Drop support for Python 3.8

## [v1.4.1] - 2023/09/14

### Fixed

- Increase timeout of async_check_firmware_available to handle unknown errors gracefully

## [v1.4.0] - 2023/07/26

### Added

- Generate QR codes from wifi guest settings
- Make use of zeroconf unicast requests to be able to respond across subnets

## [v1.3.2] - 2023/07/13

### Fixed

- Frequently connecting to an offline device lead to a memory leak

## [v1.3.1] - 2023/05/12

### Fixed

- Reduce zeroconf traffic

## [v1.3.0] - 2023/04/13

### Added

- Get MultiAP information from the device

### Fixed

- The event loop got closed to early when disconnecting from a device synchronously.

## [v1.2.0] - 2023/02/17

### Added

- Support for devices with password protected PLCNET API

## [v1.1.0] - 2023/01/24

### Added

- Get support information from the device

## [v1.0.0] - 2023/01/05

### Changed

- **BREAKING**: The results are now dataclass-like objects. Please have a look at our [examples](https://github.com/2Fake/devolo_plc_api/blob/dee4617da680685a35ac48051d1aecd0456b7764/example_async.py) to see, how migration works.

## [v0.9.0] - 2022/12/20

### Added

- Handle updates sent via mDNS

## [v0.8.1] - 2022/10/18

### Fixed

- Use correct device password if password was set before connecting to it

## [v0.8.0] - 2022/05/06

### Added

#### Device API

- Specify a duration for the guest wifi
- Start WPS clone mode
- Factory reset device

#### PLCNET API

- Start pairing mode

## [v0.7.1] - 2022/01/10

### Fixed

- Get LED status from devices

## [v0.7.0] - 2021/11/30

### Added

#### Device API

- Restart device
- Query uptime as strict monotonically increasing number

### Fixed

- Connecting to multiple devices at the same time works again
- Zeroconf Browsers terminate correctly in case a device does not answer
- Accessing password protected LAN devices works again

## [v0.6.4] - 2021/11/24

### Fixed

- Running tasks get cleanly canceled on disconnect

## [v0.6.3] - 2021/11/18

### Fixed

- Disconnecting from a device synchronously works again

## [v0.6.2] - 2021/10/28

### Fixed

- Request service info also as multicast response for better support of Magic LAN devices

### Changed

- The request timeouts were increased

## [v0.6.1] - 2021/10/20

### Fixed

- Package structure

## [v0.6.0] - 2021/10/20

### Changed

- **BREAKING**: Drop support for Python 3.7
- Use AsyncZeroconf instead of Zeroconf

### Fixed

- Use Zeroconf questions requesting multicast responses for better support of Magic LAN devices

## [v0.5.4] - 2021/10/18

### Fixed

- Fix pip installation

## [v0.5.3] - 2021/10/18

### Changed

- Rework typing
- Mark package as typed
- Add Python 3.10 to CI

## [v0.5.2] - 2021/09/01

### Changed

- Use newer dependency versions

## [v0.5.1] - 2021/01/19

### Fixed

- React correctly on different connection errors

## [v0.5.0] - 2020/12/21

### Changed

- Increase read timeout to better handle busy devices
- If a device is unavailable (e.g. in standby), DeviceUnavailable is raised
- Loggers now contain the module name

### Fixed

- Sometime a warning popped up to properly close the connection to the device although it was properly closed

## [v0.4.0] - 2020/12/08

### Added

- mDNS hostname is now stored in the device object
- Add possibility to pass in an httpx AsyncClient instance
- Ignore devolo Home Control Central Units in discovery function as they offer a device API record but no real device API

### Changed

- **BREAKING**: The discovery function does no longer connect to the device automatically

### Fixed

- Under unfavorable conditions incorrect PLCNET API data was collected

## [v0.3.0] - 2020/12/02

### Added

- If API data is discovered externally, it can be reused
- The devices can be accessed without context manager
- If the network topology is unknown, it can be discovered now

### Changed

- **BREAKING**: The device password must be specified by setting an attribute now

## [v0.2.0] - 2020/09/14

### Added

#### Device API

- Check for firmware updates
- Start firmware updates
- Start WPS

### Fixed

- Port from mDNS query is now used
- Get network overview now also works synchronously
- Sopping identify device now also works synchronously
- Set user device name now also works synchronously

## [v0.1.0] - 2020/08/28

### Added

#### Device API

- Get LED settings
- Set LED settings
- Get connected wifi clients
- Get details about wifi guest access
- Enable or disable guest wifi
- Get visible wifi access points
- Get details about master wifi (repeater only)

#### PLCNET API

- Get details about your powerline network
- Start and stop identifying your PLC device
- Rename your device
