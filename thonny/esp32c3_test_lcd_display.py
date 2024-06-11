import machine
import time
from lcd_2004 import LCD_2004
from vcnl4040 import VCNL4040
from ntptime_get_time import *


i2c = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=400000) # esp32c3 xiao

lcd   = LCD_2004(i2c=i2c)
v4040 = VCNL4040(i2c=i2c) 
lcd.lcd_backlight(False)
time.sleep(2)
lcd.lcd_backlight(True)

connect_wifi()
disconnect_wifi()
last_task=time.time()
while True:
    if (time.time() - last_task) >= 1: # true every 1 seconds
        lcd.lcd_print(get_time(),2,0)
        last_task=time.time()
    time.sleep(0.5) # this should be half of the repeat interval