import machine
LSB = 3.297 / 65455

print("Pin A0 voltage is {:.3f}".format(machine.ADC(machine.Pin.board.PA0).read_u16() * LSB))
print("Pin A1 voltage is {:.3f}".format(machine.ADC(machine.Pin.board.PA1).read_u16() * LSB))