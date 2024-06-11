import machine
analog_value = machine.ADC(26)
reading = analog_value.read_u16()
ana_val = reading/65535*3.3
print(ana_val)
