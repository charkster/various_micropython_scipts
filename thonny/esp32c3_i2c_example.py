import machine

# esp32c3 xiao
i2c = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=400000)
# rp2040 xiao
i2c = machine.I2C(1,freq=600000)
#stm32 blackpill, B6,B7
i2c = machine.I2C(1,freq=600000)
devices = i2c.scan()
device_count = len(devices)
if device_count == 0:
    print('No i2c device found.')
else:
    print(device_count, 'devices found.')

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))