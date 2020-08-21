from zeroconf import ServiceBrowser, ServiceStateChange, Zeroconf
import time
import socket


def _on_service_state_change(zeroconf: Zeroconf, service_type: str, name: str, state_change: ServiceStateChange):
    """ Service handler for Zeroconf state changes. """
    if state_change is ServiceStateChange.Added:
        zeroconf.get_service_info(service_type, name)


def get_token(ip, service_name):
    # TODO: Optimize the for & if
    zeroconf = Zeroconf()
    browser = ServiceBrowser(zeroconf, service_name, [_on_service_state_change])
    start_time = time.time()
    while not time.time() > start_time + 10:
        for mdns_name in zeroconf.cache.entries():
            try:
                if hasattr(mdns_name, "server"):
                    zc = zeroconf.cache.cache.get(mdns_name.key)
                    for item in zc:
                        if hasattr(item, "server"):
                            try:
                                zc2 = zeroconf.cache.cache[item.server.lower()]
                                for item2 in zc2:
                                    try:
                                        if socket.inet_ntoa(item2.address) == ip:
                                            zc3 = zeroconf.cache.cache.get(item.key)
                                            for item3 in zc3:
                                                if hasattr(item3, "text"):
                                                    parsed_text = parse_zeroconf_text(item3.text)
                                                    if service_name == '_dvl-plcnetapi._tcp.local.':
                                                        return parsed_text['Path']
                                                    else:
                                                        return parsed_text['Path'], parsed_text.get('Features').split(",")
                                    except OSError:
                                        continue
                            except KeyError:
                                continue
            except (AttributeError, OSError, ValueError):
                continue
    browser.cancel()
    zeroconf.close()


def parse_zeroconf_text(text):
    entries = {}
    total_length = len(text)
    parsed_length = 0
    while parsed_length < total_length:
        entry_length = int(text[parsed_length])
        entry = text[parsed_length + 1:parsed_length + entry_length + 1].decode('UTF-8')
        parsed_length = parsed_length + entry_length + 1
        split_entry = entry.split('=')
        entries[split_entry[0]] = split_entry[1]
    entries["Path"] = entries["Path"].split("/")[0]
    return entries
