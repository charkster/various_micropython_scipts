import machine
import time

pwm = machine.PWM(machine.Pin(0))

pwm.freq(1000)

while True:
    for duty in range(65025):
		pwm.duty_u16(duty)
	for duty in range(65025, 0, -1):
		pwm.duty_u16(duty)