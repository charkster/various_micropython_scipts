import machine
import socket
import network
import time
import ntptime
import utime
from AP33772 import *

i2c    = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=100000) # esp32c3 xiao
en_pin = machine.Pin(20, machine.Pin.OUT) # pin 20 is 'TX_D6'

def connect_to_wifi():
    # Your network credentials
    ssid = '0024A515BC7AX'
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
        ntptime.timeout = 4
        ntptime.settime() # this is GMT
        rtc = machine.RTC()
        utc_shift = -7 # Phoenix Arizona
        tm = utime.localtime(utime.mktime(utime.localtime()) + utc_shift*3600)
        tm = tm[0:3] + (0,) + tm[3:6] + (0,)
        rtc.datetime(tm)
    else:
        print(wlan.status())

connect_to_wifi()

en_pin.value(0)
time.sleep(1)
en_pin.value(1)
USB_PD = AP37772(i2c=i2c)
#for pdo_num in range(1,8):
#    USB_PD.get_pdo(pdo_num)
#USB_PD.get_pdo_num()
#USB_PD.get_voltage()
#USB_PD.get_current()
#USB_PD.get_temp()
#USB_PD.send_rdo(type='FIXED', pdo_num=1, op_current=2.8, max_current=3.0)
#USB_PD.get_pdo_status()
#USB_PD.send_rdo(type='PPS', pdo_num=6, op_current=3.0, voltage=8.2)
#USB_PD.send_rdo_reset()
#en_pin.value(0)
num_pdo = 0
pdo_list = ['0 OFF']
#pdo_html  = '<pre><b>Num,   Type,  Volts, Current</b><br />\n'
pdo_html  = '<pre><b>Num, Type,  Volt Upper, Volt Lower, Current</b><br />\n'
for pdo_num in range(1,8):
    pdo = USB_PD.get_pdo(pdo_num)
    if (pdo[2] > 0.0):
        if (pdo[1] == 'FIXED'):
            #          Num, Type, Volt Upper, Volt Lower, Current
            pdo_str = '{}    {:5}  {:5.1f}                    {:.2f}'.format(pdo[0],pdo[1],pdo[2],pdo[3])
        else:
            pdo_str = '{}    {:5}  {:5.1f}        {}         {:.2f}'.format(pdo[0],pdo[1],pdo[2],pdo[3],pdo[4])
#        pdo_str = ' '.join(f'{x:6}' for x in map(str, pdo))
        pdo_html +=  pdo_str + '<br />\n'
        pdo_list.append(pdo_str)
        num_pdo += 1
pdo_html += '</pre>\n'

html_str  = '<!DOCTYPE html>\n'
html_str += '<html>\n'
html_str += '<body>\n'
html_str += '<h2>Available PDOs</h2>\n'
html_str += pdo_html + '<br />\n'
html_str += '<form action=\"/\" method=\"post\">\n'
html_str += '<b><label for=\"pdo-select\">PDO Selection:</label></b><br />\n'
html_str += '<select name=\"selection\" id=\"PDO Select\">\n'
html_str += '<option value=\"\">--Please choose an option--</option>\n'
pdo_count = 0
for pdo in pdo_list:
    html_str += '<option value=\"' + str(pdo_count) + '\">' + pdo + '</option>\n'
    pdo_count += 1
html_str += '</select>\n'
html_str += '<input type=\"submit\" value=\"Click to Select\"/><br />\n'
html_str += '<b><label for=\"pps_volt\">PPS Voltage:</label></b><br />\n'
html_str += '<input type=\"number\" required name=\"pps_volt\" min=\"0\" value=\"0\" step=\"0.01\"><br />\n'
html_str += '</form>\n'
html_str += '</body>\n'
html_str += '</html>\n'

# Function to handle client requests
def handle_client(client):
    request = client.recv(1024)
    request = str(request)
    print('Content = %s' % request)

    if 'POST' in request:
        pps_volt = 0.0
        selection = int(request.split('selection=')[1][0])
        pps_volt  = float(request.split('pps_volt=')[1][:-1])
        print('Selected option:', selection)
        print('PPS Voltage:', pps_volt)
        if (selection == 0): # disable
            USB_PD.send_rdo_reset()
            en_pin.value(0)
            time.sleep(1)
            en_pin.value(1)
        else:
            pdo = USB_PD.get_pdo(selection)
            if (pdo[1] == 'FIXED'):
                USB_PD.send_rdo(type=pdo[1], pdo_num=selection, op_current=pdo[3], max_current=pdo[3])
            elif (pdo[1] == 'PPS'):
                if (pps_volt >= pdo[3] and pps_volt <= pdo[2]):
                    USB_PD.send_rdo(type=pdo[1], pdo_num=selection, op_current=pdo[4], voltage=pps_volt)

    client.send('HTTP/1.1 200 OK\r\n')
    client.send('Content-Type: text/html\r\n')
    client.send('Connection: close\r\n\r\n')
    client.sendall(html_str)
    client.close()

# Set up the web server
address = socket.getaddrinfo('192.168.0.201', 80)[0][-1]
server_socket = socket.socket()
server_socket.bind(address)
server_socket.listen(5) # at most 5 clients
print('Listening on', address)

while True:
    client, addr = server_socket.accept()
    print('Client connected from', address)
    handle_client(client)

