import machine

i2c=machine.I2C(1, freq=800_000) # PB6 SCL, PB7 SDA not adjustable, frequency is always 320kHz

def scan_i2c_1():
    print('Scanning I2C bus.')
    devices = i2c.scan() # this returns a list of devices

    device_count = len(devices)

    if device_count == 0:
        print('No i2c device found.')
    else:
        print(device_count, 'devices found.')
        for device in devices:
            print('Decimal address:', device, ", Hex address: ", hex(device))

# FRAM example
data_list = list(i2c.readfrom_mem(0x50,0x0000,8,addrsize=16))
print(list(map(hex, data_list)))