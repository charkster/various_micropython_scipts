import machine
import network
import time
import utime
import ntptime

def connect_wifi():
    # Your network credentials
    ssid = '0024A515BC7E'
    password = 'x3p08mh52h257'
    #Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    wlan.ifconfig(('192.168.0.201', '255.255.255.0', '192.168.0.1', '205.171.3.25'))
    time.sleep_ms(1000)
    wlan.active(True)
    time.sleep_ms(1000)
    wlan.connect(ssid, password)

    # Wait for connection to establish
    max_wait = 10
    while max_wait > 0:
        if wlan.status() == 1010:
                break
        max_wait -= 1
        print('waiting for connection...')
        time.sleep(1)
    
    # Manage connection errors
    if wlan.status() == 1010:
        print('connected')
        ntptime.settime() # this is GMT, not Phoenix
        rtc = machine.RTC()
        utc_shift = -7
        tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        rtc.datetime(tm)
    else:
        print(wlan.status())

def disconnect_wifi():
    wlan = network.WLAN()
    wlan.disconnect()

def get_time():
    rtc = machine.RTC()
    year, month, day, dow, hour, mins, secs = rtc.datetime()[0:7]
    days   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    months = ["JAN", "FEB", "MAR", "APR", "MAY", "JUN", "JUL", "AUG", "SEP", "OCT", "NOV", "DEC"]
    day_name = days[dow]
    month_name = months[month-1]
    date_time = str("{:s} {:s}{:2d} {:2d}:{:02d}:{:02d}{}M".format(day_name,month_name,day,(hour-1)%12+1,mins,secs,chr(65+15*(hour//12))))
    return date_time

def get_seconds():
    rtc = machine.RTC()
    year, month, day, dow, hour, mins, secs = rtc.datetime()[0:7]
    return secs

def get_minutes():
    rtc = machine.RTC()
    year, month, day, dow, hour, mins, secs = rtc.datetime()[0:7]
    return mins

def get_hours():
    rtc = machine.RTC()
    year, month, day, dow, hour, mins, secs = rtc.datetime()[0:7]
    return hour

def get_day_of_week():
    rtc = machine.RTC()
    year, month, day, dow, hour, mins, secs = rtc.datetime()[0:7]
    days   = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    day_name = days[dow]
    return day_name

def get_alarm_time():
    rtc = machine.RTC()
    year, month, day, dow, hour, mins, secs = rtc.datetime()[0:7]
    alarm_time = str("{:d}:{:02d}{}M".format((hour-1)%12+1,mins,chr(65+15*(hour//12))))
    return alarm_time