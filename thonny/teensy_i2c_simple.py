import machine

i2c=machine.I2C(0, freq=1000000) # Teensy pins 19 SCL0, 18 SDA0

print('Scanning I2C bus.')
#devices = i2c.scan() # this returns a list of devices

for a in range(0,10):
    try:
        i2c.readfrom(0xE2,1)
    except:
        pass