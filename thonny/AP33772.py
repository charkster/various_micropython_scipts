
class AP37772:
    
    # Constructor
    def __init__(self, i2c):
        self.i2c      = i2c
        self.slave_id = 0x51
        
    def write_data(self, address=0x00, data=0x00): # write data
        num_bytes = (data.bit_length() + 7) // 8
        self.i2c.writeto_mem(self.slave_id, address, data.to_bytes(num_bytes, "little"))
    
    def read_data(self, address=0x00, num_bytes=1):
        int_read_byte = int.from_bytes(self.i2c.readfrom_mem(self.slave_id, address, num_bytes), "little")
        return int_read_byte # int value
    
    _SRCPDO_ADDR      = 0x00
    _SRCPDO_NUM_PDO   = 7
    _SRCPDO_NUM_BYTES = 4
    
    _PDO_TYPE_WIDTH  = 2
    _PDO_TYPE_OFFSET = 30
    _PDO_TYPE_FIXED = 0
    _PDO_TYPE_ADPO  = 3
    
    _PDO_FIXED_VOLTAGE_WIDTH    = 10
    _PDO_FIXED_VOLTAGE_OFFSET   = 10
    _PDO_FIXED_VOLTAGE_LSB      = 0.05 # 50mV
    
    _PDO_FIXED_CURRENT_WIDTH  = 10
    _PDO_FIXED_CURRENT_OFFSET = 0
    _PDO_FIXED_CURRENT_LSB    = 0.01 # 10mA
    
    _PDO_PPS_TYPE_WIDTH   = 2
    _PDO_PPS_TYPE_OFFSET  = 28
    _PDO_PPS_TYPE         = 0
    
    _PDO_PPS_MAX_VOLTAGE_WIDTH  = 8
    _PDO_PPS_MAX_VOLTAGE_OFFSET = 17
    _PDO_PPS_MIN_VOLTAGE_WIDTH  = 8
    _PDO_PPS_MIN_VOLTAGE_OFFSET = 8
    _PDO_PPS_VOLTAGE_LSB        = 0.1 # 100mV
    
    _PDO_PPS_CURRENT_WIDTH  = 7
    _PDO_PPS_CURRENT_OFFSET = 0
    _PDO_PPS_CURRENT_LSB    = 0.05 # 50mA
    
    def get_pdo(self, num=1):
        pdo_all = self.read_data(address=self._SRCPDO_ADDR, num_bytes=(self._SRCPDO_NUM_PDO * self._SRCPDO_NUM_BYTES))
        pdo_dword = (pdo_all >> ((num-1)*32)) & (2**(self._SRCPDO_NUM_BYTES * 8) - 1)
        pdo_type_raw = int((pdo_dword >> self._PDO_TYPE_OFFSET) & (2**self._PDO_PPS_TYPE_WIDTH-1))
        if (pdo_type_raw == self._PDO_TYPE_FIXED):
            pdo_type = 'FIXED'
            voltage = ((pdo_dword >> self._PDO_FIXED_VOLTAGE_OFFSET) & (2**self._PDO_FIXED_VOLTAGE_WIDTH-1)) * self._PDO_FIXED_VOLTAGE_LSB
            current = ((pdo_dword >> self._PDO_FIXED_CURRENT_OFFSET) & (2**self._PDO_FIXED_CURRENT_WIDTH-1)) * self._PDO_FIXED_CURRENT_LSB
            return [num, pdo_type, voltage, current]
        elif (pdo_type_raw == self._PDO_TYPE_ADPO) and (((pdo_dword >> self._PDO_PPS_TYPE_OFFSET) & (2**self._PDO_PPS_TYPE_WIDTH-1)) == self._PDO_PPS_TYPE):
            pdo_type = 'PPS'
            voltage_max = ((pdo_dword >> self._PDO_PPS_MAX_VOLTAGE_OFFSET) & (2**self._PDO_PPS_MAX_VOLTAGE_WIDTH-1)) * self._PDO_PPS_VOLTAGE_LSB
            voltage_min = ((pdo_dword >> self._PDO_PPS_MIN_VOLTAGE_OFFSET) & (2**self._PDO_PPS_MIN_VOLTAGE_WIDTH-1)) * self._PDO_PPS_VOLTAGE_LSB
            current     = ((pdo_dword >> self._PDO_PPS_CURRENT_OFFSET) & (2**self._PDO_PPS_CURRENT_WIDTH-1)) * self._PDO_PPS_CURRENT_LSB
            return [num, pdo_type, voltage_max, voltage_min, current]
        else:
            return ['invalid']

    _PDONUM_ADDR = 0x1C
    
    def get_pdo_num(self):
        return self.read_data(address=self._PDONUM_ADDR, num_bytes=1)
    
    _STATUS_ADDR    = 0x1D # ALL BITS ARE CLEARED ON READ
    _MASK_ADDR      = 0x1E
    _STATUS_MASK_DR      = 0x80
    _STATUS_MASK_OTP     = 0x40
    _STATUS_MASK_OCP     = 0x20
    _STATUS_MASK_OVP     = 0x10
    _STATUS_MASK_NEWPDO  = 0x04
    _STATUS_MASK_SUCCESS = 0x02
    _STATUS_MASK_READY   = 0x01
    
    def get_pdo_status(self):
        pdo_status = self.read_data(address=self._STATUS_ADDR, num_bytes=1)
        status_list = []
        if (pdo_status & self._STATUS_MASK_READY):
            status_list.append('ready')
        if (pdo_status & self._STATUS_MASK_SUCCESS):
            status_list.append('success')
        if (pdo_status & self._STATUS_MASK_NEWPDO):
            status_list.append('new_pdo')
        if (pdo_status & self._STATUS_MASK_OVP):
            status_list.append('oover_voltage')
        if (pdo_status & self._STATUS_MASK_OCP):
            status_list.append('over_current')
        if (pdo_status & self._STATUS_MASK_OTP):
            status_list.append('over_temp')
        if (pdo_status & self._STATUS_MASK_DR):
            status_list.append('derate')
        return status_list

    _VOLTAGE_ADDR = 0x20 # ADC measured VOUT voltage
    _VOLTAGE_LSB  = 0.08 # 80mV
    
    def get_voltage(self):
        return self.read_data(address=self._VOLTAGE_ADDR, num_bytes=1) * self._VOLTAGE_LSB
    
    _CURRENT_ADDR = 0x21 # ADC measured VBUS current
    _CURRENT_LSB  = 0.024 # 24mA
    
    def get_current(self):
        return self.read_data(address=self._CURRENT_ADDR, num_bytes=1) * self._CURRENT_LSB
    
    _TEMP_ADDR = 0x22 # NTC Temperature, LSB is 1C
    
    def get_temp(self):
        return self.read_data(address=self._TEMP_ADDR, num_bytes=1) # LSB is 1C
    
    _RDO_ADDR      = 0x30 # Requested Data Object
    _RDO_NUM_BYTES = 4
    _RDO_POSITION_WIDTH  = 3 # Not needed as value 1 thru 7 fits into 3bits
    _RDO_POSITION_OFFSET = 28
    
    _RDO_FIXED_OP_CURRENT_WIDTH   = 10
    _RDO_FIXED_OP_CURRENT_OFFSET  = 10
    _RDO_FIXED_OP_CURRENT_LSB     = 0.01 # 10mA
    _RDO_FIXED_MAX_CURRENT_WIDTH  = 10
    _RDO_FIXED_MAX_CURRENT_OFFSET = 0
    _RDO_FIXED_MAX_CURRENT_LSB    = 0.01 # 10mA
    
    _RDO_PPS_VOLTAGE_WIDTH  = 11
    _RDO_PPS_VOLTAGE_OFFSET = 9
    _RDO_PPS_VOLTAGE_LSB    = 0.02 # 20mV
    _RDO_PPS_CURRENT_WIDTH  = 7
    _RDO_PPS_CURRENT_OFFSET = 0
    _RDO_PPS_CURRENT_LSB    = 0.05 # 50mA
    
    _RDO_RESET_COMMAND = 0 # 4 bytes of all zeros
    
    def send_rdo(self, type='FIXED', pdo_num=1, op_current=0.0, max_current=0.0, voltage=0.0):
        rdo_dword = 0
        rdo_dword = rdo_dword + ((pdo_num & (2**self._RDO_POSITION_WIDTH-1)) << self._RDO_POSITION_OFFSET)
        if (type=='FIXED'):
            rdo_dword = rdo_dword + ((int( op_current/self._RDO_FIXED_OP_CURRENT_LSB)  & (2**self._RDO_FIXED_OP_CURRENT_WIDTH-1))  << self._RDO_FIXED_OP_CURRENT_OFFSET)
            rdo_dword = rdo_dword + ((int(max_current/self._RDO_FIXED_MAX_CURRENT_LSB) & (2**self._RDO_FIXED_MAX_CURRENT_WIDTH-1)) << self._RDO_FIXED_MAX_CURRENT_OFFSET)
        if (type=='PPS'):
            rdo_dword = rdo_dword + ((int(   voltage/self._RDO_PPS_VOLTAGE_LSB) & (2**self._RDO_PPS_VOLTAGE_WIDTH-1)) << self._RDO_PPS_VOLTAGE_OFFSET)
            rdo_dword = rdo_dword + ((int(op_current/self._RDO_PPS_CURRENT_LSB) & (2**self._RDO_PPS_CURRENT_WIDTH-1)) << self._RDO_PPS_CURRENT_OFFSET)
        self.i2c.writeto_mem(self.slave_id, self._RDO_ADDR, rdo_dword.to_bytes(4, "little"))

    def send_rdo_reset(self):
        data = self._RDO_RESET_COMMAND
        self.i2c.writeto_mem(self.slave_id, self._RDO_ADDR, data.to_bytes(4, "little"))

    _OCPTHR_ADDR = 0x23 # Over Current threshold
    _OCPTHR_LSB  = 0.05 # 50mA
    
    _OTPTHR_ADDR = 0x24 # Over Temperature threshold, LSB is 1C
    
    _DRTHR_ADDR = 0x25 # Derating Temperature threshold, LSB is 1C
    
    _TR25_ADDR       = 0x28 # NTC Resistance at 25C, LSB 1 Ohm
    _TR25_NUM_BYTES = 2
    
    _TR15_ADDR      = 0x2A # NTC Resistance at 75C, LSB 1 Ohm
    _TR75_NUM_BYTES = 2
    
    _TR100_ADDR      = 0x2E # NTC Resistance at 100C, LSB 1 Ohm
    _TR100_NUM_BYTES = 2