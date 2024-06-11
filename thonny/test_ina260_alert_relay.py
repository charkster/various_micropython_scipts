i2c    = machine.I2C(0,sda=machine.Pin(24),scl=machine.Pin(25),freq=400000) # QT PY RP2040
ina260 = INA260(i2c=i2c, i2c_dev_addr=0x40)

print(ina260.get_bus_voltage())
print(ina260.get_current())

ina260.set_alert_current_limit(cur_lim=0.05)
