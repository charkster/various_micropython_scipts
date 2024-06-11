import machine
import time

p0 = machine.Pin(0, machine.Pin.OUT)
p1 = machine.Pin(1, machine.Pin.IN, machine.Pin.PULL_DOWN)
def wake_routine():
    p0(not p0.value())

p1.irq(wake_routine, trigger=machine.Pin.IRQ_RISING, wake=machine.)