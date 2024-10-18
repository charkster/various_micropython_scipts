import machine
import network
import time
import ntptime
import utime
import socket

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

# HTML form
html = """<!DOCTYPE html>
<html>
    <head> <title>Form Selection</title> </head>
    <body>
        <h1>Form Selection</h1>
        <form action="/" method="post">
            <label for="selection">Choose an option:</label>
            <select name="selection" id="selection">
                <option value="option1">Option 1</option>
                <option value="option2">Option 2</option>
                <option value="option3">Option 3</option>
            </select>
            <input type="submit" value="Submit">
        </form>
    </body>
</html>
"""

# Function to handle client requests
def handle_client(client):
    request = client.recv(1024)
    request = str(request)
#    print('Content = %s' % request)

    if 'POST' in request:
        selection = request.split('selection=')[1].split(' ')[0]
        print('Selected option:', selection) # <------------------------HERE is where to call the PDO request

    client.send('HTTP/1.1 200 OK\r\n')
    client.send('Content-Type: text/html\r\n')
    client.send('Connection: close\r\n\r\n')
    client.sendall(html)
    client.close()

# Set up the web server
addr = socket.getaddrinfo('192.168.0.201', 80)[0][-1]
server_socket = socket.socket()
server_socket.bind(addr)
server_socket.listen(1)
print('Listening on', addr)

while True:
    client, addr = server_socket.accept()
    print('Client connected from', addr)
    handle_client(client)
