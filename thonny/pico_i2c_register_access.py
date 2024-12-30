import machine
from machine import mem32

#machine.freq(125000000)

#CLOCKS_BASE      = 0x40008000 # RP20240
#I2C0_BASE        = 0x40044000 # RP2040
#I2C1_BASE        = 0x40048000 # RP2040
CLOCKS_BASE      = 0x40010000 # RP2350
I2C0_BASE        = 0x40090000 # RP2350
I2C1_BASE        = 0x40098000 # RP2350
IC_CON_0         = I2C0_BASE   + 0x00
IC_CON_1         = I2C1_BASE   + 0x00
IC_ENABLE_0      = I2C0_BASE   + 0x6C
IC_ENABLE_1      = I2C1_BASE   + 0x6C
IC_SS_SCL_HCNT_0 = I2C0_BASE   + 0x14
IC_SS_SCL_HCNT_1 = I2C1_BASE   + 0x14
IC_SS_SCL_LCNT_0 = I2C0_BASE   + 0x18
IC_SS_SCL_LCNT_1 = I2C1_BASE   + 0x18
IC_FS_SCL_HCNT_0 = I2C0_BASE   + 0x1C
IC_FS_SCL_HCNT_1 = I2C1_BASE   + 0x1C
IC_FS_SCL_LCNT_0 = I2C0_BASE   + 0x20
IC_FS_SCL_LCNT_1 = I2C1_BASE   + 0x20
IC_FS_SPKLEN_0   = I2C0_BASE   + 0xA0
IC_FS_SPKLEN_1   = I2C1_BASE   + 0xA0
CLK_SYS_DIV      = CLOCKS_BASE + 0x40

def print_regs():
    print("IC_ENABLE_0 enable is {:d}".format((mem32[IC_ENABLE_0] & 0x00000001))) # bit [0] is enable
    print("IC_CON_0 speed is {:d}".format((mem32[IC_CON_0] & 0x00000006)>>1)) # bits [2:1] are speed
    print("IC_SS_SCL_HCNT_0 is {:d}".format(mem32[IC_SS_SCL_HCNT_0] & 0x0000FFFF)) # lower 16bits
    print("IC_SS_SCL_LCNT_0 is {:d}".format(mem32[IC_SS_SCL_LCNT_0] & 0x0000FFFF)) # lower 16bits
    print("IC_FS_SCL_HCNT_0 is {:d}".format(mem32[IC_FS_SCL_HCNT_0] & 0x0000FFFF)) # lower 16bits
    print("IC_FS_SCL_LCNT_0 is {:d}".format(mem32[IC_FS_SCL_LCNT_0] & 0x0000FFFF)) # lower 16bits
    print("IC_FS_SPKLEN_0 is {:d}".format(mem32[IC_FS_SPKLEN_0] & 0x000000FF)) # lower 8bits
    print("IC_ENABLE_1 enable is {:d}".format((mem32[IC_ENABLE_1] & 0x00000001))) # bit [0] is enable
    print("IC_CON_1 speed is {:d}".format((mem32[IC_CON_1] & 0x00000006)>>1)) # bits [2:1] are speed
    print("IC_SS_SCL_HCNT_1 is {:d}".format(mem32[IC_SS_SCL_HCNT_1] & 0x0000FFFF)) # lower 16bits
    print("IC_SS_SCL_LCNT_1 is {:d}".format(mem32[IC_SS_SCL_LCNT_1] & 0x0000FFFF)) # lower 16bits
    print("IC_FS_SCL_HCNT_1 is {:d}".format(mem32[IC_FS_SCL_HCNT_1] & 0x0000FFFF)) # lower 16bits
    print("IC_FS_SCL_LCNT_1 is {:d}".format(mem32[IC_FS_SCL_LCNT_1] & 0x0000FFFF)) # lower 16bits
    print("IC_FS_SPKLEN_1 is {:d}".format(mem32[IC_FS_SPKLEN_1] & 0x000000FF)) # lower 8bits
    print("CLK_SYS_DIV_INT  is {:d}".format((mem32[CLK_SYS_DIV] & 0xFFFFFF00)>>8)) # bits [31:8] are INT div
    print("CLK_SYS_DIV_FRAC is {:d}".format((mem32[CLK_SYS_DIV] & 0x000000FF))) # bits [8:0] are Fractional div

# rp2040 xiao
#i2c = machine.I2C(1,scl=machine.Pin(7), sda=machine.Pin(6),freq=400000)
# rp2040 pico
#i2c = machine.I2C(1,sda=machine.Pin(2),scl=machine.Pin(3),freq=400000)
# samd21 xiao
#i2c = machine.I2C(0,sda=machine.Pin(8),scl=machine.Pin(9),freq=400000)
# samd21 qt py
#i2c = machine.I2C(1,sda=machine.Pin(16), scl=machine.Pin(17),freq=1000000)
# PICO 2
i2c = machine.I2C(0,scl=machine.Pin(5), sda=machine.Pin(4),freq=400000)

print("i2c = machine.I2C(1,freq=400000)")

print("IC_CON_0 speed is {:d}".format((mem32[IC_CON_0] & 0x00000006)>>1)) # bits [2:1] are speed
print("IC_CON_1 speed is {:d}".format((mem32[IC_CON_1] & 0x00000006)>>1)) # bits [2:1] are speed
print("IC_ENABLE_0 enable is {:d}".format((mem32[IC_ENABLE_0] & 0x00000001))) # bit [0] is enable
print("IC_ENABLE_1 enable is {:d}".format((mem32[IC_ENABLE_1] & 0x00000001))) # bit [0] is enable
print("IC_FS_SCL_HCNT_0 is {:d}".format(mem32[IC_FS_SCL_HCNT_0] & 0x0000FFFF)) # lower 16bits
print("IC_FS_SCL_HCNT_1 is {:d}".format(mem32[IC_FS_SCL_HCNT_1] & 0x0000FFFF)) # lower 16bits
print("IC_FS_SCL_LCNT_0 is {:d}".format(mem32[IC_FS_SCL_LCNT_0] & 0x0000FFFF)) # lower 16bits
print("IC_FS_SCL_LCNT_1 is {:d}".format(mem32[IC_FS_SCL_LCNT_1] & 0x0000FFFF)) # lower 16bits
print("CLK_SYS_DIV_INT  is {:d}".format((mem32[CLK_SYS_DIV] & 0xFFFFFF00)>>8)) # bits [31:8] are INT div
print("CLK_SYS_DIV_FRAC is {:d}".format((mem32[CLK_SYS_DIV] & 0x000000FF))) # bits [8:0] are Fractional div

mem32[IC_ENABLE_0] = 0
mem32[IC_FS_SCL_HCNT_0] = 100
mem32[IC_FS_SCL_LCNT_0] = 80
mem32[IC_FS_SPKLEN_0] = 5
mem32[IC_ENABLE_0] = 1