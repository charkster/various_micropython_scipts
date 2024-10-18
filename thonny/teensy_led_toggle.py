import machine
import time

help(machine)
help(machine.Pin)
help(machine.board)

led = machine.LED(1)

led.on()
time.sleep(1)
led.off()
time.sleep(1)
led.toggle()
time.sleep(1)
led.toggle()

machine.Pin('LED').value(1)
time.sleep(1)
machine.Pin('LED').value(0)

print(list(map(hex, machine.unique_id())))