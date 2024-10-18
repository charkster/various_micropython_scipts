# Pico 2 overclock
from machine import mem32
import time


def ReadTemperature():
    #RP2350 Datasheet page 1059
    mem32[0x400a0000]=0b0100_0000_0000_0111
    #
    ADC_voltage=mem32[0x400a0004]
    #
    volt = (3.3/4096)*ADC_voltage

    temperature = 27-(volt-0.706)/0.001721

    return (float(temperature))

mem32[0X40100000+0X04]=0b0101101011111110_1010000001010000
# RP2350 Datasheet page 446
# BITS 31:16 are the password 0101101011111110. / 5AFE

# RP2350 Datasheet page452
# BITS 15:0 1010000001010000
# UNLOCK: BIT 13 unlocks the VREG control interface after power up
# 0 - Locked (default)
# 1 - Unlocked
# It cannot be relocked when it is unlocked.
# BITS 6:4 101 / high temperature protection threshold set to 101 - 125C ( default from firmware )

mem32[0X40100000+0X0C]=0b0101101011111110_0000000011010000
# RP2350 Datasheet page 446
# BITS 31:16 are the password 0101101011111110. / 5AFE

# RP2350 Datasheet page454
# BITS 8:4 01101 / SET VOLTAGE to 1.2 / default is 1.1

machine.freq(340_000_000) ###

while True:
     temperature = ReadTemperature()
     print("Temperature: ",temperature)
     time.sleep(1)

import machine
p0 = machine.Pin(0, machine.Pin.OUT) # create output pin on GPIO0
p0.off()

for n in range(0,100):
    p0.on()
    p0.off()