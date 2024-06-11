import machine
import ustruct

# esp32c3 xiao
i2c = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=100000)

def temp_2_float(temp_bytearray):
    return (ustruct.unpack(">h",temp_bytearray)[0] >> 5) * 0.125

temp_bytearray = i2c.readfrom_mem(0x37,0x00,2)
temp = temp_2_float(temp_bytearray)
print(temp)