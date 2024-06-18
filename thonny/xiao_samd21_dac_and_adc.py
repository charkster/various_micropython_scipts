import machine
help(machine.Pin.board)

# DAC
dac_max_code = 2**10 - 1
dac_gain     = 1.0 # normally unity, but can calibrate gain error
dac_vref     = 3.3
max_rail     = 5.0
dac_offset   = 1  # normally 0 codes, but can calibrate offset error

dac0 = machine.DAC(0) # create DAC object on DAC pin A0_D0
#dac0.write(1023)

def set_dac(volts=0.0):
    dac0.write(int(volts/dac_vref*dac_max_code/dac_gain) + dac_offset)

# ADC
adc_max_code = 2**16-1
adc_vref     = 3.3 / 2.0

adc1 = machine.ADC(machine.Pin('A1_D1'))

def get_adc():
    return (adc1.read_u16() / adc_max_code * adc_vref)

