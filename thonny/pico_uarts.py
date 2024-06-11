import machine
uart0 = machine.UART(0, baudrate=912600, tx=machine.Pin(0), rx=machine.Pin(1))
uart1 = machine.UART(1, baudrate=912600, tx=machine.Pin(4), rx=machine.Pin(5))
uart1.write('hello')  # write 5 bytes
uart0.read(5)         # read up to 5 bytes