import machine

vbus_div2 = machine.ADC(machine.Pin(2)) # pin 2 is A0
vbus_div2.atten(machine.ADC.ATTN_11DB) # configure for 150mV to 2450mV range

vbus_mv = int(vbus_div2.read_uv()*2/1e3) # read value
print(vbus_mv)