from machine import Pin
from machine import mem32

def unlock():
    mem32[0X40100004]=0x5afea050

def overvolt():
    mem32[0X4010000C]=0x5afe00d0

def overclock(freq=320_000_000):
    QMI_M0_TIMING = 0x400D000C
    qmi_div = int(freq/40E6)
    mem32[QMI_M0_TIMING] = 0x40000200 + qmi_div
    unlock()
    overvolt()
    machine.freq(freq)
    
def ReadTemp():
    #RP2350 Datasheet page 1059
    mem32[0x400a0000]=0b0100_0000_0000_0111
    ADC_voltage=mem32[0x400a0004]
    volt = (3.3/4096)*ADC_voltage
    temperature = 27-(volt-0.706)/0.001721
    return (float(temperature))

def get_qmi_clk_div():
    QMI_M0_TIMING = 0x400D000C
    print(mem32[QMI_M0_TIMING] & 0xF)

def gpio_clock():
    d0 = Pin('D0', Pin.OUT)
    d0.off()
    for n in range(0,100):
        d0.on()
        d0.off()
