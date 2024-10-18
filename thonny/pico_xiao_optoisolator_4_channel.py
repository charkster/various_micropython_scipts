import machine

ch1_pin = machine.Pin(0, machine.Pin.OUT)  # GPO_0  is TX,  XIAO RP2040
ch2_pin = machine.Pin(7, machine.Pin.OUT)  # GPO_7  is SCL, XIAO RP2040
ch3_pin = machine.Pin(6, machine.Pin.OUT)  # GPO_6  is SDA, XIAO RP2040
ch4_pin = machine.Pin(29, machine.Pin.OUT) # GPO_29 is A3,  XIAO RP2040

ch1_pin.value(0)
ch2_pin.value(0)
ch3_pin.value(0)
ch4_pin.value(0)