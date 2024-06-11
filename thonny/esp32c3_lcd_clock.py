import machine
import time
from lcd_2004 import LCD_2004
from apds9960 import APDS9960
from ntptime_get_time import *

i2c      = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=400000) # esp32c3 xiao
alarm_p0 = machine.Pin(2, machine.Pin.OUT) # esp32c3 xiao
alarm_p1 = machine.Pin(3, machine.Pin.OUT) # esp32c3 xiao
alarm_p2 = machine.Pin(4, machine.Pin.OUT) # esp32c3 xiao
apds     = apds = APDS9960(i2c=i2c)
lcd      = LCD_2004(i2c=i2c)

lcd.lcd_backlight(False)
time.sleep(1)
lcd.lcd_backlight(True)

apds.i2c_bf_write(apds.BF_AGAIN, apds.BF_AGAIN.TABLE_ENUM["64X"])
apds.i2c_bf_write(apds.BF_PON,   apds.BF_PON.TABLE_ENUM["CHIP_ON"])
apds.i2c_bf_write(apds.BF_AEN,   apds.BF_AEN.TABLE_ENUM["ENABLE"])
# LDRIVE stays at default value of 100mA
apds.i2c_bf_write(apds.BF_PGAIN, apds.BF_PGAIN.TABLE_ENUM["4X"])
apds.i2c_bf_write(apds.BF_PEN,   apds.BF_PEN.TABLE_ENUM["ENABLE"])

connect_wifi()
disconnect_wifi()
last_task=time.time()
prox_count_down = 0
previous_minute = get_minutes()
alarm1_time  = '6:45AM'
alarm1_days  = 'Mon-Sun' # allowed is 'Mon-Fri' or 'Mon-Sun'
lcd.lcd_print("ALARM "+alarm1_days+" "+alarm1_time,4,0)
alarm_toggle = 0
alarm_ringing = False
while True:
    if (time.time() - last_task) >= 1: # true every 1 seconds
        lcd.lcd_print(get_time(),2,0)
        minute = get_minutes()
        if (previous_minute != minute): # check for alarms
            if (get_alarm_time() == alarm1_time):
                day_of_week = get_day_of_week()
                if (day_of_week in ["Mon", "Tue", "Wed", "Thu", "Fri"] or (day_of_week in ["Sat", "Sun"] and alarm1_days == 'Mon-Sun')):
                    alarm_ringing = True
            else:
                alarm_ringing = False # only ring for 1 minute maximum
            if (get_alarm_time() == '2:59AM'): # update time
                connect_wifi()
                disconnect_wifi()
        previous_minute = minute
        if (alarm_ringing):
            alarm_toggle = alarm_toggle ^ 1
            alarm_p0.value(alarm_toggle)
            alarm_p1.value(alarm_toggle)
            alarm_p2.value(alarm_toggle)
        else:
            alarm_p0.value(0)
            alarm_p1.value(0)
            alarm_p2.value(0)
            
        prox_data = apds.i2c_bf_read(apds.BF_PDATA)
        if (prox_data > 5):
            alarm_ringing = False
            lcd.lcd_print("Prox "+ str(prox_data),1,0)
        else:
            lcd.lcd_print("           ",1,0)
        last_task=time.time()
    time.sleep(0.1) # this should be half of the repeat interval
    als_data  = (apds.i2c_bf_read(apds.BF_CDATAH) << 8) + apds.i2c_bf_read(apds.BF_CDATAL)
    prox_data = apds.i2c_bf_read(apds.BF_PDATA)
    if (als_data < 5) and (prox_data < 3) and (prox_count_down == 0):
        lcd.lcd_backlight(False)
        time.sleep(1)
    elif (prox_count_down < 40):
        prox_count_down = prox_count_down + 1
        lcd.lcd_backlight(True)
    else:
        prox_count_down = 0