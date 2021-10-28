# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

### [v0.6.2] - 2021/10/28

### Fixed

- Request service info also as multicast response for better support of Magic LAN devices

### Changed

- The request timeouts were increased

### [v0.6.1] - 2021/10/20

### Fixed

- Package structure

## [v0.6.0] - 2021/10/20

### Changed

- ** BREAKING**: Drop support for Python 3.7
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

** BREAKING**: The discovery function does no longer connect to the device automatically

### Fixed

- Under unfavorable conditions incorrect PLC API data was collected

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
- Get network overview now also works synchroniously
- Sopping identify device now also works synchroniously
- Set user device name now also works synchroniously

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

#### PLC API

- Get details about your powerline network
- Start and stop identifying your PLC device
- Rename your device
