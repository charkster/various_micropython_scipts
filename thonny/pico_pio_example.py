import machine
import utime
import rp2

# Blink state machine program. Blinks LED at 10 Hz (with freq=2000)
# 2000 Hz / (20 cycles per instruction * 10 instructions) = 10 Hz
# Single pin (base pin) starts at output and logic low
@rp2.asm_pio(set_init=rp2.PIO.OUT_LOW)
# def blink():
#     wrap_target()
#     set(pins, 1) [19]
#     nop()        [19]
#     nop()        [19]
#     nop()        [19]
#     nop()        [19]
#     set(pins, 0) [19]
#     nop()        [19]
#     nop()        [19]
#     nop()        [19]
#     nop()        [19]
#     wrap()
def blink():
    wrap_target()

    set(pins, 1) [24]
    nop()        [24]
    nop()        [24]
    nop()        [24]
    set(pins, 0) [24]
    nop()        [24]
    nop()        [24]
    nop()        [24]  
    wrap()


# Init state machine with "blink" program
# (state machine 0, running at 2kHz, base pin is GP26 (LED))
sm = rp2.StateMachine(0, blink, freq=2000, set_base=machine.Pin(26))

# Continually start and stop state machine
while True:
    print("Starting state machine...")
    sm.active(1)
    utime.sleep(1)
    print("Stopping state machine...")
    sm.active(0)
    utime.sleep(1)