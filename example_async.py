import asyncio

from devolo_plc_api import Device, wifi_qr_code

# IP of the device to query
IP = "192.168.0.10"

# Password, if the device has one. It is the same as the Web-UI has. It no password is set, you can remove the password
# parameter or set it to None.
PASSWORD = "super_secret"


async def run():
    async with Device(ip=IP) as dpa:
        # Set the password
        dpa.password = PASSWORD

        # Get LED settings of the device. The state might be LED_ON or LED_OFF.
        print("LED is on" if await dpa.device.async_get_led_setting() else "LED if off")

        # Set LED settings of the device. Set enable to True to them turn on, to False to turn them off.
        # If the state was changed successfully, True is returned, otherwise False.
        print("success" if await dpa.device.async_set_led_setting(enable=True) else "failed")

        # Get MultiAP details. If the device is not aware of a mesh controller or doesn't know its IP, it is left empty.
        multi_ap = await dpa.device.async_get_wifi_multi_ap()
        print(multi_ap.enabled)  # True
        print(multi_ap.controller_id)  # "AA:BB:CC:DD:EE:FF"
        print(multi_ap.controller_ip)  # "192.0.2.1"

        # Factory reset the device. If the reset will happen shortly, True is returned, otherwise False.
        print("success" if await dpa.device.async_factory_reset() else "failed")

        # Restart the device. If the restart will happen shortly, True is returned, otherwise False.
        print("success" if await dpa.device.async_restart() else "failed")

        # Get uptime of the device. This value can only be used as a strict monotonically increasing number and therefore has no unit.
        print(await dpa.device.async_uptime())

        # Get support information from the device.
        print(await dpa.device.async_get_support_info())

        # Check for new firmware versions
        firmware = await dpa.device.async_check_firmware_available()
        print(firmware.result)  # devolo_plc_api.device_api.UPDATE_NOT_AVAILABLE
        print(firmware.new_firmware_version)  # ""

        # Start firmware update, if new version is available. Important: The response does not tell you anything about the
        # success of the update itself.
        print("update started" if await dpa.device.async_start_firmware_update() else "no update available")

        # Get details of wifi stations connected to the device: MAC address, access point type (main or guest), wifi band and
        # connection rates.
        connected_stations = await dpa.device.async_get_wifi_connected_station()
        print(connected_stations[0].mac_address)  # "AA:BB:CC:DD:EE:FF"
        print(connected_stations[0].vap_type)  # devolo_plc_api.device_api.WIFI_VAP_MAIN_AP
        print(connected_stations[0].band)  # devolo_plc_api.device_api.WIFI_BAND_5G
        print(connected_stations[0].rx_rate)  # 87800
        print(connected_stations[0].tx_rate)  # 87800

        # Get details about wifi guest access: SSID, Wifi key, state (enabled/disabled) and if time limited, the remaining
        # duration.
        guest_wifi = await dpa.device.async_get_wifi_guest_access()
        print(guest_wifi.ssid)  # "devolo-guest-930"
        print(guest_wifi.key)  # "HMANPGBA"
        print(guest_wifi.enabled)  # False
        print(guest_wifi.remaining_duration)  # 0

        # Get a QR code of the guest wifi settings as byte stream in SVG format
        qr = wifi_qr_code(guest_wifi)
        with open("qr.svg", "wb") as binary_file:
            binary_file.write(qr)

        # Enable or disable the wifi guest access. Set enable to True to it turn on, to False to turn it off. Optionally
        # specify a duration in minutes. Changing SSID or the wifi key is currently not supported. If the state was changed
        # successfully, True is returned, otherwise False.
        print("success" if await dpa.device.async_set_wifi_guest_access(enable=True, duration=5) else "failed")

        # Get details about other access points in your neighborhood: MAC address, SSID, wifi band, used channel, signal
        # strength in DB and a value from 1 to 5, if you would want to map the signal strength to a signal bars.
        neighbor_aps = await dpa.device.async_get_wifi_neighbor_access_points()
        print(neighbor_aps[0].mac_address)  # "AA:BB:CC:DD:EE:FF"
        print(neighbor_aps[0].ssid)  # "wifi"
        print(neighbor_aps[0].band)  # devolo_plc_api.device_api.WIFI_BAND_2G
        print(neighbor_aps[0].channel)  # 1
        print(neighbor_aps[0].signal)  # -73
        print(neighbor_aps[0].signal_bars)  # 1

        # Start WPS push button configuration. If WPS was started successfully, True is returned, otherwise False.
        print("WPS started" if await dpa.device.async_start_wps() else "WPS start failed")

        # Start WPS clone mode. If clone mode was started successfully, True is returned, otherwise False.
        print("WPS clone mode started" if await dpa.device.async_start_wps_clone() else "WPS clone mode start failed")

        # Get PLC network overview with enriched information like firmware version.
        network = await dpa.plcnet.async_get_network_overview()
        print(network.devices[0].product_name)  # "devolo Magic 2 WiFi next"
        print(network.devices[0].product_id)  # "MT3056"
        print(network.devices[0].friendly_version)  # "7.12.5.124"
        print(network.devices[0].full_version)  # "magic-2-wifi-next 7.12.5.124_2022-08-29"
        print(network.devices[0].user_device_name)  # "Living Room"
        print(network.devices[0].mac_address)  # "AABBCCDDEEFF"
        print(network.devices[0].topology)  # devolo_plc_api.plcnet_api.LOCAL
        print(network.devices[0].technology)  # devolo_plc_api.plcnet_api.GHN_SPIRIT
        print(network.devices[0].bridged_devices)  # []
        print(network.devices[0].attached_to_router)  # True
        print(network.devices[0].user_network_name)  # ""
        print(network.devices[0].ipv4_address)  # ""
        print(network.data_rates[0].mac_address_from)  # "AABBCCDDEEFF"
        print(network.data_rates[0].mac_address_to)  # "AABBCCDDEEFF"
        print(network.data_rates[0].tx_rate)  # 129.9375
        print(network.data_rates[0].rx_rate)  # 124.6875

        # Identify the device by making the PLC LED blink. This call returns directly with True, if identifying was started
        # successfully, otherwise False. However, the LED stays blinking for two minutes.
        print("success" if await dpa.plcnet.async_identify_device_start() else "failed")

        # Stop identify the device if you don't want to wait for the timeout.
        print("success" if await dpa.plcnet.async_identify_device_stop() else "failed")

        # Start pairing the device. This call returns directly with True, if pairing was started successfully, otherwise
        # False. However, the device stays in pairing mode for up to three minutes.
        print("success" if await dpa.plcnet.async_pair_device() else "failed")

        # Set the user device name. If the name was changed successfully, True is returned, otherwise False.
        print("success" if await dpa.plcnet.async_set_user_device_name(name="New name") else "failed")


if __name__ == "__main__":
    asyncio.run(run())
