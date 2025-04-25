import machine
import network
import time
import ntptime
import utime
import mip
import ubinascii

#p21 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)

def connect_to_wifi():
    # Your network credentials
    ssid = '0024A515BC7AX'
    password = 'x3p08mh52h257'
    #Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.ifconfig(('192.168.0.211', '255.255.255.0', '192.168.0.1', '205.171.3.25'))
    time.sleep_ms(1000)
    wlan.active(True)
    time.sleep_ms(1000)
    wlan.connect(ssid, password)

    # Wait for connection to establish
    max_wait = 10
    while max_wait > 0:
        if wlan.status() == 1010:
                break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    # Manage connection errors
    if wlan.status() == 1010:
        print('connected with max address')
        wlan_mac = wlan.config('mac')
        print(ubinascii.hexlify(wlan_mac).decode())
        ntptime.settime() # this is GMT, not Phoenix
        rtc = machine.RTC()
        utc_shift = -7
        tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        rtc.datetime(tm)
    else:
        print(wlan.status())

connect_to_wifi()
mip.install("aioble")

# https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble#passive-scan-for-nearby-devices-for-5-seconds-observer
import aioble
import asyncio

async def get_ble_devices():
    devices = dict()
    names   = dict()
    print('Scanning for BLE devices')
    async with aioble.scan(5000, interval_us=30000, window_us=30000, active=True) as scanner:
        async for result in scanner:
            addr = result.device.addr_hex()
            if result.name() is not None:
#            if True:
                if addr not in devices:
                    # Add match to dict
                    devices[addr] = result.rssi
                    if result.name() is None:
                        names[addr] = addr
                    else:
                        names[addr]   = result.name()
                elif devices[addr] < result.rssi:
                    # Update best RSSI
                    devices[addr] = result.rssi

        # sort by rssi strength
        list_of_keys = sorted(devices, key=devices.get)
        list_of_keys.reverse()

        # Print scan results
        for addr in list_of_keys:
            print(f'Found device: {names[addr]: <25}, Addr: {addr}, Best RSSI: {devices[addr]}')
            
asyncio.run(get_ble_devices())
