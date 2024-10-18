from AP33772 import *
import machine

i2c    = machine.I2C(1,sda=machine.Pin(6), scl=machine.Pin(7), freq=100000) #xiao rp2040
en_pin = machine.Pin(3, machine.Pin.OUT) # en_pin connects to 3V3 pin on mikroe click board
#i2c = machine.I2C(1,sda=machine.Pin(machine.Pin('SDA')), scl=machine.Pin(machine.Pin('SCL')), freq=100000) # QT PY SAMD21
#en_pin = machine.Pin(machine.Pin.board.MOSI, machine.Pin.OUT) # adafruit

en_pin.value(1)
USB_PD = AP37772(i2c=i2c)
for pdo_num in range(1,8):
    USB_PD.get_pdo(pdo_num)
USB_PD.get_pdo_num()
USB_PD.get_voltage()
USB_PD.get_current()
USB_PD.get_temp()
USB_PD.send_rdo(type='FIXED', pdo_num=1, op_current=2.8, max_current=3.0)
USB_PD.get_pdo_status()
USB_PD.send_rdo(type='PPS', pdo_num=6, op_current=3.0, voltage=8.2)
USB_PD.send_rdo_reset()
en_pin.value(0)