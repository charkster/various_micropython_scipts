import machine

#machine.freq(500_000_000)
p0 = Pin('D0', Pin.OUT) # create output pin on GPIO0

for n in range(0,100):
    p0.on()                 # set pin to "on" (high) level
    p0.off()                # set pin to "off" (low) level
