import machine

i2c = machine.I2C(1,sda=machine.Pin(6), scl=machine.Pin(7), freq=400000) #xiao rp2040

GPIO = MCP23017(i2c=i2c, slave_id=0x20, debug=True)

GPIO.setup(pin='b7', direction=GPIO.OUT, out_val=GPIO.HIGH)
GPIO.setup(pin='b4', direction=GPIO.OUT, out_val=GPIO.LOW)
GPIO.setup(pin='a0', direction=GPIO.IN,  int_en=True, int_defval=GPIO.LOW)
print("--> Pin a0 value is {:d}".format(GPIO.input('a0')))
time.sleep(3)
print("--> INTA and INTB are by default active-low")
print("--> Pin INTA value is {:d}".format(GPIO.input('b5')))
print("--> Pin INTB value is {:d}".format(GPIO.input('b6')))
print("--> Drive b4 high, this should cause an interrupt on INTA")
GPIO.output('b4', GPIO.HIGH)
time.sleep(1)
# Need to read the GPIO pin first, as read_intcap() will clear the interrupt and the pin
print("--> Pin INTA value is {:d}".format(GPIO.input('b5')))
print("--> Pin INTB value is {:d}".format(GPIO.input('b6')))
print("--> Pin a0 value is {:d}".format(GPIO.input('a0')))
GPIO.read_intcap()