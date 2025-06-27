import machine

# esp32c6 xiao
i2c = machine.I2C(scl=machine.Pin(23), sda=machine.Pin(22), freq=400000)
devices = i2c.scan()
device_count = len(devices)
if device_count == 0:
    print('No i2c device found.')
else:
    print(device_count, 'devices found.')

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))