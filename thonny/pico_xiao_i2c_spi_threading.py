import machine

i2c=machine.I2C(1,sda=machine.Pin(6), scl=machine.Pin(7), freq=400000) #xiao rp2040

spi = machine.SPI(0,
                  baudrate=1000000,
                  polarity=1,
                  phase=1,
                  bits=8,
                  firstbit=machine.SPI.MSB,
                  sck=machine.Pin(2),
                  mosi=machine.Pin(3),
                  miso=machine.Pin(4))

spi_cs = machine.Pin(1, machine.Pin.OUT)
spi_cs.value(1) # active low

# Adafruit i2c fram is 0x50
data_list = list(i2c.readfrom_mem(0x50,0x0000,8,addrsize=16))
print(list(map(hex, data_list)))
i2c.writeto_mem(0x50, 0x0000, bytearray([0x03, 0x02, 0x01, 0x00]),addrsize=16)
data_list = list(i2c.readfrom_mem(0x50, 0x00, 8, addrsize=16))
print(list(map(hex, data_list)))


# Adafruit spi fram commands
_NULL_DATA = 0x00
_READ_SPACE_LIST = [_NULL_DATA] * 10
_WREN_CMD  = 0x06
_WRITE_CMD = 0x02
_READ_CMD  = 0x03
_RDID_CMD  = 0x9F

read_bytes = bytearray([_NULL_DATA] * 13)

spi_cs.value(0) 
spi.write_readinto(bytearray([_READ_CMD, 0x00, 0x00] + _READ_SPACE_LIST),read_bytes)
spi_cs.value(1) 
print(list(read_bytes))

spi_cs.value(0) 
spi.write(bytearray([_WREN_CMD]))
spi_cs.value(1)
spi_cs.value(0)
spi.write(bytearray([_WRITE_CMD, 0x00, 0x00, 0x07, 0x07, 0x06, 0x06, 0x05, 0x05, 0x04, 0x04]))
spi_cs.value(1)

spi_cs.value(0) 
spi.write_readinto(bytearray([_READ_CMD, 0x00, 0x00] + _READ_SPACE_LIST),read_bytes)
spi_cs.value(1) 
print(list(read_bytes))