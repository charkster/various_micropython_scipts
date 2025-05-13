import machine
import time

#help(machine.Pin.board) # this shows which pins can be PWM, which is A0 and D0
pwm = machine.PWM(machine.Pin.board.D0) # set pin to be D0 on Xiao
pwm.init(freq=10, duty_u16=32768) # 10Hz, 50% duty
time.sleep(10)
pwm.deinit()