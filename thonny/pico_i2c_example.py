import machine

I2C_SDA_PIN = 0
I2C_SCL_PIN = 1
i2c=machine.I2C(0,sda=machine.Pin(I2C_SDA_PIN), scl=machine.Pin(I2C_SCL_PIN), freq=400000)

print('Scanning I2C bus.')
devices = i2c.scan() # this returns a list of devices

device_count = len(devices)

if device_count == 0:
    print('No i2c device found.')
else:
    print(device_count, 'devices found.')

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))

data_list = list(i2c.readfrom_mem(0x40, 0x00, 128))
print(list(map(hex, data_list)))

i2c.writeto_mem(0x40, 0x00, bytearray([0x00, 0x01, 0x02, 0x03]))


