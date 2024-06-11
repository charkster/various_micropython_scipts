import machine
import time

p21 = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_DOWN)
p2 = machine.Pin(2, machine.Pin.OUT)

def motion_detect(self):
    p2(1)
    time.sleep(3)
    p2(0)

p21.irq(motion_detect, trigger=machine.Pin.IRQ_RISING)

while True:
    time.sleep(1)