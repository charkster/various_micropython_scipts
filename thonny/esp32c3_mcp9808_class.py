import machine
import ustruct

#devices = i2c.scan()
#if devices:
#    for d in devices:
#        print(hex(d))

class MCP9808():

    ADDR_CONF   = 0x01
    ADDR_TUPPER = 0x02
    ADDR_TLOWER = 0x03
    ADDR_TCRIT  = 0x04
    ADDR_TEMP   = 0x05
    
    ADC_LSB     = 0.0625
    
    CONF_ALERT_INT       = 0x01
    CONF_ALERT_ACT_HIGH  = 0x02
    CONF_ALERT_ENABLE    = 0x08
    CONF_ALERT_INT_CLEAR = 0x20


    def __init__(self, i2c_dev_addr=0x18, debug=False):
        self.i2c          = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=100000) # esp32c3 xiao
        self.i2c_dev_addr = i2c_dev_addr
        self.alert_mode   = self.CONF_ALERT_INT | self.CONF_ALERT_ACT_HIGH | self.CONF_ALERT_ENABLE
        self.debug        = debug
    
    def get_temp(self, addr=0x05): # addr=0x05 is ambient, 0x02 is Tupper, 0x03 is Tlower, 0x04 is Tcrit
        temp_bytes   = self.i2c.readfrom_mem(self.i2c_dev_addr,addr,2)
        temp_decimal = ustruct.unpack_from(">h", temp_bytes,0)[0]
        temp_float   = (temp_decimal & 0x0FFF) * self.ADC_LSB
        temp_sign    = (temp_decimal & 0x1000) >> 13
        if (temp_sign == 1):
            return -1.0 * temp_float
        else:
            return temp_float

    def set_temp(self, addr=0x04, temp=50.0): # addr=0x02 is Tupper, 0x03 is Tlower, 0x04 is Tcrit
        temp_dec = int(temp / self.ADC_LSB)
        byte_msb = (temp_dec & 0x0F00) >> 8
        byte_lsb = (temp_dec & 0xFF)
        if (temp < 0.0):
            byte_msb = byte_msb + 0x10 # sign bit        
        self.i2c.writeto_mem(self.i2c_dev_addr,addr,bytearray([byte_msb, byte_lsb]))

    def enable_alarm(self):
        self.i2c.writeto_mem(self.i2c_dev_addr,self.ADDR_CONF,bytearray([0x00, self.alert_mode]))

    def clear_int(self):
        val_list = list(self.i2c.readfrom_mem(self.i2c_dev_addr,self.ADDR_CONF,2))
        val_list[1] = val_list[1] | self.CONF_ALERT_INT_CLEAR
        self.i2c.writeto_mem(self.i2c_dev_addr,self.ADDR_CONF,bytearray(val_list))

mcp9808 = MCP9808()
mcp9808.set_temp(addr=mcp9808.ADDR_TUPPER, temp=26.0)
mcp9808.set_temp(addr=mcp9808.ADDR_TLOWER, temp=0.0)
mcp9808.set_temp(addr=mcp9808.ADDR_TCRIT,  temp=50.0)
mcp9808.enable_alarm()
mcp9808.clear_int()
mcp9808.get_temp(addr=mcp9808.ADDR_TEMP)
mcp9808.get_temp(addr=mcp9808.ADDR_TUPPER)
mcp9808.get_temp(addr=mcp9808.ADDR_TLOWER)
mcp9808.get_temp(addr=mcp9808.ADDR_TCRIT)