import time
import umail
import network

def connect_to_wifi():
    # Your network credentials
    ssid = '0024A515BC7E'
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
    else:
        print(wlan.status())

def disconnect_from_wifi():
    wlan = network.WLAN(network.STA_IF)
    wlan.disconnect()

lastTriggerTime=0

def sendEmail():
    #initialize SMTP server and login
    smtp = umail.SMTP('smtp.gmail.com', 465, ssl=True)
    # Email details
    sender_email = 'your_sender_email_account@gmail.com'
    sender_name = 'pico email'
    sender_app_password = 'PASSWORD'
    recipient_email ='charkster@gmail.com'
    email_subject ='ESP32C3 Email'
    smtp.login(sender_email, sender_app_password)
    smtp.to(recipient_email)
    smtp.write("From:" + sender_name + "<"+ sender_email+">\n")
    smtp.write("Subject:" + email_subject + "\n")
    smtp.write("Test of email from ESP32C3 MCU\n")
    timestamp = str(time.localtime())
    smtp.write("Present time is " + timestamp)
    smtp.send()
    smtp.quit()
    lastTriggerTime=time.ticks_ms()
    disconnect_from_wifi()

time.sleep(2)


connect_to_wifi()
time.sleep_ms(1000)
sendEmail()
print("email sent")
