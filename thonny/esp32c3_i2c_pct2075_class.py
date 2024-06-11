import machine
import ustruct

class PCT2075():

    ADDR_TEMP   = 0x00
    ADDR_CONF   = 0x01
    ADDR_THYST  = 0x02
    ADDR_TOS    = 0x03
    ADDR_TIDLE  = 0x04
    
    CONF_OS_F_QUE_6  = 0x18 # 6 consecutive
    CONF_OS_F_QUE_4  = 0x10 # 4 consecutive
    CONF_OS_F_QUE_2  = 0x08 # 2 consecutive
    CONF_OS_F_QUE_1  = 0x00 # 1 consecutive
    CONF_OS_POL_HIGH = 0x04
    CONF_OS_INT      = 0x02
    CONF_OS_SHUTDOWN = 0x01
    
    ADC_LSB      = 0.125
    TOS_HYST_LSB = 0.5

    def __init__(self, i2c_dev_addr=0x37, debug=False):
        self.i2c          = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=100000) # esp32c3 xiao
        self.i2c_dev_addr = i2c_dev_addr
        self.os_mode      = self.CONF_OS_INT | self.CONF_OS_POL_HIGH | self.CONF_OS_F_QUE_6
        self.debug        = debug

    def get_temp(self, addr):
        if (addr == self.ADDR_TEMP):
            return (ustruct.unpack(">h",self.i2c.readfrom_mem(self.i2c_dev_addr,addr,2))[0] >> 5) * self.ADC_LSB
        else:
            return (ustruct.unpack(">h",self.i2c.readfrom_mem(self.i2c_dev_addr,addr,2))[0] >> 7) * self.TOS_HYST_LSB

    def set_temp(self, addr, temp): # no negative temps, only for TOS and THYST
        temp_dec = int(temp * 2.0)
        byte_msb = (temp_dec & 0x1FF) >> 1
        byte_lsb = (temp_dec & 0x1FF) >> 8
        self.i2c.writeto_mem(self.i2c_dev_addr,addr,bytearray([byte_msb, byte_lsb]))
    
    def enable_os_pin(self):
        self.i2c.writeto_mem(self.i2c_dev_addr,self.ADDR_CONF,bytearray(self.os_mode))

    def clear_os_int(self):
        self.i2c.readfrom_mem(self.i2c_dev_addr,self.ADDR_CONF,1)

pct2075 = PCT2075()
print(pct2075.get_temp(addr=pct2075.ADDR_TEMP))
pct2075.set_temp(addr=pct2075.ADDR_TOS, temp=27.0)
print(pct2075.get_temp(addr=pct2075.ADDR_TOS))
pct2075.set_temp(addr=pct2075.ADDR_THYST, temp=27.0)
print(pct2075.get_temp(addr=pct2075.ADDR_THYST))
pct2075.enable_os_pin()
pct2075.clear_os_int()