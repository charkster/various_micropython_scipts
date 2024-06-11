import machine

class INA260():

    _INA260_DEVICE_ADDRESS   = 0x44
    _INA260_CONFIG_ADDR      = 0x00
    _INA260_CURRENT_ADDR     = 0x01
    _INA260_BUS_VOLTAGE_ADDR = 0x02
    _INA260_MASK_ENABLE_ADDR = 0x06
    _INA260_ALERT_LIMIT_ADDR = 0x07
    _INA260_BUS_VOLTAGE_LSB  = 1.25 #mV
    _INA260_CURRENT_LSB      = 1.25 #mA

    # Constructor
    def __init__(self, i2c, i2c_dev_addr=0x44):
        self.i2c_dev_addr = i2c_dev_addr
        self.i2c          = i2c

    def twos_compliment_to_int(self, val, len):
        # Convert twos compliment to integer
        if(val & (1 << len - 1)):
            val = val - (1<<len)
        return val

    def get_bus_voltage(self):
        raw_read = list(self.i2c.readfrom_mem(self.i2c_dev_addr,self._INA260_BUS_VOLTAGE_ADDR,2))
        word_rdata = raw_read[0] *256 + raw_read[1]
        vbus = float(word_rdata) / 1000.0 * self._INA260_BUS_VOLTAGE_LSB
        return vbus

    def get_current(self):
        raw_read   = list(self.i2c.readfrom_mem(self.i2c_dev_addr,self._INA260_CURRENT_ADDR,2))
        word_rdata = raw_read[0] *256 + raw_read[1]
        current_twos_compliment = word_rdata
        current_sign_bit = current_twos_compliment >> 15
        if (current_sign_bit == 1):
            current = float(self.twos_compliment_to_int(current_twos_compliment, 16)) / 1000.0 * self._INA260_CURRENT_LSB
        else:
            current = float(current_twos_compliment) / 1000.0 * self._INA260_CURRENT_LSB
        return current

    def reset_chip(self):
        byte_list = [0x80, 0x00]
        self.i2c.writeto_mem(self.i2c_dev_addr,self._INA260_CONFIG_ADDR,bytearray(byte_list))
        
    def set_alert_current_limit(self, cur_lim=0.1, enable=True):
        if (enable == False):
            self.i2c.writeto_mem(self.i2c_dev_addr, self._INA260_MASK_ENABLE_ADDR, bytearray([0x00, 0x00]))
        else:
            self.i2c.writeto_mem(self.i2c_dev_addr, self._INA260_MASK_ENABLE_ADDR, bytearray([0x80, 0x00])) # OCL
        val = int((cur_lim * 1000) / self._INA260_CURRENT_LSB)
        byte1 = (val >> 8) & 0xFF
        byte0 = val & 0xFF
        self.i2c.writeto_mem(self.i2c_dev_addr, self._INA260_ALERT_LIMIT_ADDR, bytearray([byte1, byte0]))
    
    
    