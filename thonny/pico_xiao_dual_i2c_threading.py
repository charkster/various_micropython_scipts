import machine
import _thread

i2c0=machine.I2C(0,sda=machine.Pin(0), scl=machine.Pin(1), freq=400000) #xiao rp2040
i2c1=machine.I2C(1,sda=machine.Pin(6), scl=machine.Pin(7), freq=400000) #xiao rp2040


def core0_thread():
    data_list_i2c0 = []
    for b in range(0,10):
        data_list_i2c0.append( list(i2c0.readfrom_mem(0x50, b+10, 1, addrsize=16)))


def core1_thread():
    data_list_i2c1 = []
    for n in range(0,10):
        data_list_i2c1.append( list(i2c1.readfrom_mem(0x50, n, 1, addrsize=16)))

second_thread = _thread.start_new_thread(core1_thread, ())
core0_thread()
    
    
    
    
    
    
    
    
    
    
    
    
    
