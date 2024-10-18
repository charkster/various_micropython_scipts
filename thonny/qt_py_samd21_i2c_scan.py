import machine

i2c = machine.I2C(1,sda=machine.Pin(machine.Pin('SDA')), scl=machine.Pin(machine.Pin('SCL')), freq=400000) # QT PY SAMD21

print('Scanning I2C bus.')
devices = i2c.scan() # this returns a list of devices

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))

slave_id = 0x51

def write_data(slave_id=0x00, address=0x00, data=0x00): # write data
    num_bytes = (data.bit_length() + 7) // 8
    i2c.writeto_mem(slave_id, address, data.to_bytes(num_bytes, "little"))
    
def read_data(address=0x00, num_bytes=1):
    int_read_byte = int.from_bytes(i2c.readfrom_mem(slave_id, address, num_bytes), "little")
    return int_read_byte # int value

read_data(0x00,28)
i2c.readfrom_mem(slave_id, 0x00, 4)
i2c.writeto_mem(slave_id, 0x30, bytearray([0x00, 0x00, 0x00, 0x00]))

for byte in list(i2c.readfrom_mem(slave_id, 0x04, 4)):
    print(hex(byte))