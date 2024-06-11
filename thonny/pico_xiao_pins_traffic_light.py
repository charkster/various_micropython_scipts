import machine
import time

green  = machine.Pin(1, machine.Pin.OUT)
yellow = machine.Pin(2, machine.Pin.OUT)
red    = machine.Pin(4, machine.Pin.OUT)

def full_cycle(repeat=1):
    for i in range(repeat):
        green.value(1)
        time.sleep(4)
        green.value(0)
        yellow.value(1)
        time.sleep(1)
        yellow.value(0)
        red.value(1)
        time.sleep(4)
        red.value(0)

    