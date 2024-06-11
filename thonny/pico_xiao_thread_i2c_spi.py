import machine
import _thread

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

# Adafruit spi fram commands
_NULL_DATA = 0x00
_READ_SPACE_LIST = [_NULL_DATA] * 10
_WREN_CMD  = 0x06
_WRITE_CMD = 0x02
_READ_CMD  = 0x03

read_bytes = bytearray([_NULL_DATA] * 13)

def core0_thread():
    data_list_spi = []
    for b in range(0,10):
        spi_cs.value(0) 
        data_list_spi.append(spi.write_readinto(bytearray([_READ_CMD, 0x00, 0x00] + _READ_SPACE_LIST),read_bytes))
        spi_cs.value(1) 


def core1_thread():
    data_list_i2c = []
    for n in range(0,10):
        data_list_i2c.append( list(i2c.readfrom_mem(0x50, n*8, 8, addrsize=16)))

second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()
    
    
    
    
    
    
    
    
    
    
    
    
    