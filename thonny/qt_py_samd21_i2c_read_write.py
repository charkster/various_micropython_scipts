import machine

i2c = machine.I2C(1,sda=machine.Pin(machine.Pin('SDA')), scl=machine.Pin(machine.Pin('SCL')), freq=400000) # QT PY SAMD21

print('Scanning I2C bus.')
devices = i2c.scan() # this returns a list of devices

for device in devices:
    print('Decimal address:', device, ", Hex address: ", hex(device))

slave_id = 0x08
address  = 0x00
read_int = int.from_bytes(i2c.readfrom_mem(slave_id, address, 1), "little")
print("Address 0x{:02x} have value 0x{:02x}".format(address,read_int))

def read_reg(addr=0x00):
    read_int = int.from_bytes(i2c.readfrom_mem(0x08, addr, 1), "little")
    print("Address 0x{:02x} have value 0x{:02x}".format(addr,read_int))