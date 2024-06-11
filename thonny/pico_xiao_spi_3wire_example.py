import machine

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

print("Write to Address 0x00 Data 0xE5")
buffer = bytearray([0x00, 0xE5, 0x81, 0xC2])
spi_cs.value(0)
spi.write_readinto(buffer,buffer) # buffer is overwritten with read data
spi_cs.value(1) 
print(list(map(hex, buffer)))

print("Read from Address 0x00")
buffer = bytearray([0x80, 0x00, 0x00, 0x00, 0x00])
spi_cs.value(0)
spi.write_readinto(buffer,buffer) # buffer is overwritten with read data
spi_cs.value(1) 
print(list(map(hex, buffer)))
