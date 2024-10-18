class MCP23017:

    # Constructor
    def __init__(self, i2c, slave_id=0x20, debug=False):
        self.i2c      = i2c
        self.slave_id = slave_id
        self.debug    = debug

    #Constants
    IN            = 1
    OUT           = 0
    PULLUP        = 1
    HIGH          = 1
    LOW           = 0
    INVERT        = 1
    NONINVERT     = 0
    INT_ON_CHG    = 1
    INT_ON_DEFVAL = 0

    #BANK == 0 addresses, POR value, Register Access, Name
    IODIRA   = (0x00, 0xFF, 'RW', 'IODIR')
    IPOLA    = (0x02, 0x00, 'RW', 'IPOL')
    GPINTENA = (0x04, 0x00, 'RW', 'GPINTEN')
    DEFVALA  = (0x06, 0x00, 'RW', 'DEFVAL')
    INTCONA  = (0x08, 0x00, 'RW', 'INTCON')
    IOCON    = (0x0A, 0x00, 'RW', 'IOCON')
    GPPUA    = (0x0C, 0x00, 'RW', 'GPPU')
    INTFA    = (0x0E, 0x00, 'RO', 'INTF')
    INTCAPA  = (0x10, 0x00, 'RO', 'INTCAP')
    GPIOA    = (0x12, 0x00, 'RW', 'GPIO')
    OLATA    = (0x14, 0x00, 'RW', 'OLAT')

    list_of_regs = [IODIRA, IPOLA, GPINTENA, DEFVALA, INTCONA, IOCON, 
                    GPPUA,  INTFA, INTCAPA,  GPIOA,   OLATA]

    def write_byte_data(self, address=0x00, data=0x00):
        self.i2c.writeto_mem(self.slave_id, address, bytearray([data & 0xFF]))
    
    def read_byte_data(self, address=0x00):
        int_read_byte = list(self.i2c.readfrom_mem(self.slave_id, address, 1))[0]
        return int_read_byte # int value

    def check_valid_pin(self, pin='a0'):
        #check valid pin, set offset either to 0 or 1
        if (pin[0] == 'a' or pin[0] == 'A'):
            offset = 0x00
        elif (pin[0] == 'b' or pin[0] == 'B'):
            offset = 0x01
        else:
            print("ERROR first character of pin must be a, A, b or B")
            return -1
        if (self.debug == True):
            print("Offset is 0x{:02x}".format(offset))
        if (int(pin[1]) not in range(0,8)):
            print("ERROR second character of pin must be 0 thru 7")
            return -1
        return offset

    # all parameters are POR values
    def setup(self, pin='a0', direction=IN, out_val=LOW, in_polarity=NONINVERT, in_pullup=False, int_en=False, int_on_change=False, int_defval=0):
        offset = self.check_valid_pin(pin)
        #check and set input direction
        read_direction = self.read_byte_data(self.IODIRA[0] + offset)
        if (direction == self.IN):
            direction_data = read_direction | (1 << int(pin[1]))
            #check and set polarity if input
            read_polarity = self.read_byte_data(self.IPOLA[0] + offset)
            if (in_polarity == self.INVERT):
                polarity_data = read_polarity | (1 << int(pin[1]))
            elif (in_polarity == self.NONINVERT):
                polarity_data = read_polarity & ( 0xFF - (1 << int(pin[1])) )
            else:
                print("ERROR in_polarity must be either 1 for invert or 0 for noninvert")
                return -1
            if (self.debug == True):
                print("Write address 0x{:02x} with data 0x{:02x}".format(self.IPOLA[0] + offset, polarity_data))
            self.write_byte_data(self.IPOLA[0] + offset, polarity_data)
            #set or clear pullup
            read_pullup = self.read_byte_data(self.GPPUA[0] + offset)
            if (in_pullup == True):
                pullup_data = read_pullup | (1 << int(pin[1]))
            else:
                pullup_data = read_pullup & ( 0xFF - (1 << int(pin[1])) )
            if (self.debug == True):
                print("Write address 0x{:02x} with data 0x{:02x}".format(self.GPPUA[0] + offset, pullup_data))
            self.write_byte_data(self.GPPUA[0] + offset, pullup_data)
            #set interupt enable and interrupt type
            read_int_en = self.read_byte_data(self.GPINTENA[0] + offset)
            if (int_en == True):
                int_en_data = read_int_en | (1 << int(pin[1]))
                read_int_on_change = self.read_byte_data(self.INTCONA[0] + offset)
                if (int_on_change == True):
                    int_on_change_data = read_int_on_change | (1 << int(pin[1]))
                else:
                    int_on_change_data = read_int_on_change & ( 0xFF - (1 << int(pin[1])) )
                    #set defval if not interrupt on change type
                    read_defval = self.read_byte_data(self.DEFVALA[0] + offset)
                    if (int_defval == self.HIGH):
                        defval_data = read_defval | (1 << int(pin[1]))
                    elif (int_defval == self.LOW):
                        defval_data = read_defval & ( 0xFF - (1 << int(pin[1])) )
                    else:
                        print("ERROR defval must be either 1 for high or 0 for low")
                        return -1
                    if (self.debug == True):
                        print("Write address 0x{:02x} with data 0x{:02x}".format(self.DEFVALA[0] + offset, defval_data))
                    self.write_byte_data(self.DEFVALA[0] + offset, defval_data)
                if (self.debug == True):
                    print("Write address 0x{:02x} with data 0x{:02x}".format(self.INTCONA[0] + offset, int_on_change_data))
                self.write_byte_data(self.INTCONA[0] + offset, int_on_change_data)
            else:
                int_en_data = read_int_en & ( 0xFF - (1 << int(pin[1])) )
            if (self.debug == True):
                print("Write address 0x{:02x} with data 0x{:02x}".format(self.GPINTENA[0] + offset, int_en_data))
            self.write_byte_data(self.GPINTENA[0] + offset, int_en_data)
        #check and set output direction
        elif (direction == self.OUT):
            direction_data = read_direction & ( 0xFF - (1 << int(pin[1])) )
            #check and set output value
            read_out_val = self.read_byte_data(self.OLATA[0] + offset)
            if (out_val == self.HIGH):
                out_val_data = read_out_val | (1 << int(pin[1]))
            elif (out_val == self.LOW):
                out_val_data = read_out_val & ( 0xFF - (1 << int(pin[1])) )
            else:
                print("ERROR out_val must be either 1 for high or 0 for low")
                return -1
            if (self.debug == True):
                print("Write address 0x{:02x} with data 0x{:02x}".format(self.OLATA[0] + offset, out_val_data))
            self.write_byte_data(self.OLATA[0] + offset, out_val_data)
        else:
            print("ERROR direction must be either 1 for input or 0 for output")
            return -1
        if (self.debug == True):
            print("Write address 0x{:02x} with data 0x{:02x}".format(self.IODIRA[0] + offset, direction_data))
        self.write_byte_data(self.IODIRA[0] + offset, direction_data)

    def output(self, pin='a0', out_val=LOW):
        offset = self.check_valid_pin(pin)
        #check direction
        read_direction = self.read_byte_data(self.IODIRA[0] + offset)
        if ((read_direction >> int(pin[1])) & self.IN):
            print("ERROR pin {:s} already configured as an input".format(pin))
            return -1
        read_out_val = self.read_byte_data(self.OLATA[0] + offset)
        if (out_val == self.HIGH):
            out_val_data = read_out_val | (1 << int(pin[1]))
        elif (out_val == self.LOW):
            out_val_data = read_out_val & ( 0xFF - (1 << int(pin[1])) )
        else:
            print("ERROR out_val must be either 1 for high or 0 for low")
            return -1
        if (self.debug == True):
            print("Write address 0x{:02x} with data 0x{:02x}".format(self.OLATA[0] + offset, out_val_data))
        self.write_byte_data(self.OLATA[0] + offset, out_val_data)

    # Be care when using this function with interrupts enabled as this function will clear the pin interrupt 
    def input(self, pin='a0'):
        offset = self.check_valid_pin(pin)
        #check direction
        read_direction = self.read_byte_data(self.IODIRA[0] + offset)
        if ((read_direction >> int(pin[1])) & self.IN != True):
            print("ERROR pin {:s} already configured as an output".format(pin))
            return -1
        read_gpio = self.read_byte_data(self.GPIOA[0] + offset)
        if ((read_gpio >> int(pin[1])) & self.HIGH):
            return self.HIGH
        else:
            return self.LOW

    def write_regs_por(self):
        for reg in self.list_of_regs:
            if (reg[2] == 'RW'):
                self.write_byte_data(reg[0],     reg[1])
                self.write_byte_data(reg[0] + 1, reg[1])
                if (self.debug == True):
                    print("Write to {:s}A and {:s}B value 0x{:02x}".format(reg[3],reg[3],reg[1]))

    def read_intcap(self):
        read_intcapa = self.read_byte_data(self.INTCAPA[0])
        read_intcapb = self.read_byte_data(self.INTCAPA[0] + 1)
        for pin in range(0,8):
            if ((read_intcapa >> pin) & self.HIGH):
                print("GPA{:d} caused an interrupt".format(pin))
            if ((read_intcapb >> pin) & self.HIGH):
                print("GPB{:d} caused an interrupt".format(pin))
        if (self.debug == True):
            print("INTCAPA is 0x{:02x} and INTCAPB is 0x{:02x}".format(read_intcapa,read_intcapb))

    # Be care when using this function with interrupts enabled as this function will clear the pin interrupt 
    def read_gpio(self):
        read_gpioa = self.read_byte_data(self.GPIOA[0])
        read_gpiob = self.read_byte_data(self.GPIOA[0] + 1)
        if (self.debug == True):
            print("GPIOA is 0x{:02x} and GPIOB is 0x{:02x}".format(read_gpioa,read_gpiob))