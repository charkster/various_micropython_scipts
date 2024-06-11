import machine
import neopixel
import time

yellow   = (255,150,0) # RGB
red      = (255,0,  0)
green    = (0,  255,0)
no_color = (0,  0,  0)

help(machine.Pin.board)
neo_pwr = machine.Pin.board.NEO_PWR
neo_pwr.value(1)
neo = neopixel.NeoPixel(machine.Pin.board.NEOPIX,1)

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
    
import os
print(os.statvfs("/"))