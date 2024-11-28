import machine
import time
import umail
import network
import ntptime
import utime

def connect_to_wifi():
    # Your network credentials
    ssid = '0024A515BC7F'
    password = 'x3p08mh52h257'
    #Connect to Wi-Fi
    wlan = network.WLAN(network.STA_IF)
    time.sleep_ms(1000)
    wlan.active(True)
    time.sleep_ms(1000)
    wlan.connect(ssid, password)
    time.sleep_ms(1000)

    # Wait for connection to establish
    max_wait = 10
    while max_wait > 0:
        if wlan.status() >= 3:
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

def sendEmail():
    #initialize SMTP server and login
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    # Email details
    sender_email = 'azstanfordfamily@gmail.com'
    sender_name = 'pico email'
    sender_app_password = 'eueewczhxrmeuhph'
    recipient_email ='charkster@gmail.com'
    email_subject ='ESP32C3 ADC CSV file'
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    uuidgen = "ddb8f663-bfcd-49d6-ae3f-ade84587f9d0"
    smtp.write("MIME-Version: 1.0\n")
    smtp.write("Content-Type: multipart/mixed; boundary=" + uuidgen + '\n\n')
    smtp.write("--" + uuidgen + '\n') # boundary
    smtp.write("Content-Type: text/plain; charset=UTF-8\n")
    smtp.write("Content-Disposition: inline\n\n")
    t = time.localtime()
    date = str("{:2d}/{:2d}/{:4d} {:2d}:{:02d}:{:02d}".format(t[1],t[2],t[0],t[3],t[4],t[5]))
    smtp.write("ESP32C3 MCU ADC logfile is attached\n")
    smtp.write("Present time is " + date + '\n\n')
    smtp.write("--" + uuidgen + '\n') # boundary
    csv_file = 'adc_logfile.csv'
    smtp.write('Content-Type: text/csv; name=' + csv_file + '\n')
    smtp.write('Content-Disposition: attachment; filename=' + csv_file + '\n\n')
    try:
        with open(csv_file, 'r') as infile:
            content = infile.read()
    except OSError:
        pass
    smtp.write(content)
    smtp.write('\n')
    smtp.send()
    smtp.quit()
    disconnect_from_wifi()

def main():
    vbus_div2 = machine.ADC(machine.Pin(1)) # two 120k resistor divider for VBUS
    vbus_div2.atten(machine.ADC.ATTN_11DB) # use 3.3V range
    f = open('adc_logfile.csv', 'w')
    minute_count = 0
    try:
        while True:
            vbus_mv = int(vbus_div2.read_uv()*2/1e3) # millivolt
            f.write("{:d}\n".format(vbus_mv))
#            machine.deepsleep(60*1000) # 60 seconds
            time.sleep(60)
            minute_count += 1
            if (minute_count == 3):
                connect_to_wifi()
                time.sleep_ms(1000)
                sendEmail()
                minute_count = 0
    except KeyboardInterrupt:
        f.close()

if __name__ == '__main__':  
   main()
