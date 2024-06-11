import machine
import time

i2c = machine.I2C(scl=machine.Pin(7), sda=machine.Pin(6), freq=400000) 
v4040 = VCNL4040(i2c=i2c, debug=False)

v4040_int = machine.Pin(21, machine.Pin.IN, machine.Pin.PULL_UP)

# this is called when an interrupt is detected
def int_event(pin):
    v4040_int.irq(int_event, trigger=0) # disable IRQ
    check_int()
    print(v4040.read_flags())

v4040_int.irq(int_event, trigger=machine.Pin.IRQ_FALLING) # enable IRQ

def check_int():
    if (v4040_int.value()):
        print("INT pin is high, no interrupt")
    else:
        print("INT pin is low, interrupt is active")

print("--> Restore default values manually")
for bit_field in v4040.check_default_values():
    v4040.read_bf_and_print(bit_field)
time.sleep(1)
print("--> Print all non-default values, all sensor data is invalid as sensors are not enabled")
for bit_field in v4040.check_default_values():
    v4040.read_bf_and_print(bit_field)
print("--> Disable White LED (NOT USING IT)")
v4040.i2c_bf_write(v4040.BF_WHITE_EN, v4040.BF_WHITE_EN.TABLE_ENUM["DISABLE"])
print("--> Enable ALS")
v4040.i2c_bf_write(v4040.BF_ALS_IT, v4040.BF_ALS_IT.TABLE_ENUM["320ms"])
v4040.i2c_bf_write(v4040.BF_ALS_SD, v4040.BF_ALS_SD.TABLE_ENUM["ENABLE"])
time.sleep(1)
print("--> Print all non-default values")
for bit_field in v4040.check_default_values():
    v4040.read_bf_and_print(bit_field)
check_int()
print("--> Check ALS interrupts")
v4040.i2c_bf_write(v4040.BF_ALS_INT_EN, v4040.BF_ALS_INT_EN.TABLE_ENUM["ENABLE"])
time.sleep(1) # expect ALS_IF_H_INT
v4040.i2c_bf_write(v4040.BF_ALS_THDH, 0xFFFF) # set to a high value so that ALS_IF_H_INT doesn't get set anymore
v4040.i2c_bf_write(v4040.BF_ALS_THDL, 0xFFFF) # set to a high value so that we will see the ALS_IF_L_INT
time.sleep(1)  # expect ALS_IF_L_INT
v4040.i2c_bf_write(v4040.BF_ALS_THDL, 0x0000) # set to a low value so that ALS_IF_L_INT doesn't get set anymore
time.sleep(1) # expect nothing
check_int()
print("--> Check proximity sensor")
v4040.i2c_bf_write(v4040.BF_ALS_SD, v4040.BF_ALS_SD.TABLE_ENUM["DISABLE"])
v4040.i2c_bf_write(v4040.BF_LED_I, v4040.BF_LED_I.TABLE_ENUM["160mA"])
v4040.i2c_bf_write(v4040.BF_PS_CANC, 0x0008)
v4040.i2c_bf_write(v4040.BF_PS_THDH, 0x0005)
v4040.i2c_bf_write(v4040.BF_PS_INT, v4040.BF_PS_INT.TABLE_ENUM["TRIGGER_WHEN_CLOSE_OR_AWAY"])
#v4040.i2c_bf_write(v4040.BF_PS_SMART_PERS, v4040.BF_PS_SMART_PERS.TABLE_ENUM["ENABLE"])
v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_POWER_ON"])
for n in range(0,100):
    v4040.read_bf_and_print(v4040.BF_PS_DATA)
    time.sleep(0.1)
v4040.i2c_bf_write(v4040.BF_PS_SD, v4040.BF_PS_SD.TABLE_ENUM["PS_SHUT_DOWN"])
print("--> Print all non-default values")
for bit_field in v4040.check_default_values():
    v4040.read_bf_and_print(bit_field)