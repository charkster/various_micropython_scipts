import machine

i2c=machine.I2C(sda=machine.Pin(5), scl=machine.Pin(6), freq=400000) # esp32s3
i2c.scan()

def get_end_addr():
    for page in range(0,2**16):
        read_64 = i2c.readfrom_mem(0x50,page*64,64,addrsize=16)
        for i in range(0,64):
            if (read_64[i] > 127):
                return i
    print("all full")
    return -1
    

i2c.writeto_mem(0x50, 0x0000, bytearray('this is a message,','ascii'),addrsize=16)
i2c.readfrom_mem(0x50,0x0000,20,addrsize=16)