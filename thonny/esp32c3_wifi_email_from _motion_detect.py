import umail
import machine
import network
import time
import ntptime
import utime

p21 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)

def connect_to_wifi():
    # Your network credentials
    ssid = '0024A515BC7AX'
    password = 'x3p08mh52h257'
    #Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
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

def disconnect_from_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()

lastTriggerTime=0

def sendEmail():
    t = time.localtime()
    date = str("{:2d}/{:2d}/{:4d} {:2d}:{:02d}:{:02d}".format(t[1],t[2],t[0],t[3],t[4],t[5]))
    #initialize SMTP server and login
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    # Email details
    sender_email = 'azstanfordfamily@gmail.com'
    sender_name = 'pico email'
    sender_app_password = 'eueewczhxrmeuhph'
    recipient_email ='charkster@gmail.com'
    email_subject ='ESP32C3 Motion Detect'
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write("Motion detected\n")
    smtp.write(date)
    smtp.send()
    smtp.quit()
    lastTriggerTime=time.ticks_ms()
    disconnect_from_wifi()

def motion_detect(self):
    p21 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)
    p21.irq(motion_detect, trigger=0) # disable IRQ
    connect_to_wifi()
    sendEmail()
    time.sleep(60)
    p21.irq(motion_detect, trigger=machine.Pin.IRQ_RISING) # enable IRQ

time.sleep(60) # allow sensor to settle
p21.irq(motion_detect, trigger=machine.Pin.IRQ_RISING)

while True:
    time.sleep(1)