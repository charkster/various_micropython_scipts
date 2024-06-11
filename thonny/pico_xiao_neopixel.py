import machine
import neopixel
import time

yellow   = (255,150,0) # RGB
red      = (255,0,  0)
green    = (0,  255,0)
no_color = (0,  0,  0)

neo_pwr = machine.Pin(11,machine.Pin.OUT)
neo_pwr.value(1)
neo = neopixel.NeoPixel(machine.Pin.board.GP12,1)

def full_cycle(repeat=1):
    for i in range(repeat):
        neo[0] = green
        neo.write()
        time.sleep(3)
        neo[0] = yellow
        neo.write()
        time.sleep(1)
        neo[0] = red
        neo.write()
        time.sleep(3)
        neo[0] = no_color 
        neo.write()

def off():
    neo_pwr.value(0)