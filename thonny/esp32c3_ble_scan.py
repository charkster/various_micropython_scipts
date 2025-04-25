# https://github.com/micropython/micropython-lib/tree/master/micropython/bluetooth/aioble#passive-scan-for-nearby-devices-for-5-seconds-observer
import machine
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