import machine
from machine import Pin

d0 = Pin(0, Pin.OUT) #esp32c6,
d1 = Pin(1, Pin.OUT)
d2 = Pin(2, Pin.OUT)
d3 = Pin(21, Pin.OUT)
d4 = Pin(22, Pin.OUT)
d5 = Pin(23, Pin.OUT)
d6 = Pin(16, Pin.OUT)

d7 = Pin(17, Pin.OUT)
d8 = Pin(19, Pin.OUT)
d9 = Pin(20, Pin.OUT)
d10 = Pin(18, Pin.OUT)

d0.value(1)
d0.value(0)


