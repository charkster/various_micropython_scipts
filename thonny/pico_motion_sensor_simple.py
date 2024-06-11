#Code source: electrocredible.com , Language: MicroPython

from machine import Pin
import time

pin = Pin(16, Pin.IN, Pin.PULL_DOWN)
led = Pin("LED", Pin.OUT)
isMotionDetected=False;

def detect_motion(pin):
    global isMotionDetected
    isMotionDetected=True

pin.irq(trigger=Pin.IRQ_RISING, handler=detect_motion)

time.sleep(2)

while True:
    if isMotionDetected:
        isMotionDetected=False
        print("Motion Detected")
        print("timestamp={}". format(time.time()))
        led.on()
        time.sleep_ms(2000)
        led.off()