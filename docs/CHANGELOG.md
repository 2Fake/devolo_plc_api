# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/), and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

### Added

- mDNS hostname is now stored in the device object

### Changed

** BREAKING**: The discovery function does no longer connect to the device automatically

## [v0.3.0] - 02.12.2020

### Added

- If API data is discovered externally, it can be reused
- The devices can be accessed without context manager
- If the network topology is unknown, it can be discovered now

### Changed

- **BREAKING**: The device password must be specified by setting an attribute now

## [v0.2.0] - 14.09.2020

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

## [v0.1.0] - 28.08.2020

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
