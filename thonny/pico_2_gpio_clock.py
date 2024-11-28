import machine

machine.mem32[0X40100000+0X04]=0b0101101011111110_1010000001010000
machine.mem32[0X40100000+0X0C]=0b0101101011111110_0000000011010000
machine.freq(320_000_000)

p4 = machine.Pin(4, machine.Pin.OUT) # create output pin on GPIO0

def gpio_clock():
    for n in range(0,100):
        p4.on()
        p4.off()

@micropython.native
def gpio_clock_native():
    for n in range(0,100):
        p4.on()
        p4.off()

@micropython.viper
def gpio_clock_viper():
    for n in range(0,100):
        p4.on()
        p4.off()