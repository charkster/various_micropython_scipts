import machine
import network

wlan = network.WLAN(network.STA_IF)
wlan.active(True)
use_real_ssid_name = True
for net in wlan.scan():
    ssid_name = net[0].decode('ascii')
    if ssid_name:
        if (use_real_ssid_name):
             print("SSID: {:18s}, strength: {:d}".format(ssid_name,net[3]))
        else:
            print("{:d}".format(net[3]))