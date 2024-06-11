import machine
import time
from lcd_2004 import LCD_2004
from vcnl4040 import VCNL4040
from ntptime_get_time import *

i2c   = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=400000) # esp32c3 xiao
alarm_p0 = machine.Pin(2, machine.Pin.OUT) # esp32c3 xiao
alarm_p1 = machine.Pin(3, machine.Pin.OUT) # esp32c3 xiao
alarm_p2 = machine.Pin(4, machine.Pin.OUT) # esp32c3 xiao

lcd   = LCD_2004(i2c=i2c)
v4040 = VCNL4040(i2c=i2c)
lcd.lcd_backlight(False)
time.sleep(1)
lcd.lcd_backlight(True)

v4040.i2c_bf_write(v4040.BF_WHITE_EN, v4040.BF_WHITE_EN.TABLE_ENUM["DISABLE"])
v4040.i2c_bf_write(v4040.BF_ALS_IT, v4040.BF_ALS_IT.TABLE_ENUM["320ms"])
v4040.i2c_bf_write(v4040.BF_ALS_SD, v4040.BF_ALS_SD.TABLE_ENUM["ENABLE"])
v4040.i2c_bf_write(v4040.BF_LED_I, v4040.BF_LED_I.TABLE_ENUM["140mA"])
v4040.i2c_bf_write(v4040.BF_PS_MPS, v4040.BF_PS_MPS.TABLE_ENUM["8_MULTI_PULSE"])
v4040.i2c_bf_write(v4040.BF_PS_IT, v4040.BF_PS_IT.TABLE_ENUM["8T"])
v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_POWER_ON"])

connect_wifi()
disconnect_wifi()
last_task=time.time()
prox_count_down = 0
previous_minute = get_minutes()
alarm1_time  = '6:30AM'
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
            
        prox_data = v4040.i2c_bf_read(v4040.BF_PS_DATA)
        if (prox_data > 5):
            alarm_ringing = False
            lcd.lcd_print("Prox "+ str(prox_data),1,0)
            v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_SHUT_DOWN"])
            v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_POWER_ON"])
        else:
            lcd.lcd_print("           ",1,0)
        last_task=time.time()
    time.sleep(0.1) # this should be half of the repeat interval
    if (v4040.i2c_bf_read(v4040.BF_ALS_DATA) < 400) and (v4040.i2c_bf_read(v4040.BF_PS_DATA) < 5) and (prox_count_down == 0):
        lcd.lcd_backlight(False)
    elif (prox_count_down < 40):
        prox_count_down = prox_count_down + 1
        lcd.lcd_backlight(True)
    else:
        prox_count_down = 0