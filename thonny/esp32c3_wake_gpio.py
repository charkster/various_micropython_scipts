import machine
import time
import esp32

p2 = machine.Pin(2, machine.Pin.OUT)
p4 = machine.Pin(4, machine.Pin.IN, machine.Pin.PULL_DOWN)
def wake_routine():
    p2(not p2.value())

#p3.irq(wake_routine, trigger=machine.Pin.IRQ_RISING,wake=machine.IDLE)
esp32.wake_on_ext0(4, esp32.WAKEUP_ANY_HIGH)
while True:
    wake_routine()
    time.sleep(1)
    machine.lightsleep()