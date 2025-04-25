import machine

i2c=machine.I2C(1,freq=400_000) #xiao rp2040

print(list(i2c.readfrom_mem(0x3C, 0x0102, 1, addrsize=16)))
i2c.writeto_mem(0x3C, 0x0102, bytearray([0x03, 0x02, 0x01, 0xC2]),addrsize=16)
print(list(i2c.readfrom_mem(0x3C, 0x0102, 1, addrsize=16)))