import machine

i2c=machine.I2C(0, freq=400_000) # Teensy pins 19 SCL0, 18 SDA0

print('Scanning I2C bus.')
#devices = i2c.scan() # this returns a list of devices

for a in range(0,10):
    try:
        i2c.readfrom(0xE2,1)
    except:
        pass

# FRAM i2c
data_list = list(i2c.readfrom_mem(0x50,0x0000,8,addrsize=16))
print(list(map(hex, data_list)))