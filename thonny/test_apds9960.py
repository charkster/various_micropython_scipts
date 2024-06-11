import machine

#i2c  = machine.I2C(1,sda=machine.Pin(22),scl=machine.Pin(23),freq=400000) # QT PY RP2040, STEMMA
i2c      = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=400000) # esp32c3 xiao
#list_of_dev_addresses = i2c.scan()
#print([hex(x) for x in list_of_dev_addresses])

apds = APDS9960(i2c=i2c)
apds.check_default_values(debug=True)

apds.i2c_bf_write(apds.BF_AGAIN, apds.BF_AGAIN.TABLE_ENUM["16X"])
apds.i2c_bf_write(apds.BF_PON,   apds.BF_PON.TABLE_ENUM["CHIP_ON"])
apds.i2c_bf_write(apds.BF_AEN,   apds.BF_AEN.TABLE_ENUM["ENABLE"])
cdatal = apds.i2c_bf_read(apds.BF_CDATAL)
cdatah = apds.i2c_bf_read(apds.BF_CDATAH)
print("Ambient light value is {:d}".format((cdatah << 8) + cdatal))
als_data = (apds.i2c_bf_read(apds.BF_CDATAH) << 8) + apds.i2c_bf_read(apds.BF_CDATAL)


# LDRIVE stays at default value of 100mA
apds.i2c_bf_write(apds.BF_PGAIN, apds.BF_PGAIN.TABLE_ENUM["4X"])
apds.i2c_bf_write(apds.BF_PEN,   apds.BF_PEN.TABLE_ENUM["ENABLE"])
print("Proximity value is {:d}".format(apds.i2c_bf_read(apds.BF_PDATA)))