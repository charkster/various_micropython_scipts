import machine
import time

def main():
    vbus_div2 = machine.ADC(machine.Pin(1)) # two 120k resistor divider for VBUS
    vbus_div2.atten(machine.ADC.ATTN_11DB) # use 3.3V range
    f = open('logfile.csv', 'w')
    try:
        while True:
            vbus_mv = int(vbus_div2.read_uv()*2/1e3) # millivolt
            f.write("{:d}\n".format(vbus_mv))
#            machine.deepsleep(1*1000) # 60 seconds
            time.sleep(1)
    except KeyboardInterrupt:
        f.close()

if __name__ == '__main__':  
   main()
